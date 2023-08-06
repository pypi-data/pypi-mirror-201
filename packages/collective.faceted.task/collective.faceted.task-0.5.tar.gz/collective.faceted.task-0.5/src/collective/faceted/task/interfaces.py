# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from collective.eeafaceted.z3ctable.interfaces import IFacetedTable

from collective.task.behaviors import ITaskContainer

from zope.interface import Interface

from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveFacetedTaskLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IFacetedTaskConfig(Interface):
    """ Marker interface for FacetedTask config."""


class IFacetedTaskContainer(ITaskContainer):
    """ Marker interface for FacetedTask container."""


class IFacetedTasksTable(IFacetedTable):
    """ Marker interface FacetedTask table."""
