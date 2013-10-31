from five import grok
from Products.CMFCore.interfaces import IContentish
from datetime import datetime
from Solgema.fullcalendar.interfaces import ISolgemaFullcalendarMarker
from ploneun.calendar.interfaces import ITableColumnProvider
import calendar
from zope.component import queryAdapter
grok.templatedir('templates')

class CalendarTable(grok.View):
    grok.context(ISolgemaFullcalendarMarker)
    grok.name('calendar_table')
    grok.require('zope2.View')
    grok.template('calendartable')

    def months(self):
        thismonth = datetime.now().month
        month = int(self.request.get('month', thismonth))
        return [{'value': i, 'name': n,
            'selected': i == month} for i, n in enumerate(
            calendar.month_name) if i
        ]

    def month(self):
        thismonth = datetime.now().month
        return int(self.request.get('month', thismonth))


    def items(self):
        now = datetime.now()
        month = int(self.request.get('month', now.month))
        year = int(self.request.get('year', now.year))
        
        results = self.context.results()

        def filter_month_year(item):
            if not item.start:
                return False
            if item.start.month() == month and item.start.year() == year:
                return True
            return False

        return filter(filter_month_year, results)

    def items_by_type(self):
        items = self.items()
        types = {}
        for item in items:
            types.setdefault(item.portal_type, [])
            types[item.portal_type].append(item)
        return types

    def extract_types(self, items_by_type):
        result = []
        portal_types = self.context.portal_types
        for i in items_by_type.keys():
            title = portal_types[i].title
            result.append({
                'id': i,
                'title': title
            })
        return result

    def columnprovider(self, portal_type):
        defaultcolumnprovider = ITableColumnProvider(self.context)
        columnprovider = queryAdapter((self.context,), ITableColumnProvider)
        columnprovider = columnprovider or defaultcolumnprovider
        return columnprovider

    def type_columns(self, portal_type):
        colprovider = self.columnprovider(portal_type)
        return colprovider.header_row()

    def item_columns(self, item):
        colprovider = self.columnprovider(item.portal_type)
        return colprovider.item_row(item)

