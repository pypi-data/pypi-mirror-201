# -*- coding: utf-8 -*-

from collective.eeafaceted.z3ctable.columns import BaseColumn
from collective.eeafaceted.z3ctable.columns import BaseColumnHeader

from collective.task.adapters import TaskAdapter
from collective.task.browser.table import TasksTable


class FacetedTasksTable(TasksTable):

    """Table that displays tasks info."""


class FacetedTaskColumnHeader(BaseColumnHeader):
    """
    Column header for faceted task dashboard
    """

    @property
    def faceted_url(self):
        base_url = '/'.join(self.request.get('URL').split('/')[:-1])
        faceted_url = '{}/facetednavigation_view'.format(base_url)
        return faceted_url


class TitleColumn(BaseColumn):
    """
    Column that displays title.
    """

    def renderCell(self, item):
        adaptedTask = TaskAdapter(item.getObject())
        title = adaptedTask.get_full_tree_title().decode('utf-8')

        path = title.split('/')
        head = path[-1]
        tail = u'/'.join(path[0:-1])
        title = u'<span class="task_url_head">{}</span>'.format(head)
        if tail:
            title = u'<span class="task_url_tail">{}/</span>{}'.format(tail, title)

        return title
