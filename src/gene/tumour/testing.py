# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import gene.tumour


class GeneTumourLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=gene.tumour)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'gene.tumour:default')


GENE_TUMOUR_FIXTURE = GeneTumourLayer()


GENE_TUMOUR_INTEGRATION_TESTING = IntegrationTesting(
    bases=(GENE_TUMOUR_FIXTURE,),
    name='GeneTumourLayer:IntegrationTesting'
)


GENE_TUMOUR_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(GENE_TUMOUR_FIXTURE,),
    name='GeneTumourLayer:FunctionalTesting'
)


GENE_TUMOUR_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        GENE_TUMOUR_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='GeneTumourLayer:AcceptanceTesting'
)
