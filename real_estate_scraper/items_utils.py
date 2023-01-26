import re

def extract_floor(value):
    num = re.sub("[^*\d]", '', value)
    try:
        num = int(num)
        return num
    except ValueError:
        return 0


def merge_all_features(*feature_lists):
    all_features = set()
    for feautre_list in feature_lists:
        if isinstance(feautre_list, list):
            for feature in feautre_list:
                all_features.add(feature)
    
    return list(all_features)


def has_feature(feature_list, feature):
    return feature in feature_list


def extract_estate_floors(value):
    if 'one' in value:
        return '1'
    if 'two' in value:
        return '2'
    if 'more' in value:
        return '3 or more'
    
    return value


def translate_offer_type(value):
    if 'sprze' in value:
        return 'sell'
    if 'wyna' in value:
        return 'rental'
    
    return value


def translate_regular_user(value):
    if value == 'y':
        return True
    else:
        return False


def translate_proper_type(value):
    if 'mieszkanie' in value:
        return 'flat'
    if 'dom' in value:
        return 'house'
    
    return value


def get_heating(*args):
    return merge_all_features(*args)[0] if merge_all_features(*args) else None


def get_secondary_heating(heating_1, heating_types):
    secondary_heating = list(filter(lambda x: x != heating_1, heating_types))
    if secondary_heating:
        return secondary_heating[0]
    else:
        return None

