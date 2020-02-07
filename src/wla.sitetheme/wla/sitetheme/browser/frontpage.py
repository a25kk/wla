# -*- coding: utf-8 -*-
"""Module providing views for the site navigation root"""
from Products.Five.browser import BrowserView
from plone import api

from ade25.sitecontent.contentpage import IContentPage


class FrontPageView(BrowserView):
    """ General purpose front page view """

    def __call__(self):
        self.has_preview_cards = len(self.cards()) > 0
        return self.render()

    def render(self):
        return self.index()

    def cards(self, search_limit=12):
        preview_cards = self.preview_cards(search_limit=search_limit)
        cards = list()
        for item in preview_cards:
            item_obj = item.getObject()
            item_size = getattr(item_obj, 'elementSize', '100')
            cards.append({
                'uuid': item.UID,
                'title': item.Title,
                'item_size': item_size,
                'template': item_obj.restrictedTraverse('@@card-view')()
            })
        return cards

    @staticmethod
    def preview_cards(search_limit=12):
        items = api.content.find(
            object_provides=IContentPage.__identifier__,
            review_state='published',
            sort_on='getObjPositionInParent',
            is_promoted=True,
            sort_limit=search_limit)
        return items[:search_limit]
