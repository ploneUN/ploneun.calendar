from collective.grok import gs
from ploneun.calendar import MessageFactory as _

@gs.importstep(
    name=u'ploneun.calendar', 
    title=_('ploneun.calendar import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('ploneun.calendar.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
