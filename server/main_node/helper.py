"""
SUMMARY

Auxiliary functions for traffic.py
"""

import os
import random
import uuid

import aioredis
import bleach


"""
Checks if a dictionary contains certain keys -> boolean

dict_to_be_checked (dict)
keys_to_be_checked (arr)
"""
def check_keys_in_dict(dict_to_be_checked, keys_to_be_checked):

    for a_key in keys_to_be_checked:
        if a_key not in dict_to_be_checked:
            return False

    # All keys are checked to be in
    return True



"""
Returns a list of the checked keys which are not keys in the dict -> []

dict_to_be_checked (dict)
keys_to_be_checked (arr)
"""
def missing_keys_in_dict(dict_to_be_checked, keys_to_be_checked):

    missing_keys = []

    for a_key in keys_to_be_checked:
        if a_key not in dict_to_be_checked:
            missing_keys.append(a_key)

    # All keys are checked to be in
    return missing_keys



"""
Sanitizes a certain string, replacing HTML tags by HTML symbols. -> str

given_str (str)
"""
def sanitize_str_for_HTML(given_str):
    return bleach.clean(given_str, tags=[])



"""
Generates a random key identifier
"""
def generate_key_identifier():
    return uuid.uuid4().hex + str(random.random())



"""
Generates a record of the user and this cookie in Redis

key_ID (str)
username (str)
expire_at (int/float): How long until the cookie expires
"""
async def generate_cookie_record(key_ID, username, expire_at):
    redis = await aioredis.create_redis(address = (os.environ["REDIS_HOST"], 6379), db = 0, password = os.environ["REDIS_PASSWORD"])
    await redis.hmset_dict(key_ID, {"username": username})
    await redis.expire(key_ID, int(expire_at))
    redis.close()
    await redis.wait_closed()



"""
Verifies that a cookie's key exists

key_ID (str)
"""
async def verify_cookie_key(key_ID):
    redis = await aioredis.create_redis(address = (os.environ["REDIS_HOST"], 6379), db = 0, password = os.environ["REDIS_PASSWORD"])
    key_exists = await redis.exists(key_ID)
    redis.close()
    await redis.wait_closed()

    return key_exists



"""
Deletes a key from the cookie's local Redis copy.
Does nothing if the key does not exist

key_ID (str)
"""
async def delete_cookie_key(key_ID):
    redis = await aioredis.create_redis(address = (os.environ["REDIS_HOST"], 6379), db = 0, password = os.environ["REDIS_PASSWORD"])

    # Deletes key if it exists
    if await redis.exists(key_ID):
        await redis.delete(key_ID)

    redis.close()
    await redis.wait_closed()



"""
Obtains all the information attached to a user currently stored in Redis

key_ID (str)
"""
async def get_user_session_info(key_ID):
    redis = await aioredis.create_redis(address = (os.environ["REDIS_HOST"], 6379), db = 0, password = os.environ["REDIS_PASSWORD"])

    # Deletes key if it exists
    info = decode_utf8_dict(await redis.hgetall(key_ID))

    redis.close()
    await redis.wait_closed()

    return info



"""
Decodes a dictionary with both keys and values encoded in UTF-8. Probably obtained directly from Redis

# encoded_dict (dict) {str: str}
"""
def decode_utf8_dict(encoded_dict):

    A = {}

    utf8_encoding = "UTF-8"

    for a_key in encoded_dict:
        A[a_key.decode(utf8_encoding)] = encoded_dict[a_key].decode(utf8_encoding)

    return A

