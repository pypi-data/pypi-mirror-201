# -*- coding: utf-8 -*-
"""
urban.vocabulary
----------------

Created by mpeeters
:copyright: (c) 2016 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from mock import Mock
from plone import api

import unittest

from urban.vocabulary import utils
from urban.vocabulary import testing
from urban.vocabulary import ws
from urban.vocabulary.vocabularies import base


class FakeUrbanVocabulary(object):

    def __init__(*args, **kwargs):
        pass

    def getAllVocTerms(context):
        pass


class TestVocabulary(base.BaseVocabulary):
    registry_key = 'pca'
    config_vocabulary_path = u'pcazones'
    config_vocabulary_options = {
        'inUrbanConfig': False,
    }
    _expire_delay = 10000


class TestBooleanVocabulary(TestVocabulary, base.BaseBooleanVocabulary):
    pass


class TestBaseVocabulary(unittest.TestCase):
    layer = testing.URBAN_VOCABULARY_INTEGRATION_TESTING
    _now = 1500000000

    def setUp(self):
        self._time_now = utils.time_now
        self._get_registry_record = api.portal.get_registry_record
        utils.time_now = Mock(return_value=self._now)
        api.portal.set_registry_record(
            'urban.vocabulary.interfaces.IVocabularies.pca_cached',
            [[u'key1', u'value1', u'', u'1'], [u'key2', u'value2', u'', u'1']],
        )

    def tearDown(self):
        utils.time_now = self._time_now
        api.portal.get_registry_record = self._get_registry_record

    @property
    def _instance(self):
        """Return a BaseVocabulary instance"""
        return TestVocabulary()

    def test_call(self):
        """Test BaseVocabulary.__call__ method"""

    def test_get_base_vocabulary(self):
        """Test BaseVocabulary._get_base_vocabulary method"""
        voc = self._instance
        values = [
            type('obj', (object, ), {'id': u'key1', 'title': u'Title 1'})(),
            type('obj', (object, ), {'id': u'key2', 'title': u'Title 2'})(),
        ]
        voc._get_config_vocabulary_values = Mock(return_value=values)
        base_voc = voc._get_base_vocabulary(None)
        self.assertEqual(2, len(base_voc))
        self.assertEqual([u'key1', u'key2'], [t.token for t in base_voc])

    def test_get_registry_items_not_existing_record(self):
        """Test BaseVocabulary._get_registry_items method"""
        voc = self._instance
        api.portal.get_registry_record = Mock(return_value=None)
        voc._refresh_registry = Mock(return_value=None)
        self.assertEqual([], voc._get_registry_items(None))
        self.assertFalse(voc._refresh_registry.called)

    def test_get_registry_items_existing_record(self):
        voc = self._instance
        voc._refresh_registry = Mock(return_value=None)
        self.assertEqual(
            [(u'key1', u'value1', u''), (u'key2', u'value2', u'')],
            voc._get_registry_items(None),
        )
        self.assertTrue(voc._refresh_registry.called)

    def test_get_registry_items_disabled_record(self):
        # disable the first record (u'0')
        api.portal.set_registry_record(
            'urban.vocabulary.interfaces.IVocabularies.pca_cached',
            [[u'key1', u'value1', u'', u'0'], [u'key2', u'value2', u'', u'1']],
        )
        voc = self._instance
        voc._refresh_registry = Mock(return_value=None)
        self.assertEqual(
            [(u'key2', u'value2', u'')],
            voc._get_registry_items(None),
        )
        self.assertTrue(voc._refresh_registry.called)

    def test_get_registry_items_all_records(self):
        # disable the first record (u'0')
        api.portal.set_registry_record(
            'urban.vocabulary.interfaces.IVocabularies.pca_cached',
            [[u'key1', u'value1', u'', u'0'], [u'key2', u'value2', u'', u'1']],
        )
        voc = self._instance
        voc._refresh_registry = Mock(return_value=None)
        # return the disabled elements when 'all' paramater is True
        self.assertEqual(
            [(u'key1', u'value1', u''), (u'key2', u'value2', u'')],
            voc._get_registry_items(None, all=True),
        )
        self.assertTrue(voc._refresh_registry.called)

    def test_set_delay_key(self):
        """Test BaseVocabulary.set_delay_key class method"""
        voc = self._instance
        voc.set_delay_key()
        self.assertEqual(self._now // 10000, voc._delay_key)

    def test_get_delay_key(self):
        """Test BaseVocabulary._get_delay_key class method"""
        voc = self._instance
        voc.set_delay_key()
        self.assertEqual(self._now // 10000, voc._get_delay_key())

    def test_verify_delay(self):
        """Test BaseVocabulary.verify_delay class method"""
        voc = self._instance
        voc.set_delay_key()
        self.assertFalse(voc.verify_delay())
        utils.time_now = Mock(return_value=self._now + 9999)  # Delay is 10000
        self.assertFalse(voc.verify_delay())
        utils.time_now = Mock(return_value=self._now + 10000)
        self.assertTrue(voc.verify_delay())

    def test_refresh_registry_function(self):
        """Test refresh_registry function"""
        voc = self._instance
        voc.verify_delay = Mock(return_value=False)
        ws.UrbanWebservice.store_values = Mock(return_value=False)
        base.refresh_registry(None, None, voc)
        self.assertFalse(ws.UrbanWebservice.store_values.called)

        voc.verify_delay = Mock(return_value=True)
        voc.set_delay_key = Mock(return_value=None)
        base.refresh_registry(None, None, voc)
        self.assertTrue(ws.UrbanWebservice.store_values.called)
        self.assertFalse(voc.set_delay_key.called)

        ws.UrbanWebservice.store_values = Mock(return_value=True)
        base.refresh_registry(None, None, voc)
        self.assertTrue(voc.set_delay_key.called)


class TestBaseBooleanVocabulary(unittest.TestCase):
    layer = testing.URBAN_VOCABULARY_INTEGRATION_TESTING
    _now = 1500000000

    def setUp(self):
        self._get_registry_record = api.portal.get_registry_record
        api.portal.set_registry_record(
            'urban.vocabulary.interfaces.IVocabularies.pca_cached',
            [[u'key1', u'value1', u'1'], [u'key2', u'value2', u'1']],
        )

    def tearDown(self):
        api.portal.get_registry_record = self._get_registry_record

    def test_generate_vocabulary_with_default_value(self):
        """
        Test BaseBooleanVocabulary._generate_vocabulary method
        when there is a default value
        """
        vocabulary = TestBooleanVocabulary()
        base_vocabulary = utils.vocabulary_from_items([
            ('value1', 'title1'),
            ('value2', 'title2'),
        ])
        api.portal.get_registry_record = Mock(side_effect=(None, True))
        voc = vocabulary._generate_vocabulary(base_vocabulary)
        self.assertEqual(2, len(voc))
        self.assertEqual(True, voc.getTermByToken('value1').title)
        self.assertEqual(True, voc.getTermByToken('value2').title)

        api.portal.get_registry_record = Mock(side_effect=(None, False))
        voc = vocabulary._generate_vocabulary(base_vocabulary)
        self.assertEqual(2, len(voc))
        self.assertEqual(False, voc.getTermByToken('value1').title)
        self.assertEqual(False, voc.getTermByToken('value2').title)

    def test_generate_vocabulary_with_mapping(self):
        """
        Test BaseBooleanVocabulary._generate_vocabulary method
        when there is mapping keys
        """
        vocabulary = TestBooleanVocabulary()
        base_vocabulary = utils.vocabulary_from_items([
            ('value1', 'title1'),
            ('value2', 'title2'),
        ])
        api.portal.get_registry_record = Mock(side_effect=(['value1'], True))
        voc = vocabulary._generate_vocabulary(base_vocabulary)
        self.assertEqual(2, len(voc))
        self.assertEqual(True, voc.getTermByToken('value1').title)
        self.assertEqual(False, voc.getTermByToken('value2').title)
