# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from urban.vocabulary.testing import URBAN_VOCABULARY_INTEGRATION_TESTING
from urban.vocabulary.vocabularies.catchmentarea import CatchmentAreaVocabulary
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that urban.vocabulary is properly installed."""

    layer = URBAN_VOCABULARY_INTEGRATION_TESTING

    def setUp(self):
        # set language to 'fr' as we do some translations above
        ltool = api.portal.get_tool('portal_languages')
        defaultLanguage = 'fr'
        supportedLanguages = ['en', 'fr']
        ltool.manage_setLanguageSettings(defaultLanguage, supportedLanguages, setUseCombinedLanguageCodes=False)
        # this needs to be done in tests for the language to be taken into account...
        ltool.setLanguageBindings()

    def test_CatchmentAreaVocabulary_custom_base_vocabulary(self):
        """"""
        portal = api.portal.get()
        catchmentarea_voc = CatchmentAreaVocabulary()
        expected = [
            u"Zone de prévention éloignée",
            u"Zone de prévention rapprochée",
            u"Zone de surveillance",
            u"Hors captage",
        ]
        base_vocab = catchmentarea_voc._get_base_vocabulary(portal)
        returned = [t.title for t in base_vocab.by_token.values()]
        self.assertEquals(returned, expected)
