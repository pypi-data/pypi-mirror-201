# -*- coding: utf-8 -*-

from plone import api

from collective.eeafaceted.z3ctable.browser.views import FacetedTableView

from collective.faceted.task import _
from collective.faceted.task.browser.table import FacetedTasksTable
from collective.faceted.task.interfaces import IFacetedTaskContainer

from collective.task.behaviors import ITask

from Products.CMFPlone.PloneBatch import Batch

from zope.interface import implements
from zope.viewlet.interfaces import IViewlet


class TasksListBase(FacetedTableView):
    """
    Base class for both the view and viewlet
    rendering the task listing.
    """
    noresult_message = _(u"There is no task for this content.")
    __table__ = FacetedTasksTable

    def update(self):
        self.table = self.__table__(self.context, self.request)
        brains = self.query_tasks()
        self.table.results = [b.getObject() for b in brains]
        self.table.update()

    def query_tasks(self):
        catalog = api.portal.get_tool('portal_catalog')
        container_path = '/'.join(self.context.getPhysicalPath())
        brains = catalog.searchResults(
            object_provides=ITask.__identifier__,
            path={'query': container_path},
            sort_on='getObjPositionInParent'
        )
        return brains

    def tasks_batch(self):
        brains = self.query_tasks()
        batch = Batch(brains, len(brains))
        return batch


class TasksListViewlet(TasksListBase):
    """
    Viewlet displaying tasks list for current task container object.
    """
    implements(IViewlet)

    label = _(u"Tasks list")

    def __init__(self, context, request, view, manager=None):
        super(TasksListBase, self).__init__(context, request)
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager


class TasksListView(TasksListBase):
    """
    View displaying tasks list for current task container object.
    """


class IsFacetedTaskContainer(object):
    """
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return IFacetedTaskContainer.providedBy(self.context)
