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


class Natura2000Vocabulary(BaseVocabulary):
    config_vocabulary_path = u'natura_2000'
    config_vocabulary_options = {
        'inUrbanConfig': False,
    }
    registry_key = 'natura_2000'


class Natura2000BooleanVocabulary(Natura2000Vocabulary, BaseBooleanVocabulary):
    pass
