from ploneun.calendar.interfaces import ITableColumnProvider
from zope.interface import Interface
from five import grok

class DefaultColumnProvider(grok.Adapter):
    grok.implements(ITableColumnProvider)
    grok.context(Interface)

    def header_row(self):
        return [
            u'Title',
            u'Description'
        ]

    def item_row(self, item):
        return [
            '<a href="%s">%s</a>' % (item.getURL(), item.Title()),
            item.Description()
        ]
