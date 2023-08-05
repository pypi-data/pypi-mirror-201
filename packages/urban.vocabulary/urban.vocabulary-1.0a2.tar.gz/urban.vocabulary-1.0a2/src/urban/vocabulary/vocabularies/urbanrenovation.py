# -*- coding: utf-8 -*-

from urban.vocabulary.vocabularies.base import BaseVocabulary
from urban.vocabulary.vocabularies.base import BaseBooleanVocabulary


class UrbanRenovationVocabulary(BaseVocabulary):
    config_vocabulary_path = u'prenu'
    config_vocabulary_options = {
        'inUrbanConfig': False,
    }
    registry_key = 'urban_renovation'


class UrbanRenovationBooleanVocabulary(UrbanRenovationVocabulary,
                                       BaseBooleanVocabulary):
    pass
