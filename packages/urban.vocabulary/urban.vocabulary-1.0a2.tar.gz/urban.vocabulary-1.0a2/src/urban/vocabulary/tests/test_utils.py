# -*- coding: utf-8 -*-
"""
urban.vocabulary
----------------

Created by mpeeters
:copyright: (c) 2016 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from plone.registry.interfaces import IRecord
from plone.registry.interfaces import IRecordsProxy
from zope.interface import alsoProvides
from zope.schema.vocabulary import SimpleVocabulary

import unittest

from urban.vocabulary import utils


class TestUtils(unittest.TestCase):

    def test_vocabulary_from_items(self):
        """Test utils.vocabulary_from_items function"""
        voc = utils.vocabulary_from_items([(1, 'a'), (2, 'b')])
        self.assertEqual(2, len(voc))
        term = voc.getTermByToken('2')
        self.assertEqual(2, term.value)
        self.assertEqual('b', term.title)

    def test_extend_vocabulary(self):
        """Test utils.extend_vocabulary function"""
        vocabulary = SimpleVocabulary([
            SimpleVocabulary.createTerm(1, 1, 'a'),
            SimpleVocabulary.createTerm(2, 2, 'b'),
        ])
        voc = utils.extend_vocabulary(vocabulary, [(3, 'c', '',), (4, 'd', 'e')])
        self.assertEqual(4, len(voc))
        term = voc.getTermByToken('2')
        self.assertEqual(2, term.value)
        self.assertEqual('b', term.title)
        term = voc.getTermByToken('3')
        self.assertEqual(3, term.value)
        self.assertEqual('c', term.title)
        term = voc.getTermByToken('4')
        # if a custom value is defined (e),  it should be used instead the
        # default one (d)
        self.assertEqual('e', term.title)

    def test_to_int(self):
        """Test utils.to_int function"""
        self.assertEqual(2, utils.to_int(2))
        self.assertEqual(2, utils.to_int('2'))
        self.assertEqual(2, utils.to_int(u'2'))
        self.assertEqual('a', utils.to_int('a'))

    def test_to_str(self):
        """Test utils.to_str function"""
        self.assertEqual('text.text', utils.to_str('text.\ntext'))
        self.assertEqual('text.text', utils.to_str('text.\n\rtext'))
        self.assertEqual('text.text', utils.to_str('text.\rtext'))
        self.assertEqual('text.text', utils.to_str('text.text'))

    def test_is_registry_context(self):
        """Test utils.is_registry_context function"""
        obj = type('obj', (object, ), {})()
        self.assertFalse(utils.is_registry_context(obj))
        alsoProvides(obj, IRecord)
        self.assertTrue(utils.is_registry_context(obj))

        obj2 = type('obj', (object, ), {})()
        alsoProvides(obj2, IRecordsProxy)
        self.assertTrue(utils.is_registry_context(obj2))
        alsoProvides(obj2, IRecord)
        self.assertTrue(utils.is_registry_context(obj2))
