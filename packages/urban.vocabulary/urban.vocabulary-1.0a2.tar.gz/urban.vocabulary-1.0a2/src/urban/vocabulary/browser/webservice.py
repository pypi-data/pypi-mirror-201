# -*- coding: utf-8 -*-
"""
urban.vocabulary
----------------

Created by mpeeters
:license: GPL, see LICENCE.txt for more details.
"""

from Products.Five import BrowserView

from urban.vocabulary.ws import UrbanWebservice


class VocabularyWebserviceView(BrowserView):
    """
    Call a geonode webservice, handle returned values and store them into the
    registry
    """

    def __call__(self):
        ws = UrbanWebservice(self.request.get('registry_key'))
        response = ws.store_values()
        if response is True:
            return 'OK'
        return 'NOK'
