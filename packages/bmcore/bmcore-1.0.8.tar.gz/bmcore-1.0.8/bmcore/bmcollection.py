from typing import List
from bmcore.bmtypes import *
import logging
import json
import random
import redis


logger = logging.getLogger(__name__)


class Metadatum:
    def __init__(self, value: dict) -> None:
        self.value = value
        self.json_str = json.dumps(value)

    def validate(self):
        for key, val in self.value.items():
            if isinstance(val, str) and len(val) > 64:
                raise ValueError(
                    f"The value of '{key}' is greater than 64 characters")
        if "name" not in self.value:
            raise ValueError("The 'name' field is missing")
        if "image" not in self.value:
            raise ValueError("The 'image' field is missing")
        elif not self.value["image"].startswith("ipfs://"):
            raise ValueError(
                "The 'image' field should be prefixed by 'ipfs://'")


class BaseType:
    def __init__(self, env: BMEnvironment, policy_id: str) -> None:
        self.env = env
        self.redis = redis.Redis.from_url(env.db_connection_string)
        self.policy_id = policy_id
        self.prefix = f"{policy_id}:{self.__class__.__name__}:"

    def add_prefix(self, key):
        return self.prefix + key

    def DANGER_flush(self):
        with self.redis.pipeline() as pipe:
            for key in self.redis.scan_iter(self.prefix + "*"):
                pipe.delete(key)
            pipe.execute()


class BMCollection(BaseType):
    def set_collection_json(self, metadata: dict):
        try:
            _metadata = metadata["721"][self.policy_id]
            pipeline = self.redis.pipeline(transaction=False)

            for (asset_name, value) in _metadata.items():
                metadatum = Metadatum(value)
                metadatum.validate()
                pipeline.set(self.add_prefix(asset_name), metadatum.json_str)

            pipeline.execute(raise_on_error=True)

        except redis.RedisError as e:
            logger.error(f"Error writing to Redis: {e}")
            raise

    def get_metadata(self, asset_name):
        metadata_bytes = self.redis.get(self.add_prefix(asset_name))
        if metadata_bytes:
            metadata_str = metadata_bytes.decode('utf-8')
            return json.loads(metadata_str)
        else:
            return None

    def size(self):
        return len(self.redis.keys(self.prefix + "*"))


class BMFreeAssets(BaseType):
    def add_items(self, asset_names: List[str], partition=None):
        if (not asset_names):
            return

        key = None
        if (partition):
            key = self.add_prefix(f"list:{partition}")
        else:
            key = self.add_prefix("list")

        with self.redis.pipeline() as pipe:
            pipe.sadd(key, *asset_names)
            pipe.execute()

    def pop_n_random(self, count, partition=None):
        if (partition):
            key = self.add_prefix(f"list:{partition}")
        else:
            key = self.add_prefix("list")
        return {element.decode() for element in self.redis.spop(key, count)}

    def get_all(self):
        return {element.decode() for element in self.redis.smembers(self.add_prefix("list"))}


class BMReservedAssets(BaseType):
    def reserve_items(self, asset_names: List[str], ttl_minutes=BMConstants.MINTING_SESSION_TTL_MINUTES):
        with self.redis.pipeline() as pipe:
            pipe.sadd(self.add_prefix("list"), *asset_names)
            for asset_name in asset_names:
                pipe.setex(self.add_prefix(asset_name),
                           (ttl_minutes + 1) * 60, "")
            pipe.execute()

    def is_reserved(self, asset_name):
        return self.redis.exists(self.add_prefix(asset_name))

    def mark_items_as_minted(self, asset_names):
        with self.redis.pipeline() as pipe:
            for asset_name in asset_names:
                pipe.srem(self.add_prefix("list"), asset_name)
                pipe.delete(self.add_prefix(asset_name))
            pipe.execute()

    def move_back_to_free(self, asset_names, free_assets: BMFreeAssets):
        if not asset_names:
            return

        with self.redis.pipeline() as pipe:
            for asset_name in asset_names:
                pipe.smove(self.add_prefix("list"),
                           free_assets.add_prefix("list"), asset_name)
            pipe.execute()

    def get_all(self):
        return {element.decode() for element in self.redis.smembers(self.add_prefix("list"))}


class BMMintedAssets(BaseType):

    def __init__(self, env: BMEnvironment, project: BMProject, api=None) -> None:
        if (api is None):
            self.api = env.chain_context.api
        else:
            self.api = api
        super().__init__(env, project)

    def get_all(self):
        try:
            minted_assets = []
            for asset in self.api.assets_policy(self.policy_id, gather_pages=True):
                hrname = BMMintedAssets.get_hrname(self.policy_id, asset.asset)
                minted_assets.append(hrname)
            return set(minted_assets)
        except Exception as e:
            logger.error(f"Error getting minted assets: {e}")
            return set([])

    @staticmethod
    def get_hrname(policy_id, name):
        hex = name.replace(policy_id, '')
        return bytes.fromhex(hex).decode('utf-8')


class Differ():

    def __init__(self, free_assets: BMFreeAssets, reserved_assets: BMReservedAssets, minted_assets: BMMintedAssets) -> None:
        self.free_assets = free_assets
        self.reserved_assets = reserved_assets
        self.minted_assets = minted_assets

    def eval(self):
        minted_on_chain = self.minted_assets.get_all()
        reserved = self.reserved_assets.get_all()

        successfuly_minted = []
        failed_mints = []

        for asset in reserved:
            if (asset in minted_on_chain):
                successfuly_minted.append(asset)
            elif (not self.reserved_assets.is_reserved(asset)):
                failed_mints.append(asset)

        self.reserved_assets.mark_items_as_minted(successfuly_minted)
        self.reserved_assets.move_back_to_free(failed_mints, self.free_assets)
