from typing import List, Dict
import pandas as pd

HA_FEATURES = None
HA_FEATURE_GROUPS = None

FEATURES_INPUT = ['other_diagnoses__ischemic_heart_disease', 'kbs__characteristic__compressive', 'kbs__characteristic__fully_relief', 'kbs__relief__medicines', 'other_diagnoses__myocardial_infarction', 'bad_habits__alcohol', 'other_symptoms__general_weakness', 'blood_pressure__during_at_checkup', 'blood_pressure__during_at_lifetime', 'kbs__characteristic__occurs_at_physical_activity', 'other_symptoms__dyspnea', 'other_diagnoses__hypertension']


def load_ha_features(path_file: str = "feature.csv") -> pd.DataFrame:
    global HA_FEATURES
    
    if HA_FEATURES is None:
        HA_FEATURES = pd.read_csv(path_file, delimiter=",")
    return HA_FEATURES


def load_ha_feature_groups(path_file: str = "feature_group.csv") -> pd.DataFrame:
    global HA_FEATURE_GROUPS

    if HA_FEATURE_GROUPS is None:
        HA_FEATURE_GROUPS = pd.read_csv(path_file, delimiter=",")
    return HA_FEATURE_GROUPS


def features_verbose(features: List) -> List[Dict[str, str]]:

    all_features = load_ha_features()
    all_groups = load_ha_feature_groups()
    result = []
    for f in features:
        feature = all_features[all_features['code'] == f]
        feature_group = all_groups[all_groups['id'] == int(feature['feature_group_id'])]
        feature_rec = {"code": feature.code.values[0],
                       "name": f'{feature_group.name.values[0]} : {feature.name.values[0]}'
        }
        result.append(feature_rec)
    return result


if __name__ == '__main__':

    input_features = FEATURES_INPUT
    print(features_verbose(input_features))
