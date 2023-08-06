# -*- coding: utf-8 -*-

from plone.dexterity.browser import add
from plone.dexterity.browser import edit
from plone.dexterity.browser.view import DefaultView


class TaskAddForm(add.DefaultAddForm):
    portal_type = 'task'

    def __init__(self, context, request):
        super(TaskAddForm, self).__init__(context, request)
        # disable portlets
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)


class TaskAddView(add.DefaultAddView):
    form = TaskAddForm


class TaskEditForm(edit.DefaultEditForm):

    def __init__(self, context, request):
        super(TaskEditForm, self).__init__(context, request)
        # disable portlets
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)


class TaskView(DefaultView):
    """
    """

    def __init__(self, context, request):
        super(TaskView, self).__init__(context, request)
        # disable portlets
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)

    def __call__(self):
        return self.context.REQUEST.RESPONSE.redirect(
            '{}/facetedtask_view'.format(self.context.aq_parent.absolute_url())
        )
