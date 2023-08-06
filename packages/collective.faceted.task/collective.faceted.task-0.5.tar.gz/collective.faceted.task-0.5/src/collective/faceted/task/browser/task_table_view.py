# -*- coding: utf-8 -*-

from collective.eeafaceted.z3ctable.browser.views import FacetedTableView

from collective.faceted.task.interfaces import IFacetedTasksTable

from zope.interface import implements


class FacetedTaskTableView(FacetedTableView):
    """
    """

    implements(IFacetedTasksTable)

    ignoreColumnWeight = True

    def _getViewFields(self):
        """Returns fields we want to show in the table."""

        col_names = [
            u'simple_status',
            u'path',
            u'assigned_user_column',
            u'CreationDate',
            u'due_date',
        ]

        return col_names
