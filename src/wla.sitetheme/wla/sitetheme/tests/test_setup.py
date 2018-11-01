# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from wla.buildout.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of wla.buildout into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if wla.buildout is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('wla.buildout'))

    def test_uninstall(self):
        """Test if wla.buildout is cleanly uninstalled."""
        self.installer.uninstallProducts(['wla.buildout'])
        self.assertFalse(self.installer.isProductInstalled('wla.buildout'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IWlaBuildoutLayer is registered."""
        from wla.buildout.interfaces import IWlaBuildoutLayer
        from plone.browserlayer import utils
        self.failUnless(IWlaBuildoutLayer in utils.registered_layers())
