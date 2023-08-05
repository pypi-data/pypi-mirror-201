# -*- coding: utf-8 -*-

from urban.vocabulary.vocabularies.base import BaseVocabulary
from urban.vocabulary.vocabularies.base import BaseBooleanVocabulary


class UrbanRevivalVocabulary(BaseVocabulary):
    config_vocabulary_path = u'prevu'
    config_vocabulary_options = {
        'inUrbanConfig': False,
    }
    registry_key = 'urban_revival'


class UrbanRevivalBooleanVocabulary(UrbanRevivalVocabulary,
                                    BaseBooleanVocabulary):
    pass
