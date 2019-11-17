import logging
import pprint
import subprocess as sp
from xml.etree import ElementTree as ET

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

pp = pprint.PrettyPrinter(indent=2)

it = ET.iterparse('playlist.xspf')
# remove XML namespace
# we all hate XML (tm)
for _, el in it:
    prefix, has_namespace, postfix = el.tag.partition('}')
    if has_namespace:
        el.tag = postfix  # strip all namespaces
document = it.root

'''
    <track>
      <title>Sky Sport News HD</title>
      <location>https://eventhlshttps-i.akamaihd.net/hls/live/263645/ssn-hd-https/index.m3u8</location>
    </track>
'''

# iter through all tracks
for track in document.findall('trackList/track'):
    title = track.find('title').text
    location = track.find('location').text

    log.debug('testing channel: %s', title)
    log.debug('\turl: %s', location)
    cmd = ['timeout', '10', 'ffprobe', '-hide_banner', location]
    p = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    if p.returncode != 0:
        log.error('Stream %s  NOT healthy', title)
        log.debug('STDOUT: %s', p.stdout)
        log.debug('STDERR: %r', p.stderr)
    # pp.pprint(title)

