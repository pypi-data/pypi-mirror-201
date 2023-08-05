# -*- coding: utf-8 -*-

from urban.vocabulary.vocabularies.base import BaseVocabulary
from urban.vocabulary.vocabularies.base import BaseBooleanVocabulary


class AreaPlanVocabulary(BaseVocabulary):
    config_vocabulary_path = u'folderzones'
    config_vocabulary_options = {
        'inUrbanConfig': False,
    }
    registry_key = 'area_plan'


class AreaPlanBooleanVocabulary(AreaPlanVocabulary, BaseBooleanVocabulary):
    pass
