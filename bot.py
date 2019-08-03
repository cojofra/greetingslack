# -*- coding: utf-8 -*-
import logging
import json
import os
import sys
import slack


logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
TOKEN = os.environ['SLACK_TOKEN']

###############################################################
# Site vars
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

# Text snippets
public_adsk = {
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "1. :loudspeaker: *This is a PUBLIC channel. Do not share Autodesk IP.*\n2. :question: If you have any questions about the technology center itself - how to book a conference room, or our workshop policies for example, just ask <@niles>! If he doesn’t know the answer, he will find someone who does."
    }
}

guidelines = {
    'type': "section",
    'text': {
        "type": "mrkdwn",
        "text": "A few simple guidelines to remember about this channel:"
    }
}

greeting = {
    "type": "context",
    "elements": [
        {
            "type": "plain_text",
            "text": "Your Autodesk Technology Center Team",
            "emoji": True
        }
    ]
}

# Employee texts
employee_global = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ":wave::wave::skin-tone-3::wave::skin-tone-5: *Welcome to the global Technology Centers slack channel*\nwhere Autodesk employees can connect with Technology Center residents; to read about - as well as share - exciting, relevant updates including invites or links to presentations and speakers."
        }
    },
    guidelines,
    public_adsk,
    {
        "type": "section",
        "text":{
            "type": "mrkdwn",
            "text": "We’ve also created some helpful handles for you to reach specific people at the different technology centers.\n*<@TC-Team-Toronto>* - Toronto Community Team\n*<@TC-Team-SF>* – San Francisco Community Team\n*<@TC-Team-Boston>* - Boston Community Team"
        }
    },
    greeting
]

employee_local = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ":wave::wave::skin-tone-3::wave::skin-tone-5: *Welcome to the local Technology Center %s slack channel*\nwhere Autodesk employees can connect with Technology Center residents; to read about - as well as share - exciting, relevant updates including invites or links to presentations and speakers."
        }
    },
    guidelines,
    public_adsk,
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "You can reach the local community team and your fellow residents here. Use %s for your local community team."
        }
    },
    greeting
]

# Resident texts
resident_global = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ":wave::wave::skin-tone-3::wave::skin-tone-5: *Welcome to the Global Technology Centers slack channel*\nwhere you can connect with fellow resident teams as well as Autodesk employees across all the tech centers. This is the place to read about - as well as share - exciting, relevant updates including invites or links to presentations and speakers."
        }
    },
    guidelines,
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "1. :loudspeaker: *This is channel is accessible by all of Autodesk. Do not share any sensitive IP.*\n2. :cityscape: You have also been added to your site-specific tech center channel. That’s the place to find information about local tech center events and updates.\n3. :question: If you have general questions about the technology centers (how to book conference rooms or workshop policies, for example), just ask @niles. If he doesn’t know the answer, he will find someone who does.\nIn this channel you can also reach your fellow global residents directly."
        }
    },
    greeting
]

resident_local = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ":wave::wave::skin-tone-3::wave::skin-tone-5: *Welcome to your local Technology Center %s slack channel*\nwhere you can connect with other residents, your community team, and employees in the space. This is the place to read about - as well as share - exciting, relevant updates including invites or links to presentations and speakers."
        }
    },
    guidelines,
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
            "text": "You can reach the local community team and your fellow residents here."
        }
    },
    greeting
]

###############################################################
# Channel list
tc_channels = {
    'CA405J807': {
        'employee': json.dumps(employee_global),
        'resident': json.dumps(resident_global),
    },
    'CFVV9V35W' : {
        'employee': json.dumps(employee_local) % (boston['city_name'],
            boston['slack_handles']),
        'resident': json.dumps(resident_local) % (boston['city_name']),
    },
    'CFZJUL20N' : {
        'employee': json.dumps(employee_local) % (sf['city_name'],sf['slack_handles']),
        'resident': json.dumps(resident_local) % (sf['city_name']),
    },
    'CFZUUDHU2' : {
        'employee': json.dumps(employee_local) % (toronto['city_name'],
            toronto['slack_handles']),
        'resident': json.dumps(resident_local) % (toronto['city_name']),
    }
}

def is_tc_channel_join(data):
    return data['channel_type'] == 'C' and data['channel'] in tc_channels

def get_user_info(user_id, web_client):
    logging.debug('FINDING USER WITH ID: '+user_id)
    user = web_client.users_info(user=user_id)['user']

    user_info = {
        'real_name':user['real_name'],
        'type':'resident' if user['is_restricted'] or user['is_ultra_restricted'] else 'employee',
    }
    return user_info

if __name__ == "__main__":
    #Connect to Slack
    @slack.RTMClient.run_on(event='member_joined_channel')
    def parse_join(**payload):
        d = payload['data']
        web_client = payload['web_client']
        if is_tc_channel_join(d):
            user_id = d["user"]
            user_info = get_user_info(user_id, web_client)
            channel_id = d['channel']
            # logging.debug(d)

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
            web_client.chat_postEphemeral(**data)

            logging.debug('\033[91m' + "HELLO SENT TO " + user_info['real_name'] +
                '\033[0m')
    rtm_client = slack.RTMClient(token=TOKEN)
    rtm_client.start()
