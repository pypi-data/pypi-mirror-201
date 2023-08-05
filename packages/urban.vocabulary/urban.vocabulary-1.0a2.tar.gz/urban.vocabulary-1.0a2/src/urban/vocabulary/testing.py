# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from mock import Mock
from Products.urban import UrbanVocabularyTerm
from urban.vocabulary import ws

import os
import urban.vocabulary


class UrbanVocabularyLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        UrbanVocabularyTerm.UrbanVocabulary.getAllVocTerms = Mock(return_value={})
        self.loadZCML(package=urban.vocabulary, name='testing.zcml')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'urban.vocabulary:testing')
        ws.URBAN_CFG_DIR = '{}/../../var/urban'.format(os.getcwd())
        coring_cfg = ws.ExternalConfig('parcel_coring')
        coring_polygon = ws.ExternalConfig('coring_polygon')
        ws.WS_BASE_URL = coring_cfg.parcel_coring.get('url', '')
        ws.POLYGON = coring_polygon.coring_polygon.get('wkt', '')


URBAN_VOCABULARY_FIXTURE = UrbanVocabularyLayer()


URBAN_VOCABULARY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(URBAN_VOCABULARY_FIXTURE,),
    name='UrbanVocabularyLayer:IntegrationTesting'
)


URBAN_VOCABULARY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(URBAN_VOCABULARY_FIXTURE,),
    name='UrbanVocabularyLayer:FunctionalTesting'
)


URBAN_VOCABULARY_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        URBAN_VOCABULARY_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='UrbanVocabularyLayer:AcceptanceTesting'
)
