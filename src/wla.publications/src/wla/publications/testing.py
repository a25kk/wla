# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from zope.configuration import xmlconfig

import wla.publications


class WlaPublicationsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        xmlconfig.file(
            'configure.zcml',
            wla.publications,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'wla.publications:default')


WLA_PUBLICATIONS_FIXTURE = WlaPublicationsLayer()


WLA_PUBLICATIONS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(WLA_PUBLICATIONS_FIXTURE,),
    name='WlaPublicationsLayer:IntegrationTesting'
)


WLA_PUBLICATIONS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(WLA_PUBLICATIONS_FIXTURE,),
    name='WlaPublicationsLayer:FunctionalTesting'
)


WLA_PUBLICATIONS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        WLA_PUBLICATIONS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='WlaPublicationsLayer:AcceptanceTesting'
)
