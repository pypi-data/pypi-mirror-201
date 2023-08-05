# -*- coding: utf-8 -*-
"""
urban.vocabulary
------------------

Created by mpeeters
:license: GPL, see LICENCE.txt for more details.
"""

from plone.registry.interfaces import IRecord
from plone.registry.interfaces import IRecordsProxy
from time import time
from zope.schema.vocabulary import SimpleVocabulary


def vocabulary_from_items(items):
    """
    Create a zope.schema vocabulary from a list of tuple e.g.
    [('value1', 'title1'), ('value2', 'title2')]
    """
    return SimpleVocabulary(
        [SimpleVocabulary.createTerm(item[0], item[0], item[1])
         for item in items],
    )


def extend_vocabulary(voc, items):
    """Add new terms to an existing vocabulary"""
    for value, title, custom in items:
        if value in voc.by_token or value in voc.by_value:
            continue
        term = SimpleVocabulary.createTerm(value, value, custom or title)
        voc._terms.append(term)
        voc.by_token[term.token] = term
        voc.by_value[term.value] = term
    return voc


def to_int(str):
    """Convert a string to an integer if that is possible"""
    try:
        return int(str)
    except ValueError:
        return str


def to_str(str):
    """Convert a string to zope schema TextLine value"""
    invalid_chars = ('\n', '\r')
    for char in invalid_chars:
        str = str.replace(char, '')
    return str


def is_registry_context(context):
    """Verify if the given context match a registry record"""
    if IRecordsProxy.providedBy(context) or IRecord.providedBy(context):
        return True
    return False


def time_now():
    """Return current time"""
    return time()
