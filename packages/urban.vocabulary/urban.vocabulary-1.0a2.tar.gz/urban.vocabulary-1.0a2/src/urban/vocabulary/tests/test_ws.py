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

import requests
import unittest

from urban.vocabulary import ws
from urban.vocabulary import testing


class TestUrbanWebservice(unittest.TestCase):
    layer = testing.URBAN_VOCABULARY_INTEGRATION_TESTING
    _rkey = 'urban.vocabulary.interfaces.IVocabularies.pca_cached'

    @property
    def _cls(self):
        cls = ws.UrbanWebservice('pca')
        return cls

    def tearDown(self):
        api.portal.set_registry_record(self._rkey, [])

    @staticmethod
    def _request_result(code, json={'success': True}):
        def json_method(self):
            return json
        return type('response', (object, ), {
            'status_code': code,
            'json': json_method,
        })()

    def test_get_registry_value(self):
        """Test UrbanWebservice.get_registry_value method"""
        cls = self._cls
        self.assertEqual(
            '{}l=7&att=LIBELLE,CODECARTO',
            cls.get_registry_value('url'),
        )
        self.assertIsNone(cls.get_registry_value('foo'))
        self.assertEqual('FOO', cls.get_registry_value('foo', default='FOO'))

    def test_ws_url(self):
        """Test UrbanWebservice.ws_url property"""
        cls = self._cls
        cls.get_registry_value = Mock(return_value='{}a')
        self.assertListEqual(
            ['https://xxx-geonode.imio-app.be/survey/survey_value_list?a'],
            cls.ws_url
        )
        cls.get_registry_value = Mock(return_value=['{}a', 'b'])
        self.assertListEqual(
            [
                'https://xxx-geonode.imio-app.be/survey/survey_value_list?a',
                'b'
            ],
            cls.ws_url
        )

    def test_call_ws_missing_url(self):
        """Test UrbanWebservice._call_ws method when there is no url"""
        cls = self._cls
        cls.get_registry_value = Mock(return_value=None)
        self.assertIsNone(cls._call_ws(force=0))

    def test_call_ws_server_error(self):
        """Test UrbanWebservice._call_ws method when the geo server return an
        http error"""
        cls = self._cls
        urls = ['https://a.com?p=1', 'https://b.com?p=1']
        cls.get_registry_value = Mock(return_value=urls)
        requests.post = Mock(side_effect=[
            self._request_result(200),
            self._request_result(500),
        ])
        self.assertIsNone(cls._call_ws(force=0))

    def test_call_ws_not_success(self):
        """Test UrbanWebservice._call_ws method when the geo server return an
        handled error"""
        cls = self._cls
        urls = ['https://a.com?p=1', 'https://b.com?p=1']
        cls.get_registry_value = Mock(return_value=urls)
        requests.post = Mock(side_effect=[
            self._request_result(200),
            self._request_result(200, {'success': False}),
        ])
        self.assertIsNone(cls._call_ws(force=0))

    def test_call_ws_normal(self):
        """Test UrbanWebservice._call_ws method"""
        cls = self._cls
        urls = ['https://a.com?p=1', 'https://b.com?p=2']
        cls.get_registry_value = Mock(return_value=urls)
        requests.post = Mock(side_effect=[
            self._request_result(200, {'success': True, 'a': 1}),
            self._request_result(200, {'success': True, 'b': 2}),
        ])
        self.assertListEqual(
            [({'area': 'Polygon ((x, y, z))', 'p': ['1']}, {'success': True, 'a': 1}),
             ({'area': 'Polygon ((x, y, z))', 'p': ['2']}, {'success': True, 'b': 2})],
            cls._call_ws(force=0),
        )

    def test_call_ws_cached(self):
        """Test UrbanWebservice._call_ws method cache key"""
        cls = self._cls
        urls = ['https://a.com?p=1', 'https://b.com?p=2']
        cls.get_registry_value = Mock(return_value=urls)
        requests.post = Mock(return_value=self._request_result(200))
        result = [
            ({'area': 'Polygon ((x, y, z))', 'p': ['1']}, {'success': True}),
            ({'area': 'Polygon ((x, y, z))', 'p': ['2']}, {'success': True}),
        ]
        self.assertListEqual(result, cls._call_ws(force=0))
        requests.post = Mock(return_value=self._request_result(500))
        self.assertListEqual(result, cls._call_ws(force=0))

        self.assertIsNone(cls._call_ws(force=1))

    def test_map_result(self):
        """Test UrbanWebservice._map_result method"""
        cls = self._cls
        cls.get_registry_value = Mock(side_effect=['b', 'a'])
        json = {'result': {'features': [
            {'a': 'Token 1', 'b': 'Title 1'},
            {'a': 'Token 2', 'b': 'Title 2'},
        ]}}
        mapping = {'title': 'b', 'token': 'a'}
        self.assertListEqual(
            [['token-1', 'Title 1', u'', u'1'], ['token-2', 'Title 2', u'', u'1']],
            cls._map_result(json, mapping),
        )

    def test_format_title(self):
        """Test UrbanWebservice._format_title method"""
        self.assertEqual('str', self._cls._format_title('  str'))
        self.assertEqual('str', self._cls._format_title('str  '))
        self.assertEqual('str', self._cls._format_title('  str  '))

    def test_store_value_normal(self):
        """Test UrbanWebservice.store_values method"""
        cls = self._cls
        cls._call_ws = Mock(return_value=[
            ({'att': ['A,B']}, {}), ({'att': ['A,B']}, {}),
        ])
        cls._map_result = Mock(side_effect=[
            [[u'token-1', u'Title 1', u'', u'1'], [u'token-2', u'Title 2', u'', u'1']],
            [[u'token-3', u'Title 3', u'', u'1'], [u'token-4', u'Title 4', u'', u'1']],
        ])
        self.assertTrue(cls.store_values())
        data = api.portal.get_registry_record(self._rkey)
        self.assertEqual(4, len(data))
        self.assertListEqual(
            [u'token-1', u'token-2', u'token-3', u'token-4'],
            [r[0] for r in data],
        )

    def test_store_value_no_result(self):
        """Test UrbanWebservice.store_values when there is not result"""
        cls = self._cls
        cls._call_ws = Mock(return_value=[])
        self.assertFalse(cls.store_values())
        data = api.portal.get_registry_record(self._rkey)
        self.assertEqual([[]], data)

    def test_store_value_error(self):
        """Test UrbanWebservice.store_values when the _map_result method raise
        and error"""
        cls = self._cls
        cls._call_ws = Mock(return_value=[({'att': ['A,B']}, {})])
        cls._map_result = Mock(side_effect=KeyError())
        self.assertFalse(cls.store_values())
        data = api.portal.get_registry_record(self._rkey)
        self.assertEqual([[]], data)

    def test_convert_value(self):
        """Test ws.convert_value function"""
        self.assertEqual(['foo'], ws.convert_value('foo'))
        self.assertEqual(['foo'], ws.convert_value(['foo']))
