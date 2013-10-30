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
