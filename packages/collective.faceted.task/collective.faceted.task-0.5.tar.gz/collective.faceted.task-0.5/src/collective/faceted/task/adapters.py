# -*- coding: utf-8 -*-

from collective.task.behaviors import ITaskContainer

from collective.faceted.task.interfaces import IFacetedTaskConfig

from eea.facetednavigation.criteria.handler import Criteria as eeaCriteria

from zope.component import queryUtility


class Criteria(eeaCriteria):
    """
    """

    def __init__(self, context):
        """ """
        if ITaskContainer.providedBy(context):
            faceted_task_config = queryUtility(IFacetedTaskConfig)
            if faceted_task_config:
                context = faceted_task_config

        super(Criteria, self).__init__(context)
