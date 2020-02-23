import hashlib
import configparser
from urllib.request import urlopen
from xml.etree.ElementTree import parse
from zwift import Client


def r_îni_file():
    r_ini_object = configparser.ConfigParser()
    r_ini_object.read('FBox.ini')
    return r_ini_object

def start_vent(cmd):
#start connection
    fritzurl = URL
#check SID
    with urlopen(fritzurl + '/login_sid.lua') as f:
        dom = parse(f)
        sid = dom.findtext('./SID')
        challenge = dom.findtext('./Challenge')

    if sid == '0000000000000000':
        md5 = hashlib.md5()
        md5.update(challenge.encode('utf-16le'))
        md5.update('-'.encode('utf-16le'))
        md5.update(PASS.encode('utf-16le'))
        response = challenge + '-' + md5.hexdigest()
        uri = fritzurl + '/login_sid.lua?username=' + USER + '&response=' + response
    with urlopen(uri) as f:
        dom = parse(f)
        sid = dom.findtext('./SID')

    uri = fritzurl + '/webservices/homeautoswitch.lua?ain=' + AIN + '&switchcmd=' + cmd + '&sid=' + sid
    urlopen(uri)



config =  r_îni_file()

URL = config.get('FritzBox', 'FBoxURL')
USER = config.get('FritzBox', 'FBoxUSER')
PASS = config.get('FritzBox', 'FBoxPass')
AIN = config.get('FritzBox', 'FBoxAIN')
cmdon = config.get('FritzBox', 'FBoxcmdon')
cmdoff = config.get('FritzBox', 'FBoxcmdoff')
username = config.get('Zwift', 'Zwiftusername')
password = config.get('Zwift', 'Zwiftpassword')
player_id = config.getint('Zwift', 'Zwiftplayer_id')
VentOn = config.getint('Vent', 'HBVentOn')
VentOff = config.getint('Vent', 'HBVentOff')

#login zwift
while True:
    try:
        client = Client(username, password)
        world = client.get_world(1)
        benutzer = world.player_status(player_id)

        if benutzer.player_state.heartrate > VentOn:
            start_vent(cmdon)
        if benutzer.player_state.heartrate <= VentOff:
            start_vent(cmdoff)
        print('Program is still runing...everything is OK!!')
    except KeyboardInterrupt:
        print ('Programm wird beendet')
        raise

###########
#change in request.py the protobuf def!!!
#
#    def protobuf(self, url):
#        headers = self.get_headers(accept_type='application/x-protobuf-lite')
#       resp = requests.get(self.BASE_URL + url, headers=headers)
#        if resp.status_code == 404:
#            print('Rider not yet found on Zwift')
#        elif not resp.ok:
#            raise RequestException("{} - {}".format(
#                resp.status_code, resp.reason))
#        return resp.content
