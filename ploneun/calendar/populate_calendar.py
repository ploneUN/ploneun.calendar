from zope.globalrequest import getRequest
from plone.api import content as contentapi
from zope.app.container.interfaces import IObjectAddedEvent
from ploneun.calendar.content.calendarfacility import ICalendarFacility
from five import grok

@grok.subscribe(ICalendarFacility, IObjectAddedEvent)
def populate_calendar(obj, event):

    if obj.has_key('index'):
        return

    collection = contentapi.create(obj, 'Collection', id='index',
                                    title=obj.Title())


    collection.setLayout('solgemafullcalendar_view')

    collection.query = [
        {'i': 'portal_type', 
         'o': 'plone.app.querystring.operation.selection.is', 
         'v': ['Event']}, 
        {'i': 'path', 
         'o': 'plone.app.querystring.operation.string.relativePath',
         'v': '../'}
    ]

    obj.setDefaultPage('index')

    collection.reindexObject()
    obj.reindexObject()

    request = getRequest()
    request.response.redirect(collection.absolute_url())
