# -*- coding: utf-8 -*-

from urban.vocabulary.vocabularies.base import BaseVocabulary
from urban.vocabulary.vocabularies.base import BaseBooleanVocabulary


class SARVocabulary(BaseVocabulary):
    registry_key = 'sar'


class SARBooleanVocabulary(SARVocabulary, BaseBooleanVocabulary):
    pass
