# -*- coding: utf-8 -*-

from plone import api

from urban.vocabulary.vocabularies.base import BaseVocabulary
from urban.vocabulary.vocabularies.base import BaseBooleanVocabulary
from urban.vocabulary import utils
from urban.vocabulary import _

from zope.i18n import translate


class CatchmentAreaVocabulary(BaseVocabulary):
    registry_key = 'catchment_area'

    def _get_base_vocabulary(self, context):
        """
          This vocabulary for field catchmentArea returns a list of
          catchment areas : close prevention area, far prevention area,
          supervision area or outside catchment
        """
        portal = api.portal.get()
        vocab = (
            ('close', translate(_('close_prevention_area'), context=portal.REQUEST)),
            ('far', translate(_('far_prevention_area'), context=portal.REQUEST)),
            ('supervision', translate(_('supervision_area'), context=portal.REQUEST)),
            ('ouside', translate(_('outside_catchment'), context=portal.REQUEST)),
        )
        return utils.vocabulary_from_items(vocab)


class CatchmentAreaBooleanVocabulary(CatchmentAreaVocabulary,
                                     BaseBooleanVocabulary):
    pass
