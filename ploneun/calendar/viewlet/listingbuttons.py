from Acquisition import aq_inner
from zope.interface import Interface
from five import grok
from zope.component import getMultiAdapter
from Products.CMFCore.interfaces import IContentish
from plone.app.layout.viewlets import interfaces as manager
from ploneun.calendar.interfaces import IProductSpecific
from Solgema.fullcalendar.interfaces import ISolgemaFullcalendarMarker
from plone.app.collection.interfaces import ICollection
from Products.ATContentTypes.interfaces.topic import IATTopic
import os

grok.templatedir('templates')


class ListingButtons(grok.Viewlet):
    grok.context(ISolgemaFullcalendarMarker)
    grok.viewletmanager(manager.IBelowContentTitle)
    grok.template('listingbuttons')
    grok.layer(IProductSpecific)

    def available(self):
        # only show on collection/topic
        if not self.context.restrictedTraverse('@@iscalendarlayout')():
            return False
        if ICollection.providedBy(self.context):
            return True
        if IATTopic.providedBy(self.context):
            return True
        return False

    def buttons(self):
        current_view = os.path.basename(self.request.getURL())
        url = self.context.absolute_url()
        buttons = [{
             'id': 'solgemafullcalendar_view',
             'url': url + '/solgemafullcalendar_view',
             'label': u'Calendar',
            }, {
             'id': 'list_all',
             'url': url + '/list_all',
             'label': u'List View',
            }, {
             'id': 'list_upcoming',
             'url': url + '/list_upcoming',
             'label': u'Upcoming',
            }, {
             'id': 'list_past',
             'url': url + '/list_past',
             'label': u'Past',
            }, {
              'id': 'calendar_table',
              'url': url + '/calendar_table',
              'label': u'Table'
        }]

        for button in buttons:
            if button['id'] == current_view:
                button['checked'] = True
            else:
                button['checked'] = False

        return buttons
