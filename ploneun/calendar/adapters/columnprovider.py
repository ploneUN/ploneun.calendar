from ploneun.calendar.interfaces import ITableColumnProvider
from zope.interface import Interface
from five import grok

class DefaultColumnProvider(grok.Adapter):
    grok.implements(ITableColumnProvider)
    grok.context(Interface)

    def header_row(self):
        return [
            u'Date',
            u'Title',
            u'Description'
        ]

    def item_row(self, item):
        date = ''
        if item.start and item.end:
            date = '%s - %s' % (item.start.strftime('%d %b'),
                    item.end.strftime('%d %b'))
        return [
            date,
            '<a href="%s">%s</a>' % (item.getURL(), item.Title()),
            item.Description()
        ]


class EventColumnProvider(grok.Adapter):
    grok.implements(ITableColumnProvider)
    grok.context(Interface)
    grok.name('Event')

    def header_row(self):
        return [
            u'Date',
            u'Event Title',
            u'Place',
            u'Contact Person'
        ]

    def item_row(self, item):
        item_obj = item.getObject()
        return [
            '%s - %s' % (item.start.strftime('%d %b'), 
                            item.end.strftime('%d %b')),
            '<a href="%s">%s</a>' % (item.getURL(), item.Title()),
            item_obj.getField('location').get(item_obj),
            item_obj.getField('contactName').get(item_obj)
        ]
