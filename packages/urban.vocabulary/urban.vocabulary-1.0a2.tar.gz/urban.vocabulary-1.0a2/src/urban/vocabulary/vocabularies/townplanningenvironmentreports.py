# -*- coding: utf-8 -*-
"""
urban.vocabulary
------------------

Created by mpeeters
:license: GPL, see LICENCE.txt for more details.
"""

from urban.vocabulary.vocabularies.base import BaseVocabulary
from urban.vocabulary.vocabularies.base import BaseBooleanVocabulary


class TownPlanningEnvironmentReportsVocabulary(BaseVocabulary):
    config_vocabulary_path = None
    config_vocabulary_options = {}
    registry_key = 'town_planning_environment_reports'


class TownPlanningEnvironmentReportsBooleanVocabulary(
        TownPlanningEnvironmentReportsVocabulary, BaseBooleanVocabulary):
    pass
