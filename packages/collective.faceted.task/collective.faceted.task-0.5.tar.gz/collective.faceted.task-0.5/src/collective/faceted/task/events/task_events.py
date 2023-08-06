# -*- coding: utf-8 -*-

from Acquisition import aq_base

from eea.facetednavigation.interfaces import IFacetedNavigable
from eea.facetednavigation.layout.interfaces import IFacetedLayout
from eea.facetednavigation.subtypes.interfaces import IPossibleFacetedNavigable


def activate_faceted_tasks_listing(task_container, event):
    """
    Set the listing tasks faceted view on the faceted tasks container.
    """
    if hasattr(aq_base(task_container), 'checkCreationFlag'):
        if task_container.checkCreationFlag():
            return

    if IFacetedNavigable.providedBy(task_container):
        return
    elif IPossibleFacetedNavigable.providedBy(task_container):
        subtyper = task_container.unrestrictedTraverse('@@faceted_subtyper')
        subtyper.enable()
        IFacetedLayout(task_container).update_layout('list_tasks')
        task_container.manage_delProperties(['layout'])
