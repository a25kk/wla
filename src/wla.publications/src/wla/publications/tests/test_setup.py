# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from wla.publications.testing import WLA_PUBLICATIONS_INTEGRATION_TESTING  # noqa
from plone import api

import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that wla.publications is properly installed."""

    layer = WLA_PUBLICATIONS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if wla.publications is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('wla.publications'))

    def test_uninstall(self):
        """Test if wla.publications is cleanly uninstalled."""
        self.installer.uninstallProducts(['wla.publications'])
        self.assertFalse(self.installer.isProductInstalled('wla.publications'))

    def test_browserlayer(self):
        """Test that IWlaPublicationsLayer is registered."""
        from wla.publications.interfaces import IWlaPublicationsLayer
        from plone.browserlayer import utils
        self.assertIn(IWlaPublicationsLayer, utils.registered_layers())
