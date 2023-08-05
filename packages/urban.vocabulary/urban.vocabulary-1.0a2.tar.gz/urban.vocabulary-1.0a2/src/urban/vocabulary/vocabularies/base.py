# -*- coding: utf-8 -*-
"""
urban.vocabulary
------------------

Created by mpeeters
:license: GPL, see LICENCE.txt for more details.
"""

from Products.urban import UrbanVocabularyTerm
from datetime import datetime
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.async.interfaces import IAsyncService
from zope.component import getUtility
from zope.component.interfaces import ComponentLookupError

import copy

from urban.vocabulary import utils
from urban.vocabulary import ws
from urban.vocabulary.interfaces import ISettings


class BaseVocabulary(object):
    config_vocabulary_path = None
    config_vocabulary_options = {}
    # See Products.Urban.UrbanVocabularyTerm.UrbanVocabulary for options
    registry_key = None
    _registry_interface = 'urban.vocabulary.interfaces.IVocabularies'
    _expire_delay = 86400  # in seconds

    def __call__(self, context, all=False):
        vocabulary = self._get_base_vocabulary(context)
        if self.registry_key:
            vocabulary = utils.extend_vocabulary(
                vocabulary,
                self._get_registry_items(context, all=all),
            )
        return vocabulary

    def _get_base_vocabulary(self, context):
        urban_vocabulary_values = self._get_config_vocabulary_values(context)
        return self._vocabulary_from_urban_vocabulary(
            urban_vocabulary_values,
            context,
        )

    @staticmethod
    def get_licence_config_ids():
        return [b.id for b in api.content.find(portal_type='LicenceConfig')]

    @classmethod
    def _get_config_vocabulary_values(cls, context):
        """Return the vocabulary values created from urban config"""
        if not cls.config_vocabulary_path:
            return []
        options = copy.deepcopy(cls.config_vocabulary_options)
        in_urban_config = cls.config_vocabulary_options.get(
            'inUrbanConfig',
            False,
        )
        values = []
        vocabularies = []
        if utils.is_registry_context(context) and in_urban_config:
            options['inUrbanConfig'] = False
            for licence_id in cls.get_licence_config_ids():
                vocabularies.append(UrbanVocabularyTerm.UrbanVocabulary(
                    '{0}/{1}'.format(licence_id, cls.config_vocabulary_path),
                    **options
                ))
        else:
            vocabularies.append(UrbanVocabularyTerm.UrbanVocabulary(
                cls.config_vocabulary_path,
                **cls.config_vocabulary_options
            ))

        for voc in vocabularies:
            try:
                values.extend(voc.getAllVocTerms(context).values())
            except InvalidParameterError:
                # This may happen during import steps when `portal_urban`
                # is not created yet
                pass
        return values

    def _get_registry_items(self, context, all=False):
        key = '{0}.{1}_cached'.format(
            self._registry_interface,
            self.registry_key,
        )
        record = api.portal.get_registry_record(key, default=None)
        if record is not None:
            self._refresh_registry()
        return [(e[0], e[1], e[2]) for e in record and record or [] if e and (all or int(e[3]))]

    def _vocabulary_from_urban_vocabulary(self, urban_values, context):
        """Convert an urban vocabulary to a zope.schema vocabulary"""
        items = set([(t.id, t.title or t.Title()) for t in urban_values])
        return utils.vocabulary_from_items(items)

    def _refresh_registry(self):
        """Refresh (if necessary) the values stored in the registry"""
        async = get_async()
        portal = api.portal.get()
        if async:
            async.queueJob(
                refresh_registry,
                portal,
                self.registry_key,
                self.__class__,
            )
        else:
            refresh_registry(portal, self.registry_key, self.__class__)

    @classmethod
    def set_delay_key(cls):
        cls._delay_key = utils.time_now() // cls._expire_delay

    @classmethod
    def _get_delay_key(cls):
        return getattr(cls, '_delay_key', None)

    @classmethod
    def verify_delay(cls):
        """Verify if there is a delay and if it expired"""
        time = utils.time_now()
        return getattr(cls, '_delay_key', None) != time // cls._expire_delay


class BaseBooleanVocabulary(BaseVocabulary):

    def __call__(self, context, all=False):
        vocabulary = super(BaseBooleanVocabulary, self).__call__(context, all=all)
        return self._generate_vocabulary(vocabulary)

    def _generate_vocabulary(self, base_vocabulary):
        keys, value = self.boolean_mapping
        other_value = not value
        if len(keys) == 0:
            items = [(t.value, value) for t in base_vocabulary]
        else:
            items = [(t.value, t.value in keys and value or other_value)
                     for t in base_vocabulary]
        return utils.vocabulary_from_items(items)

    def _get_settings_field(self, key):
        """Return a field object from ISettings class"""
        classes = ISettings.getBases() + (ISettings, )
        for cls in classes:
            if key in cls.names():
                return cls.get(key)
        raise KeyError("Missing key '{0}' in {1}".format(key, cls))

    @property
    def boolean_mapping(self):
        mapping_keys = api.portal.get_registry_record(
            '{0}_boolean_mapping'.format(self.registry_key),
            interface=ISettings,
            default=None,
        ) or []
        key = '{0}_boolean_mapping_value'.format(self.registry_key)
        field = self._get_settings_field(key)
        mapping_value = api.portal.get_registry_record(
            key,
            interface=ISettings,
            default=None,
        )
        if mapping_value is None:
            mapping_value = field.default
        if mapping_value is None:  # This should normally never happen
            mapping_value = True
        return mapping_keys, mapping_value


def refresh_registry(context, registry_key, cls):
    if cls.verify_delay() is True:
        ws_instance = ws.UrbanWebservice(registry_key)
        result = ws_instance.store_values()
        if result is True:
            cls.set_delay_key()


def get_async():
    """Ensure that the async worker is running and return it"""
    async = getUtility(IAsyncService)
    try:
        queues = async.getQueues()
        queue = queues['']
        if len(queue) > 0:
            message_date = queue[0]._begin_after.replace(tzinfo=None)
            msg_duration = datetime.utcnow() - message_date
            if msg_duration.total_seconds() > 60:
                return
    except KeyError:  # No worker declared
        return
    except ComponentLookupError:  # Missing configuration in instance
        return
    return async
