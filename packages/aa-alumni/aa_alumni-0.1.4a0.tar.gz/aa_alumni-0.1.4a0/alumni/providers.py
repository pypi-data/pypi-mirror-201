from esi.clients import esi_client_factory

from . import __version__

"""
Swagger spec operations:
get_corporations_corporation_id_alliancehistory
get_characters_character_id_corporationhistory
"""


class EsiResponseClient:
    def __init__(self, token=None):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = esi_client_factory(app_info_text="AA Alumni v" + __version__,)
        return self._client


esi = EsiResponseClient()
