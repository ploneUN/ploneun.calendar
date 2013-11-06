from five import grok
from Products.CMFCore.interfaces import IContentish
from Products.CMFPlone.PloneBatch import Batch
from DateTime import DateTime
from Solgema.fullcalendar.interfaces import ISolgemaFullcalendarMarker
grok.templatedir('templates')

class CalendarListing(grok.View):
    grok.context(ISolgemaFullcalendarMarker)
    grok.baseclass()
    grok.name('calendarlisting')
    grok.require('zope2.View')
    grok.template('calendarlisting')

    def months(self):
        items = self._items()
        b_start = self.request.get('b_start', 0)
        result = self._group_by_month(items)
        return Batch(result, 2, int(b_start), orphan=0)

    def _group_by_month(self, events):
        months = []
        month_info = []
        old_month_year = None
        for event in events:

            # ignore if content does not have start/end
            if not event.start:
                continue 

            start = event.start
            end = event.end
            month = str(start.month())
            year = str(start.year())
            month_year = year+month
            if month_year != old_month_year:
                old_month_year = month_year
                if month_info:
                    months.append(month_info)
                month_info = {'month': start.month(),
                              'year': start.year(),
                              'month_name': start.strftime("%B"),
                              'events': []}

            event_dict = {'event': event,
                          'day': start.day(),
                          'month' : start.month(),
                          'month_name': start.strftime('%b'),
                          'year' : start.year(),
                          'day_end' : end.day(),
                          'month_end' : end.month(),
                          'month_end_name': end.strftime('%b'),
                          'year_end' : end.year(),
                          'title': event.Title,
                          'description': event.Description,
                          'location': event.location,
                          'url': event.getURL(),
                          }
            month_info['events'].append(event_dict)

        if month_info:
            months.append(month_info)

        return months

class AllListing(CalendarListing):
    grok.name('list_all')
    
    def _items(self):
        return self.context.queryCatalog()


class UpcomingListing(CalendarListing):
    grok.name('list_upcoming')
    
    def _items(self):
        today = DateTime()
        return filter(lambda x: (x.start > today) if x.start else False,
                    self.context.queryCatalog())

class PastListing(CalendarListing):
    grok.name('list_past')
    
    def _items(self):
        today = DateTime()
        return filter(lambda x: (x.end < today) if x.end else False,
                    self.context.queryCatalog())


