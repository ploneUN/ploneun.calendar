from five import grok
from Products.CMFCore.interfaces import IContentish
from datetime import datetime
from Solgema.fullcalendar.interfaces import ISolgemaFullcalendarMarker
import calendar
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

