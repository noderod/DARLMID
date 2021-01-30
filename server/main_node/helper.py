"""
BASICS

Auxiliary functions for traffic.py
"""


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
