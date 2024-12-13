# SPDX-License-Identifier: EUPL-1.2
#
# (C) Copyright 2018-2024 CSI-Piemonte

from beecell.types.type_dict import dict_get
from beecell.types.type_string import truncate
from .client import CmpBaseService
from .resource import CmpResourceAbstractService


class CmpResourceProviderService(CmpResourceAbstractService):
    """Cmp resource provider service"""

    def __init__(self, manager):
        CmpBaseService.__init__(self, manager)

        self.vpc = CmpResourceProviderVpcService(self.manager)
        self.instance = CmpResourceProviderInstanceService(self.manager)
        self.gateway = CmpResourceProviderGatewayService(self.manager)
        self.load_balancer = CmpResourceProviderLoadBalancerService(self.manager)
        self.site_network = CmpResourceProviderSiteNetworkService(self.manager)


class CmpResourceProviderVpcService(CmpResourceAbstractService):
    """Cmp resource provider vpc service"""

    VERSION = "v2.0"

    def get(self, oid, **kwargs):
        """get vpc

        :param oid: vpc id or uuid
        :return: vpc
        :raise CmpApiClientError:
        """

        uri = self.get_uri("provider/vpcs/%s" % oid, preferred_version=self.VERSION, **kwargs)
        res = self.api_get(uri).get("vpc", {})
        self.logger.debug("get vpc %s: %s" % (oid, truncate(res)))
        return res


class CmpResourceProviderInstanceService(CmpResourceAbstractService):
    """Cmp resource provider instance service"""

    def get(self, oid, **kwargs):
        """get instance

        :param oid: instance id or uuid
        :return: instance
        :raise CmpApiClientError:
        """
        uri = self.get_uri("provider/instances/%s" % oid, preferred_version=self.VERSION, **kwargs)
        res = self.api_get(uri).get("instance", {})
        self.logger.debug("get instance %s: %s" % (oid, truncate(res)))
        return res

    def load(self, container, name, physical_resource, pwd, image, **kwargs):
        """import provider instance from physical server

        :param container: provider container id
        :param name: instance name
        :param physical_resource: physical server resource id
        :param pwd: instance password
        :param image: instance image
        :param kwargs: additional key value params
        :param kwargs.hotsname: hostname
        :return:
        """
        data = {
            "container": container,
            "name": name,
            "desc": name,
            "physical_id": physical_resource,
            "attribute": {},
            "resclass": "beehive_resource.plugins.provider.entity.instance.ComputeInstance",
            "configs": {"multi_avz": True, "admin_pass": pwd, "image": image},
        }
        data["configs"].update(kwargs)
        uri = self.get_uri("entities/import", preferred_version=self.VERSION, **kwargs)
        res = self.api_post(uri, data={"resource": data}).get("uuid", None)
        self.logger.debug("import entity: %s" % res)

    def del_cache(self, oid, **kwargs):
        """Delete resource provider instance cache

        :return:
        """
        uri = self.get_uri("entities/%s/cache" % oid, preferred_version=self.VERSION, **kwargs)
        res = self.api_put(uri)
        self.logger.debug("delete cache for provider instance: %s" % res.get("uuid"))

    def stack_create_from_vm(
        self,
        name: str,
        provider_vm_id,
        stack_admin_pwd: str,
        engine: str,
        version: str,
        charset: str = "latin1",
        timezone: str = "Europe/Rome",
    ):
        config = {
            "container": "ResourceProvider01",
            "name": name,
            "desc": name,
            "physical_id": provider_vm_id,
            "attribute": {},
            "resclass": "beehive_resource.plugins.provider.entity.sql_stack_v2.SqlComputeStackV2",
            "configs": {
                "charset": charset,
                "timezone": timezone,
                "engine": engine,
                "version": version,
                "pwd": {"admin": stack_admin_pwd, "db_superuser": "", "db_appuser_pwd": ""},
                "user": {"db_superuser": "system", "db_appuser_pwd": "test"},
            },
        }
        uri = self.get_uri("entities/import", preferred_version=self.VERSION)
        res = self.api_post(uri, data={"resource": config}).get("uuid", None)
        self.logger.debug("created stackV2 %s", res)
        return res


class CmpResourceProviderGatewayService(CmpResourceAbstractService):
    """Cmp resource provider gateway service"""

    def get(self, oid, **kwargs):
        """get gateway

        :param oid: gateway id or uuid
        :return: gateway
        :raise CmpApiClientError:
        """
        uri = self.get_uri("provider/gateways/%s" % oid, preferred_version=self.VERSION, **kwargs)
        res = self.api_get(uri).get("gateway", {})
        self.logger.debug("get gateway %s: %s" % (oid, truncate(res)))
        return res


class CmpResourceProviderLoadBalancerService(CmpResourceAbstractService):
    """Cmp resource provider load balancer service"""

    def get(self, oid, **kwargs):
        """get load balancer

        :param oid: load balancer id or uuid
        :return: load balancer
        :raise CmpApiClientError:
        """
        uri = self.get_uri("provider/loadbalancers/%s" % oid, preferred_version=self.VERSION, **kwargs)
        res = self.api_get(uri).get("load_balancer", {})
        self.logger.debug("get load balancer %s: %s" % (oid, truncate(res)))
        return res

    def load(self, container, name, **kwargs):
        """import provider load balancer

        :param container: provider container id
        :param name: instance name
        :param kwargs: additional key-value params
        :return:
        """
        data = {
            "container": container,
            "name": name,
            "desc": name,
            "attribute": {
                "compute_zone": kwargs.get("compute_zone"),
                "site_network": kwargs.get("site_network"),
                "multi_avz": False,
            },
            "resclass": "beehive_resource.plugins.provider.entity.load_balancer.ComputeLoadBalancer",
            "configs": {},
        }
        data["configs"].update(kwargs)
        uri = self.get_uri("entities/import", preferred_version=self.VERSION, **kwargs)
        res = self.api_post(uri, data={"resource": data})
        res = res.get("uuid")
        print("imported compute load balancer: %s" % res)
        return res


class CmpResourceProviderSiteNetworkService(CmpResourceAbstractService):
    """Cmp resource provider site network service"""

    def get(self, oid, **kwargs):
        """get site network

        :param oid: site network id or uuid
        :return: gateway
        :raise CmpApiClientError:
        """
        uri = self.get_uri("provider/site_networks/%s" % oid, preferred_version="v2.0", **kwargs)
        res = self.api_get(uri).get("site_network", {})
        self.logger.debug("get site-network %s: %s" % (oid, truncate(res)))
        return res
