from five import grok
from plone.directives import dexterity, form
from ploneun.calendar.content.calendarfacility import ICalendarFacility

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(ICalendarFacility)
    grok.require('zope2.View')
    grok.template('calendarfacility_view')
    grok.name('view')

