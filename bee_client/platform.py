# SPDX-License-Identifier: EUPL-1.2
#
# (C) Copyright 2018-2026 CSI-Piemonte

from .client import CmpBaseService, CmpApiManager


class CmpPlatformAbstractService(CmpBaseService):
    """Cmp business service"""

    SUBSYSTEM = "platform"
    PREFIX = "plt"
    VERSION = "v1.0"


class CmpPlatformService(CmpPlatformAbstractService):
    """Cmp business service"""

    def __init__(self, manager:CmpApiManager):
        CmpBaseService.__init__(self, manager)

        from .test import CmpPlatformTestService

        self.test = CmpPlatformTestService(self.manager)
