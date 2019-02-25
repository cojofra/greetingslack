import websocket
import json
import requests
import urllib
import os
import sys
import logging



logging.basicConfig(level=logging.DEBUG,
        stream=sys.stdout)

# Suppress InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

MESSAGE_EMP = os.environ['WELCOME_MESSAGE_EMP']
MESSAGE_GUE = os.environ['WELCOME_MESSAGE_GUE']
TOKEN = os.environ['SLACK_TOKEN']
CHANNELS = json.loads(os.environ['CHANNELS_TO_MONITOR'])
UNFURL = os.environ['UNFURL_LINKS']

###############################################################

def is_tc_channel_join(msg):
    return msg['type'] == "member_joined_channel" and msg['channel'] in CHANNELS and msg['channel_type'] == 'C'

def get_user_info(user_id):
    logging.debug('FINDING USER WITH ID: '+user_id)
    resp = requests.get("https://slack.com/api/users.info?token="+TOKEN+"&user="+user_id)
    resp = resp.json()

    user_info = {
        'real_name':resp['user']['real_name'],
        'type':'guest' if resp['user']['is_restricted'] or resp['user']['is_ultra_restricted'] else 'employee',
    }
    return user_info

def parse_join(message):
    m = json.loads(message)
    logging.debug(m)
    if is_tc_channel_join(m):
        user_id = m["user"]
        user_info = get_user_info(user_id)
        channel_id = m['channel']
        logging.debug(m)

        # Different message based on user type
        data = {
            'token': TOKEN,
            'channel': channel_id,
            'text': MESSAGE_EMP if user_info['type'] == 'employee' else MESSAGE_RES,
            'user': user_id,
            'parse': 'full',
            'as_user': 'true',
        }

        logging.debug(data)

        if (UNFURL.lower() == "false"):
          data = data.update({'unfurl_link': 'false'})

        xx = requests.post("https://slack.com/api/chat.postEphemeral", data=data)
        logging.debug('\033[91m' + "HELLO SENT TO " + user_info['real_name'] + '\033[0m')

#Connects to Slacks and initiates socket handshake
def start_rtm():
    
    r = requests.get("https://slack.com/api/rtm.start?token="+TOKEN, verify=False)
    r = r.json()
    logging.info(r)
    r = r["url"]
    return r

def on_message(ws, message):
    parse_join(message)

def on_error(ws, error):
    logging.error("SOME ERROR HAS HAPPENED: " + error)

def on_close(ws):
    logging.info('\033[91m'+"Connection Closed"+'\033[0m')

def on_open(ws):
    logging.info("Connection Started - Auto Greeting new joiners to specific channels")


if __name__ == "__main__":
    r = start_rtm()
    ws = websocket.WebSocketApp(r, on_message = on_message, on_error = on_error, on_close = on_close)
    #ws.on_open
    ws.run_forever()