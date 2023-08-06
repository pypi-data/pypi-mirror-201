# -*- coding: utf-8 -*-

from plone import api

import os


def isNotCurrentProfile(context):
    return context.readDataFile("collectivefacetedtask_marker.txt") is None


def post_install(context):
    """Post install script"""
    if isNotCurrentProfile(context):
        return

    set_up_faceted_task_config(context)


def set_up_faceted_task_config(context):
    """
    """

    site = api.portal.get()
    faceted_task_config = site.unrestrictedTraverse('faceted_task_config')
    subtyper = faceted_task_config.unrestrictedTraverse('@@faceted_subtyper')

    if not subtyper.is_faceted:
        # enable faceted navigation
        subtyper.enable()

        # load default config
        xml_faceted_config = open('%s/faceted_task_config.xml' % os.path.dirname(__file__))
        importer = faceted_task_config.unrestrictedTraverse('@@faceted_exportimport')
        importer.import_xml(import_file=xml_faceted_config)

        # allow js edit ressources on the faceted_task_config view
        portal_javascripts = api.portal.get_tool('portal_javascripts')
        faceted_edit_js = portal_javascripts.getResource('faceted_edit.js')
        condition = "{} or 'faceted_task_config' in request.URL0".format(
            faceted_edit_js.getExpression()
        )
        faceted_edit_js.setExpression(condition)
