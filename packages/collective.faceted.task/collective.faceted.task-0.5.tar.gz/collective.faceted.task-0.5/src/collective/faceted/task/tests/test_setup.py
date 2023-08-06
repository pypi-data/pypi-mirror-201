# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from collective.faceted.task.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of collective.faceted.task into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.faceted.task is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('collective.faceted.task'))

    def test_uninstall(self):
        """Test if collective.faceted.task is cleanly uninstalled."""
        self.installer.uninstallProducts(['collective.faceted.task'])
        self.assertFalse(self.installer.isProductInstalled('collective.faceted.task'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that ICollectiveFacetedTaskLayer is registered."""
        from collective.faceted.task.interfaces import ICollectiveFacetedTaskLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectiveFacetedTaskLayer, utils.registered_layers())
