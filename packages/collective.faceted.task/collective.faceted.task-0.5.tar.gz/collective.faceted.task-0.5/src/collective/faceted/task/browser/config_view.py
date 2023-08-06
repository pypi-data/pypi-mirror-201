# -*- coding: utf-8 -*-

from Acquisition import aq_base

from collective.faceted.task.interfaces import IFacetedTaskConfig

from Products.Five import BrowserView

from zope.component import getUtility
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from zope.traversing.namespace import view


class FacetedTaskConfigView(BrowserView):
    """
    """
    implements(IPublishTraverse)

    def __init__(self, context, request):
        """
        """
        faceted_task_config = getUtility(IFacetedTaskConfig)
        self.context = aq_base(faceted_task_config).__of__(context)
        self.request = request

    def __call__(self):
        self.update()
        return self.context()

    def update(self):
        """
        """

    def publishTraverse(self, request, name):
        """
        """
        return self.unrestrictedTraverse(name)

    def unrestrictedTraverse(self, name):
        """
        """
        return self.context.unrestrictedTraverse(name)


class FacetedTaskConfigViewTraverser(view):
    """
    """

    def traverse(self, name, furtherPath):
        """
        """
        config_view = self.context
        return config_view.unrestrictedTraverse(name)
