from five import grok
from ploneun.calendar.interfaces import ICalendarDataExtender
from zope.interface import Interface

class DefaultCalendarDataExtender(grok.Adapter):
    grok.context(Interface)
    grok.implements(ICalendarDataExtender)

    def __init__(self, context):
        self.context = context

    def __call__(self, brain):
        return {
            'footnote': ''
        }

class EventCalendarDataExtender(grok.Adapter):
    grok.context(Interface)
    grok.implements(ICalendarDataExtender)
    grok.name('Event')

    def __init__(self, context):
        self.context = context

    def __call__(self, brain):
        return {
            'footnote': brain.getObject().location or ''
        }
