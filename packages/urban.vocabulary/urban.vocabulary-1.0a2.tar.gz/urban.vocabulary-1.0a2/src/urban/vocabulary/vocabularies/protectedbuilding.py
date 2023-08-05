# -*- coding: utf-8 -*-
"""
urban.vocabulary
------------------

Created by mpeeters
:license: GPL, see LICENCE.txt for more details.
"""

from urban.vocabulary.vocabularies.base import BaseVocabulary
from urban.vocabulary.vocabularies.base import BaseBooleanVocabulary


class ProtectedBuildingVocabulary(BaseVocabulary):
    config_vocabulary_path = u'folderprotectedbuildings'
    config_vocabulary_options = {
        'inUrbanConfig': False,
    }
    registry_key = 'protected_building'


class ProtectedBuildingBooleanVocabulary(ProtectedBuildingVocabulary,
                                         BaseBooleanVocabulary):
    pass
