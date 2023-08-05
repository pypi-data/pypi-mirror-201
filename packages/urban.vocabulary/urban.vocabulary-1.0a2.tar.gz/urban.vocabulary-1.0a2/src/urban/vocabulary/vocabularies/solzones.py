# -*- coding: utf-8 -*-
"""
urban.vocabulary
------------------

Created by mpeeters
:license: GPL, see LICENCE.txt for more details.
"""

from urban.vocabulary.vocabularies.base import BaseVocabulary
from urban.vocabulary.vocabularies.base import BaseBooleanVocabulary


class SOLZonesVocabulary(BaseVocabulary):
    config_vocabulary_path = u'solzones'
    config_vocabulary_options = {
        'inUrbanConfig': False,
    }
    registry_key = 'sol'


class SOLZonesBooleanVocabulary(SOLZonesVocabulary, BaseBooleanVocabulary):
    pass
