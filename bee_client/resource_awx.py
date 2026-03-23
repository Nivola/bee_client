# SPDX-License-Identifier: EUPL-1.2
#
# (C) Copyright 2018-2026 CSI-Piemonte

from .client import CmpBaseService
from .resource import CmpResourceAbstractService


class CmpResourceAwxService(CmpResourceAbstractService):
    """Cmp resource awx service"""

    def __init__(self, manager):
        CmpBaseService.__init__(self, manager)
        self.project = CmpResourceAwxProjectService(self.manager)


class CmpResourceAwxAbstractService(CmpResourceAbstractService):
    """Cmp resource awx service"""
    pass


class CmpResourceAwxProjectService(CmpResourceAwxAbstractService):
    """Cmp resource awx volume service"""

    def list(self, *args, **kwargs):
        """get projects

        :param container: container id or uuid
        :param name: entity name
        :param desc: entity description
        :param objid: entity authorization id
        :param ext_id: entity ext_id
        :param state: entity state
        :param attributes: entity attributes
        :param tags: comma separated list of tags
        :param page: query page
        :param size: query page size
        :param field: query sort field
        :param order: query sort order
        :return: list of entities
        :raise CmpApiClientError:
        """
        params = [
            "container",
            "name",
            "desc",
            "objid",
            "ext_id",
            "state",
            "tags",
            "attribute",
        ]
        mappings = {
            "name": lambda n: "%" + n + "%",
            "attribute": lambda n: "%" + n + "%"
        }
        data = self.format_paginated_query(kwargs, params, mappings=mappings)
        uri = self.get_uri("awx/projects", preferred_version=self.VERSION, **kwargs)
        res = self.api_get(uri, data=data)
        self.logger.debug("get awx projects: %s", res)
        return res

    def get(self, oid, **kwargs):
        """get project

        :param oid: project id or uuid
        :return: entity
        :raise CmpApiClientError:
        """
        uri = self.get_uri(f"awx/projects/{oid}", preferred_version=self.VERSION, **kwargs)
        res = self.api_get(uri)
        self.logger.debug("get awx project %s: %s", oid, res)
        return res
