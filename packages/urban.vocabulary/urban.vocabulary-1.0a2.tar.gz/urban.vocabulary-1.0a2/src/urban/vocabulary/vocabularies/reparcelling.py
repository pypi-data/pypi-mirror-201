# -*- coding: utf-8 -*-
"""
urban.vocabulary
----------------

Created by mpeeters
:copyright: (c) 2016 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from urban.vocabulary.vocabularies.base import BaseVocabulary
from urban.vocabulary.vocabularies.base import BaseBooleanVocabulary


class ReparcellingVocabulary(BaseVocabulary):
    config_vocabulary_path = u'reparcelling'
    config_vocabulary_options = {
        'inUrbanConfig': False,
    }
    registry_key = 'reparcelling'


class ReparcellingBooleanVocabulary(ReparcellingVocabulary,
                                    BaseBooleanVocabulary):
    pass
