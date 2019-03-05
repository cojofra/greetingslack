# -*- coding: utf-8 -*-
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

TOKEN = os.environ['SLACK_TOKEN']
UNFURL = os.environ['UNFURL_LINKS']

###############################################################
toronto = {
    'city_name': "Toronto",
    'slack_handles':"*<@TC-Team-Toronto>*",
}
sf = {
    'city_name': "San Francisco",
    'slack_handles':"*<@TC-Team-SF>*",
}
boston = {
    'city_name': "Boston",
    'slack_handles':"*<@TC-Team-Boston>*",
}

employee_global = """[
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ":wave: Welcome to the global Technology Centers slack channel, where Autodesk employees can connect with Technology Center residents; to read about - as well as share - exciting, relevant updates including invites or links to presentations and speakers."
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "A few simple guidelines to remember about this channel:"
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "1. :loudspeaker: *This is a PUBLIC channel. Do not share Autodesk IP.*\n2. :question: If you have any questions about the technology center itself - how to book a conference room, or our workshop policies for example, just ask <@niles>! If he doesn’t know the answer, he will find someone who does."
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "We’ve also created some helpful handles for you to reach specific people at the different technology centers.\n *<@TC-Team-Toronto>* - Toronto Community Team\n*<@TC-Team-SF>* – San Francisco Community Team\n*<@TC-Team-Boston>* - Boston Community Team"
        }
    },
    {
        "type": "context",
        "elements": [
            {
                "type": "plain_text",
                "text": "Your Autodesk Technology Center Team",
                "emoji": true
            }
        ]
    }
]"""

employee_local = """[
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ":wave: Welcome to the local Technology Center %s slack channel, where Autodesk employees can connect with Technology Center residents; to read about - as well as share - exciting, relevant updates including invites or links to presentations and speakers."
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "A few simple guidelines to remember about this channel:"
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "1. :loudspeaker: *This is a PUBLIC channel. Do not share Autodesk IP.*\n2. :question: If you have any questions about the technology center itself - how to book a conference room, or our workshop policies for example, just ask <@niles>! If he doesn’t know the answer, he will find someone who does."
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "You can reach the local community team with this slack group %s"
        }
    },
    {
        "type": "context",
        "elements": [
            {
                "type": "plain_text",
                "text": "Your Autodesk Technology Center Team",
                "emoji": true
            }
        ]
    }
]"""

resident_global = """[
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ":wave: Welcome to the Global Technology Centers slack channel where you can connect with fellow resident teams as well as Autodesk employees across all the tech centers. This is the place to read about - as well as share - exciting, relevant updates including invites or links to presentations and speakers."
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "A few simple guidelines to remember about this channel:"
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "1. :loudspeaker: *This is channel is accessible by all of Autodesk. Do not share any sensitive IP.*\n2. :cityscape: You have also been added to your site-specific tech center channel. That’s the place to find information about local tech center events and updates.\n3. :question: If you have general questions about the technology centers (how to book conference rooms or workshop policies, for example), just ask @niles. If he doesn’t know the answer, he will find someone who does."
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "We’ve also created some helpful handles for you to reach specific people at the different technology centers.\n *<@TC-Team-Toronto>* - Toronto Community Team\n*<@TC-Team-SF>* - San Francisco Community Team\n*<@TC-Team-Boston>* - Boston Community Team\nIn this channel you can also reach your fellow global residents directly."
        }
    },
    {
        "type": "context",
        "elements": [
            {
                "type": "plain_text",
                "text": "Your Autodesk Technology Center Team",
                "emoji": true
            }
        ]
    }
]"""

resident_local = """[
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ":wave: Welcome to your local Technology Center %s slack channel where you can connect with other residents, your community team, and employees in the space. This is the place to read about - as well as share - exciting, relevant updates including invites or links to presentations and speakers."
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "A few simple guidelines to remember about this channel:"
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "1. :loudspeaker: *This is channel is accessible by all of Autodesk. Do not share any sensitive IP.*\n2. :cityscape: This is your site-specific channel and it’s the place to find information about local tech center events and updates.\n3. :question: If you have general questions about the technology centers (how to book conference rooms or workshop policies, for example), just ask @niles. If he doesn’t know the answer, he will find someone who does."
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "You can reach the local community team and your fellow residentsin here. Use %s for your local community team."
        }
    },
    {
        "type": "context",
        "elements": [
            {
                "type": "plain_text",
                "text": "Your Autodesk Technology Center Team",
                "emoji": true
            }
        ]
    }
]"""

tc_channels = {
    'CA405J807': {
        'employee': employee_global,
        'resident': resident_global,
    },
    'CFVV9V35W' : {
        'employee': employee_local % (boston['city_name'],
            boston['slack_handles']),
        'resident': resident_local % (boston['city_name'],
            boston['slack_handles']),
    },
    'CFZJUL20N' : {
        'employee': employee_local % (sf['city_name'],sf['slack_handles']),
        'resident': resident_local % (sf['city_name'],sf['slack_handles']),
    },
    'CFZUUDHU2' : {
        'employee': employee_local % (toronto['city_name'],
            toronto['slack_handles']),
        'resident': resident_local % (toronto['city_name'],
            toronto['slack_handles']),
    },
}

def is_tc_channel_join(msg):
    return msg['type'] == "member_joined_channel" and msg['channel_type'] == 'C' and msg['channel'] in tc_channels

def get_user_info(user_id):
    logging.debug('FINDING USER WITH ID: '+user_id)
    resp = requests.get("https://slack.com/api/users.info?token="+TOKEN+
        "&user="+user_id)
    resp = resp.json()

    user_info = {
        'real_name':resp['user']['real_name'],
        'type':'resident' if resp['user']['is_restricted'] or resp['user']['is_ultra_restricted'] else 'employee',
    }
    return user_info

def parse_join(message):
    m = json.loads(message)
    if is_tc_channel_join(m):
        user_id = m["user"]
        user_info = get_user_info(user_id)
        channel_id = m['channel']
        logging.debug(m)

        # Different message based on user type
        data = {
            'token': TOKEN,
            'channel': channel_id,
            'text': """Welcome to the Global Technology Centers Slack channel,
                where Autodesk employees can connect with Technology Center
                residents; to read about - as well as share - exciting,
                relevant updates including invites or links to presentations
                and speakers. If you have any operational questions, ask
                <@niles>""",
            'blocks': tc_channels[channel_id][user_info['type']],
            'user': user_id,
            'parse': 'full',
            'as_user': 'true',
        }

        logging.debug(data)

        if (UNFURL.lower() == "false"):
          data = data.update({'unfurl_link': 'false'})

        xx = requests.post("https://slack.com/api/chat.postEphemeral",
            data=data)
        logging.debug('\033[91m' + "HELLO SENT TO " + user_info['real_name'] +
            '\033[0m')

#Connects to Slacks and initiates socket handshake
def start_rtm():

    r = requests.get("https://slack.com/api/rtm.start?token="+TOKEN,
        verify=False)
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
