"""
Date created: 1/13/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Contributors: 
    https://github.com/josephedradan

Reference:

"""
from typing import Type
from typing import Union

from pacman.feature_extractor_coordiate.feature_extractor_coordinate import CoordinateExtractor
from pacman.feature_extractor_coordiate.feature_extractor_identity import IdentityExtractor
from pacman.feature_extractor_coordiate.feature_extractor_simple import SimpleExtractor
from pacman.feature_extractor_coordiate.feature_extrator import FeatureExtractor

LIST_SUBCLASS_FEATURE_EXTRACTOR = [
    CoordinateExtractor,
    IdentityExtractor,
    SimpleExtractor,
]

DICT_K_NAME_SUBCLASS_FEATURE_EXTRACTOR_V_SUBCLASS_FEATURE_EXTRACTOR = {
    subcless_feature_extractor_.__name__: subcless_feature_extractor_
    for subcless_feature_extractor_ in LIST_SUBCLASS_FEATURE_EXTRACTOR
}


def get_subclass_feature_extractor(name_feature_extractor: Union[str, Type[FeatureExtractor], None]) -> Type[FeatureExtractor]:
    feature_extractor = name_feature_extractor

    if isinstance(name_feature_extractor, str):
        feature_extractor = DICT_K_NAME_SUBCLASS_FEATURE_EXTRACTOR_V_SUBCLASS_FEATURE_EXTRACTOR.get(
            name_feature_extractor
        )

    if feature_extractor is None:
        raise Exception("{} is not a valid feature extractor".format(name_feature_extractor))

    return feature_extractor
