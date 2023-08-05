# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from urban.vocabulary.testing import URBAN_VOCABULARY_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that urban.vocabulary is properly installed."""

    layer = URBAN_VOCABULARY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if urban.vocabulary is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'urban.vocabulary'))

    def test_browserlayer(self):
        """Test that IUrbanVocabularyLayer is registered."""
        from urban.vocabulary.interfaces import (
            IUrbanVocabularyLayer)
        from plone.browserlayer import utils
        self.assertIn(IUrbanVocabularyLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = URBAN_VOCABULARY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['urban.vocabulary'])

    def test_product_uninstalled(self):
        """Test if urban.vocabulary is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'urban.vocabulary'))

    def test_browserlayer_removed(self):
        """Test that IUrbanVocabularyLayer is removed."""
        from urban.vocabulary.interfaces import IUrbanVocabularyLayer
        from plone.browserlayer import utils
        self.assertNotIn(IUrbanVocabularyLayer, utils.registered_layers())
