# -*- coding: utf-8 -*-

from collective.faceted.task.interfaces import IFacetedTaskConfig

from plone.dexterity.content import Container

from zope.interface import implements


class FacetedTaskConfig(Container):
    """
    FacetedTask config utility factory.
    """

    implements(IFacetedTaskConfig)

    UID = None

    def __call__(self):
        return self.unrestrictedTraverse('@@configure_faceted.html')()

    def absolute_url(self):
        """
        """
        old_url = super(FacetedTaskConfig, self).absolute_url()
        url = old_url.replace(self.__name__, 'faceted_task_config')
        return url
