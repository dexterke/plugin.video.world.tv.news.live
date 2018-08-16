import HTMLParser
import cookielib
import json
import os
import re
import sys
import urllib
import urllib2
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin


## Settings
settings = xbmcaddon.Addon(id='plugin.video.world.tv.news.live')
userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
myLogFile = os.path.join(settings.getAddonInfo('path'), 'resources', 'plugin.log')
movies_thumb = os.path.join(settings.getAddonInfo('path'), 'resources', 'media', 'movies.png')
addon_thumb = os.path.join(settings.getAddonInfo('path'), 'icon.png')


LF = open(myLogFile, 'w+')
LF.write('--- INIT -------------------' + '\n')
LF.close()


def removeSubstr(string, suffix):
    return string[:string.index(suffix) + len(suffix)]


def trimSubstrEnd(string, prefix):
    part = string.split(prefix)
    return str(part[1])


def trimSubstr(string, suffix):
    part = string.split(suffix)
    return str(part[0])


def setIcon(thumb_file):
  thumb_file_name = thumb_file.replace(' ', '')[:-4].upper()
  try:
    thumb_file_name = os.path.join(settings.getAddonInfo('path'), 'resources', 'media', thumb_file)
  except:
    thumb_file_name = movies_thumb

  return thumb_file_name


def ROOT():
  addDir('Aljazeera Live [EN]', "http://english.streaming.aljazeera.net/aljazeera/english2/index.m3u8", setIcon('AlJazeera.png'))
  addDir('Aljazeera Live [AR]', "http://aljazeera-ara-apple-live.adaptive.level3.net/apple/aljazeera/arabic/160.m3u8", setIcon('AlJazeera.png'))
  addDir('ATV [HU]', "http://nodes.stream.atv.hu/atvliveedge/_definst_//atvstream_2_aac/playlist.m3u8",  setIcon('ATVHU.png'))
  addDir('EuroNews Live [EN]', "http://www.euronews.com/api/watchlive.json", setIcon('EuroNewsLive.png'))
  addDir('EuroNews Live [FR]', "http://fr.euronews.com/api/watchlive.json", setIcon('EuroNewsLive_FR.png'))
  addDir('EuroNews Live [DE]', "http://de.euronews.com/api/watchlive.json", setIcon('EuroNewsLive_DE.png'))
  addDir('EuroNews Live [IT]', "http://it.euronews.com/api/watchlive.json", setIcon('EuroNewsLive_IT.png'))
  addDir('EuroNews Live [ES]', "http://es.euronews.com/api/watchlive.json", setIcon('EuroNewsLive_ES.png'))
  addDir('EuroNews Live [PT]', "http://pt.euronews.com/api/watchlive.json", setIcon('EuroNewsLive_PT.png'))
  addDir('EuroNews Live [GR]', "http://gr.euronews.com/api/watchlive.json", setIcon('EuroNewsLive_GR.png'))
  addDir('EuroNews Live [HU]', "http://hu.euronews.com/api/watchlive.json", setIcon('EuroNewsLive_HU.png'))
  addDir('EuroNews Live [RU]', "http://ru.euronews.com/api/watchlive.json", setIcon('EuroNewsLive_RU.png'))
  addDir('EuroNews Live [TR]', "http://tr.euronews.com/api/watchlive.json", setIcon('EuroNewsLive_TR.png'))
  addDir('EuroNews Live [FA]', "http://fa.euronews.com/api/watchlive.json", setIcon('EuroNewsLive.png'))
  addDir('EuroNews Live [AR]', "http://arabic.euronews.com/api/watchlive.json", setIcon('EuroNewsLive.png'))
  addDir('Digi24 Live [RO]', "http://www.digi24.ro/live/digi24", setIcon('Digi24.png'))
  addDir('France24 Live [EN]', "http://static.france24.com/live/F24_EN_LO_HLS/live_web.m3u8", setIcon('France24.png'))
  addDir('France24 Live [FR]', "http://static.france24.com/live/F24_FR_LO_HLS/live_web.m3u8", setIcon('France24.png'))
  addDir('France24 Live [ES]', "http://static.france24.com/live/F24_ES_LO_HLS/live_web.m3u8", setIcon('France24.png'))
  addDir('FranceInfo Live [FR]', "http://hdfauthftv-a.akamaihd.net/esi/TA?format=json&url=https%3A%2F%2Flivefrancetv.akamaized.net%2Fsimulcast%2FFrance_Info%2Fhls_monde%2Findex.m3u8&callback=_jsonp_loader_callback_request_0", setIcon('FranceInfo.png'))
  addDir('PRO TV News [RO]', "https://vid.hls.protv.ro/protvnews/protvnews.m3u8?1", setIcon('ProTVnews.png'))


def addDir(name, url, iconimage):
    iconimage = urllib.unquote(urllib.unquote(iconimage))
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&name=" + urllib.quote_plus(name) + "&thumb=" + urllib.quote_plus(iconimage)

    listedItem = xbmcgui.ListItem(name, iconImage=movies_thumb, thumbnailImage=iconimage)
    itemInfo = {
      'type': 'Video',
      'genre': 'Live Stream',
      'title': name,
      'playcount': '0'
    }
    listedItem.setInfo('video', itemInfo)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=listedItem)

    LF = open(myLogFile, 'a')
    LF.write("addDir: '" + name + "', '" + url + "', '" + iconimage + '\'\n')
    LF.close()

    return ok


def getParams():
  LF = open(myLogFile, 'a')
  LF.write("getParams getParams: '" + sys.argv[1] + '\'\n')

  param = []
  paramstring = sys.argv[2]
  if len(paramstring) >= 2:
      params = sys.argv[2]
      cleanedparams = params.replace('?', '')
      if (params[len(params) - 1] == '/'):
	  params = params[0:len(params) - 2]
      pairsofparams = cleanedparams.split('&')
      param = {}
      for i in range(len(pairsofparams)):
	  splitparams = {}
	  splitparams = pairsofparams[i].split('=')
	  if (len(splitparams)) == 2:
	      param[splitparams[0]] = splitparams[1]

  LF = open(myLogFile, 'a')
  LF.write("getParams: '" + str(param) + '\'\n')
  LF.close()
  #-----------------------------------------------------------------------------------------------------------
  #'url': 'http%3A%2F%2Ffa.euronews.com%2Flive', 'name': 'EuroNews+Live+%5BFA%5D', 'thumb': 'resources%2Fmedia%2FEuroNewsLive.png'}'
  #-----------------------------------------------------------------------------------------------------------
  LF.close()
  return param


def makeCookie(name, value, domain):
    return cookielib.Cookie(
        version=0,
        name=name,
        value=value,
        port=None,
        port_specified=False,
        domain=domain,
        domain_specified=True,
        domain_initial_dot=False,
        path="/",
        path_specified=True,
        secure=False,
        expires=None,
        discard=False,
        comment=None,
        comment_url=None,
        rest=None
    )


def is_json(myjson):
    try:
      json_object = json.loads(myjson)
    except ValueError, e:
      return False
    return True


def getPlayList(url):
  global myCookieJar
  global httpURLopener
  global playList

  LF = open(myLogFile, 'a')
  LF.write('----------------------------' + '\n')
  LF.write("getPlayList url: '" + url + '\'\n')

  httpURLopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(myCookieJar))
  httpURLopener.addheaders = [
      #('Host', host),
      ('Connection', 'keep-alive'),
      ('Accept', '*/*'),
      ('X-Requested-With', 'XMLHttpRequest'),
      ('User-Agent', userAgent),
      ('Referer', url),
      ('Accept-Encoding', 'identity'),
      ('Accept-Language', 'en-GB')
    ]

  ## DIGI 24 specical case
  if "digi24" in url:
    apiKey = None
    keyMakerUrl = "http://balancer.digi24.ro/streamer/make_key.php"
    playListUrl = None
    playListPointer = None
    playList_from_JSON = None
    try:
      apiKey = httpURLopener.open(keyMakerUrl).read()
      LF.write("apiKey: '" + str(apiKey) + '\'\n')
    except:
      xbmcgui.Dialog().ok('getPlayList Error', 'Could not access ' + keyMakerUrl)
      LF.write("getPlayList Error: Could not access '" + keyMakerUrl + '\'\n')

    if apiKey is not None:
      playListUrl = "http://balancer.digi24.ro/streamer.php?&scope=digi24&key=" + str(apiKey) + "&outputFormat=json&type=abr&quality=hq"
      LF.write("playListUrl: '" + playListUrl + '\'\n')
      try:
	playListPointer = httpURLopener.open(playListUrl).read()
	LF.write("playListPointer: '" + str(playListPointer) + '\'\n')
      except:
	xbmcgui.Dialog().ok('getPlayList Error', 'Could not access ' + playListUrl)
	LF.write("getPlayList Error: Could not access '" + playListUrl + '\'\n')

      if playListUrl is not None:
	try:
	  decoded_JSON_data = json.loads(playListPointer)
	  playList_from_JSON = decoded_JSON_data['file']
	  LF.write("playList_from_JSON: '" + playList_from_JSON + '\'\n')
	except:
	  xbmcgui.Dialog().ok('getPlayList Error', 'Could not access ' + playListPointer)
	  LF.write("getPlayList Error: Could not access '" + playListPointer + '\'\n')

	if playList_from_JSON is not None:
	  if "http://" not in playList_from_JSON:
	    playList = "http:" + playList_from_JSON
	  else:
	    playList = playList_from_JSON
	  LF.write("playList: '" + playList + '\'\n')

    else:
      xbmcgui.Dialog().ok('getPlayList Error', 'Could not access' + keyMakerUrl)
      LF.write("getPlayList Error: Could not access '" + keyMakerUrl + '\'\n')

  else:
    try:
      playListPointer = httpURLopener.open(url).read()
      LF.write("playListPointer: '" + str(playListPointer) + '\'\n')
    except:
      xbmcgui.Dialog().ok('getPlayList Error', 'Could not access ' + url)
      LF.write("getPlayList Error: Could not access '" + url + '\'\n')

    ## FranceInfo adds a comment in front of the JSON data
    if "_jsonp_loader_callback_request_0(" in playListPointer:
      playListPointer = trimSubstrEnd(playListPointer, "_jsonp_loader_callback_request_0(")
      playListPointer = trimSubstr(playListPointer, ")")

    ## Check if result is a valid JSON, if so: get the playlist
    if is_json(playListPointer):
      try:
	decoded_JSON_data = json.loads(playListPointer)
	playList_from_JSON = decoded_JSON_data['url']
      except:
	xbmcgui.Dialog().ok('getPlayList Error', 'Could not access ' + url)
	LF.write("getPlayList Error: Could not access '" + url + '\'\n')

      ## FranceInfo: playList_from_JSON already contains the playlist
      if "hdfauthftv-a.akamaihd.net" in url:
	  playList = playList_from_JSON
	  LF.write('----------------------------' + '\n')
	  LF.write('playList: ' + playList + '\n')
	  LF.write('----------------------------' + '\n')
      else:
	## Correct the Euronews URL retrieved in JSON
	if "http://" not in playList_from_JSON:
	  playList_from_JSON = "".join(("http:", playList_from_JSON))

	## List cookies if any
	for cookie in (myCookieJar):
	  LF.write("getPlayList cookie: " + str(cookie) + '\n')
	LF.write("decoded_JSON_data: '" + str(decoded_JSON_data) + '\'\n')

	try:
	  playListJSON = httpURLopener.open(playList_from_JSON).read()
	except:
	  xbmcgui.Dialog().ok('getPlayList Error', 'Could not access ' + playList_from_JSON)
	  LF.write("getPlayList Error: Could not access '" + playList_from_JSON + '\'\n')

	decoded_JSON_data = json.loads(playListJSON)
	## EuroNews Specific
	if "euronews.com" in url:
	  #playList = decoded_JSON_data['primary']
	  playList = decoded_JSON_data['backup']

	LF.write("----------------------------"+'\n')
	LF.write("playListJSON: '" + playListJSON + '\'\n')
	LF.write("playList: '" + playList + '\'\n')
	LF.write("----------------------------"+'\n')

    ## Result is not JSON
    else:
      playList = url

    ## Log Playlist
    if playList is not None:
      try:
	playListContent = httpURLopener.open(playList).read()
	LF.write(playListContent)
	LF.write('----------------------------' + '\n')
      except:
	xbmcgui.Dialog().ok('getPlayList Error', 'Could not access ' + playList)
	LF.write("getPlayList Error: Could not access '" + playList + '\'\n')

  LF.close()


def parseInput(url):
    global playList
    playList = None
    item = None

    getPlayList(url)
    LF = open(myLogFile, 'a')

    ## Build ListItem
    if playList is not None:
      try:
	item = xbmcgui.ListItem(path=playList, iconImage=addon_thumb, thumbnailImage=nowPlayingThumb)
	itemInfo = {
	  'type': 'Video',
	  'genre': 'Live Stream',
	  'title': nowPlayingTitle,
	  'playcount': '0'
	}
	item.setInfo('video', itemInfo)
      except:
	xbmcgui.Dialog().ok('Error', 'Could not access media')
	LF.write("Build ListItem: Could not access '" + playList + '\'\n')

    ## Play stream
    if item is not None and playList is not None:
      LF.write("xbmc.Player().play(" + playList + "," + str(item) + ")" + '\n')
      try:
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.Player().play(playList, item)
      except:
	xbmcgui.Dialog().ok('Error', 'Could not play media')
	LF.write("Error: Could not play media")

    else:
      xbmcgui.Dialog().ok('Error', 'Could not access ' + url)
      LF.write("Error: Could not access '" + url + '\'\n')
    LF.close()


#### RUN Addon ###
params = getParams()
url = None
host = None
nowPlayingThumb = None
nowPlayingTitle = None
httpURLopener = None
playList = None
myCookieJar = cookielib.CookieJar()

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass

try:
  nowPlayingTitle = urllib.unquote_plus(params["name"])
except:
  nowPlayingTitle = str(url)

try:
  nowPlayingThumb = urllib.unquote_plus(params["thumb"])
except:
  nowPlayingThumb = movies_thumb

if url is None or len(url) < 1:
  ROOT()
else:
  parseInput(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

####################################################################################################
