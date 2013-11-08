from logging import getLogger

logger = getLogger('ploneun.calendar')

def _patch_solgema_collection_path_criteria():

    try:
        from Solgema.fullcalendar.browser.adapters import CollectionEventSource
    except ImportError, e:
        return

    if getattr(CollectionEventSource, '__ploneun_path_patched', False):
        return

    logger.info('Patching CollectionEventSource to support path criteria')

    from Acquisition import aq_parent

    _orig_getCriteriaArgs = CollectionEventSource._getCriteriaArgs

    def _getCriteriaArgs(self):
        _args, filters = _orig_getCriteriaArgs(self)
        if 'path' in _args:
            path = _args['path']
            if path == '../':
                parent = aq_parent(self.context)
                path = '/'.join(parent.getPhysicalPath())
            
            _args['path'] = {
                'query': path,
                'depth': 1
            }
        return _args, filters

    CollectionEventSource._getCriteriaArgs = _getCriteriaArgs

_patch_solgema_collection_path_criteria()


def _patch_solgema_data_extender():
    try:
        from Solgema.fullcalendar.browser import adapters
    except ImportError, e:
        return

    if getattr(adapters, '__ploneun_dataextender_patched', False):
        return

    logger.info('Patching Solgema.fullcalendar with data extender support')

    from zope.component.hooks import getSite
    from ploneun.calendar.interfaces import ICalendarDataExtender
    from zope.component import getAdapter

    _orig_dict_from_events = adapters.dict_from_events

    def dict_from_events(events, editable=None, state=None, color=None, css=None):
        result = _orig_dict_from_events(events, editable, state, color, css)
        site = getSite()
        newresult = []
        for item in result:
            uid = item['id'].replace('UID_','')
            brains = site.portal_catalog(UID=uid)
            brain = None
            if brains:
                brain = brains[0]

            portal_type = brain.portal_type if brain else None
            extender = getAdapter(site, ICalendarDataExtender, name=portal_type)
            item.update(extender(brain))
            newresult.append(item)
        return newresult
    
    adapters.dict_from_events = dict_from_events
    adapters.__ploneun_dataextender_patched = True

_patch_solgema_data_extender()
