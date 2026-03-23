# SPDX-License-Identifier: EUPL-1.2
#
# (C) Copyright 2018-2026 CSI-Piemonte

from .business import CmpBusinessAbstractService
from .client import CmpBaseService, CmpApiManager


class CmpBusinessCapabilityService(CmpBusinessAbstractService):
    """Cmp business capability"""

    def __init__(self, manager: CmpApiManager):
        CmpBaseService.__init__(self, manager)

    def list(self, *args, **kwargs):
        """get capabilities

        :param id: capability id
        :param objid: capability objid
        :param page: query page
        :param size: query page size
        :param field: query sort field
        :param order: query sort order
        :param objid: authorization id
        :return: list of capabilities
        :raise CmpApiClientError:
        """
        params = ["id", "objid"]
        aliases = {}
        mappings = {}
        data = self.format_paginated_query(kwargs, params, mappings=mappings, aliases=aliases)
        uri = self.get_uri("capabilities")
        res = self.api_get(uri, data=data)
        self.logger.debug("get capabilities: %s", res)
        return res

    def get(self, oid):
        """get capability

        :param oid: capability id or uuid
        :return: capability
        :raise CmpApiClientError:
        """
        uri = self.get_uri(f"capabilities/{oid}")
        res = self.api_get(uri).get("capability")
        self.logger.debug("get capability %s: %s", oid, res)
        return res

    def delete(self, oid):
        """Delete capability

        :param oid: id of the capability
        :return:
        :raises CmpApiClientError: raise :class:`CmpApiClientError`
        """
        uri = self.get_uri(f"capabilities/{oid}")
        data = ""
        self.api_delete(uri, data=data)
        self.logger.debug("delete capability %s", oid)
