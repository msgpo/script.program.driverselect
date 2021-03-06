import xbmc
import xbmcgui
import xbmcaddon
import json
import platform
import re

ADDON_NAME = xbmcaddon.Addon().getAddonInfo('name')
PATH = xbmcaddon.Addon().getAddonInfo('path')
PROFILE = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile'))
LS = xbmcaddon.Addon().getLocalizedString

# Constants

STRING = 0
BOOL = 1
NUM = 2


def writeLog(message, level=xbmc.LOGDEBUG):
    xbmc.log('[%s %s] %s' % (xbmcaddon.Addon().getAddonInfo('id'),
                             xbmcaddon.Addon().getAddonInfo('version'),
                             message.encode('utf-8')), level)


def notify(header, message, icon=xbmcgui.NOTIFICATION_INFO, dispTime=5000):
    xbmcgui.Dialog().notification(header.encode('utf-8'), message.encode('utf-8'), icon=icon, time=dispTime)


def release():
    item = {}
    coll = {'platform': platform.system(), 'hostname': platform.node()}
    if coll['platform'] == 'Linux':
        with open('/etc/os-release', 'r') as _file:
            for _line in _file:
                parameter, value = _line.split('=')
                item[parameter] = value.replace('"', '').strip()

    coll.update({'osname': item.get('NAME', ''), 'osid': item.get('ID', ''), 'osversion': item.get('VERSION_ID', '')})
    return coll


def dialogOK(header, message):
    return xbmcgui.Dialog().ok(header.encode('utf-8'), message.encode('utf-8'))


def dialogYesNo(header, message):
    return xbmcgui.Dialog().yesno(header.encode('utf-8'), message.encode('utf-8'))


def dialogSelect(header, itemlist, preselect=-1, useDetails=False):
    return xbmcgui.Dialog().select(header.encode('utf-8'), itemlist, preselect=preselect, useDetails=useDetails)


def jsonrpc(query):
    querystring = {"jsonrpc": "2.0", "id": 1}
    querystring.update(query)
    try:
        response = json.loads(xbmc.executeJSONRPC(json.dumps(querystring, encoding='utf-8')))
        if 'result' in response: return response['result']
    except TypeError, e:
        writeLog('Error executing JSON RPC: %s' % (e.message), xbmc.LOGFATAL)
    return None


def getAddonSetting(setting, sType=STRING, multiplicator=1):
    if sType == BOOL:
        return  True if xbmcaddon.Addon().getSetting(setting).upper() == 'TRUE' else False
    elif sType == NUM:
        try:
            return int(re.match('\d+', xbmcaddon.Addon().getSetting(setting)).group()) * multiplicator
        except AttributeError:
            return 0
    else:
        return xbmcaddon.Addon().getSetting(setting)
