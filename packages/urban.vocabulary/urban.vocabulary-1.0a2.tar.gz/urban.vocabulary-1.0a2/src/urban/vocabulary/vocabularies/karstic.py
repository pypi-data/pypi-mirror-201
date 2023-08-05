# -*- coding: utf-8 -*-

from urban.vocabulary.vocabularies.base import BaseVocabulary
from urban.vocabulary.vocabularies.base import BaseBooleanVocabulary


class KarsticVocabulary(BaseVocabulary):
    config_vocabulary_path = u'karst_constraints'
    config_vocabulary_options = {
        'inUrbanConfig': False,
    }
    registry_key = 'karstic'


class KarsticBooleanVocabulary(KarsticVocabulary, BaseBooleanVocabulary):
    pass
