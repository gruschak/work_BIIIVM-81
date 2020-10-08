from typing import List, Optional, Dict, TypedDict
import pandas as pd
import csv

FEATURES_INPUT = ['other_diagnoses__ischemic_heart_disease', 'kbs__characteristic__compressive', 'kbs__characteristic__fully_relief', 'kbs__relief__medicines', 'other_diagnoses__myocardial_infarction', 'bad_habits__alcohol', 'other_symptoms__general_weakness', 'blood_pressure__during_at_checkup', 'blood_pressure__during_at_lifetime', 'kbs__characteristic__occurs_at_physical_activity', 'other_symptoms__dyspnea', 'other_diagnoses__hypertension']
HEART_ATTACK_FEATURES = None


class HeartAttackFeature(object):
    def __init__(self):
        self.id = None
        self.group_code = None
        self.code = None
        self.name = None


class HeartAttackFeatures(object):
    """ Признаки для heart_attack """
    def __init__(self):
        self._features = []

    @property
    def features(self) -> List[HeartAttackFeature]:
        """ """
        return self._features


def load_heart_attack_features(path: str) -> HeartAttackFeatures:
    """ """
    result = HeartAttackFeatures()

    with open(path, "rt") as f:
        reader = csv.reader(f, delimiter=",")
        next(reader, None)  # скипаем первую запись
        for row in reader:
            feature = HeartAttackFeature()
            feature.id = int(row[0])
            feature.group_code = int(row[1])
            feature.code = row[2]
            feature.name = row[3]
            result.features.append(feature)

    return result


# ----------------------------------------------------------------------------------------------------------------------
# Группы признаков
# ----------------------------------------------------------------------------------------------------------------------
class HeartAttackFeatureGroup(object):
    """ Группа признаков """

    def __init__(self):
        self.id = None
        self.code = None
        self.name = None


class HeartAttackFeatureGroups(object):
    """ Список групп признаков """
    def __init__(self):
        self._groups = []

    @property
    def groups(self) -> List[HeartAttackFeatureGroup]:
        """ """
        return self._groups


def load_heart_attack_feature_groups(path: str) -> HeartAttackFeatureGroups:
    """ """
    result = HeartAttackFeatureGroups()

    with open(path, "rt") as f:
        reader = csv.reader(f, delimiter=",")
        next(reader, None)  # скипаем первую запись
        for row in reader:
            group = HeartAttackFeatureGroup()
            group.id = int(row[0])
            group.code = row[1]
            group.name = row[2]
            result.groups.append(group)

    return result

##################################################################################


def get_heart_attack_features() -> List[HeartAttackFeature]:
    """ """
    global HEART_ATTACK_FEATURES

    if HEART_ATTACK_FEATURES is None:
        path = "feature.csv"
        HEART_ATTACK_FEATURES = load_heart_attack_features(path=path)

    return HEART_ATTACK_FEATURES


class HeartAttackFeaturesGroupPack(object):

    __shared_state = {
        "_groups": None
    }

    def __init__(self):
        self.__dict__ = self.__shared_state

    @property
    def groups(self) -> List[HeartAttackFeatureGroup]:
        return self._groups


def get_heart_attack_feature_groups() -> List[HeartAttackFeatureGroup]:

    pack = HeartAttackFeaturesGroupPack()

    if pack.groups is None:
        # пытаемся загрузить группы
        path = "feature_group.csv"
        pack._groups = load_heart_attack_feature_groups(path=path)

    return pack.groups


if __name__ == '__main__':

    input_features = FEATURES_INPUT

    """
    features = load_heart_attack_features("feature.csv")
    groups = load_heart_attack_feature_groups("feature_group.csv")

    for f in features.features:
        print(f.name, f.id, f.code, f.group_code)

    for g in groups.groups:
        print(g.name, g.id, g.code)
    """

    FeaturesDF = pd.read_csv("feature.csv", delimiter=",")
    FeatureGroupsDF = pd.read_csv("feature_group.csv", delimiter=",")
    # print(DfFeatures[['id', 'code', 'name', 'feature_group_id']])
    # print(FeatureGroupsDF[['id', 'code', 'name']])
    # print(DfFeatures[DfFeatures['code'] == input_features[0]])
    # for f in DfFeatures.values: print(f)
    for f in input_features:
        Feature = FeaturesDF[FeaturesDF['code'] == f]
        FeatureGroup = FeatureGroupsDF[FeatureGroupsDF['id'] == int(Feature.feature_group_id)]
        print(f" \"name\": \"{FeatureGroup['name'].values[0]} : {Feature.name.values[0]}\"")
        print("----------------------------")

