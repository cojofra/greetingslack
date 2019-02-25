# Greetings Slackers
This simple script written in basic Python will allow you to hook into the real time API of Slack and perform an ephemeral message greeting to every new joiner!
Usually this is used to tell new joiners about the network, the guidelines, rules, useful links etc etc

I forked this from original code by orliesaurus. New to programming or don't know how to get started just yet? Don't fret! @izzydoesizzy wrote an amazing step by step, [tutorial with screenshot](https://medium.com/@izzydoesizzy/create-a-slack-bot-that-privately-greets-new-users-in-5-easy-steps-a38eabeabcb5)

# Requirements
Python 2.7+
Edit `bot.py` in the except portion to customise with your greeting and token

# Installation
```bash
git clone <thisgitrepo>
cd <thisgitrepo>
virtualenv greetingslack
. greetingslack/bin/activate
pip install requests
pip install websocket-client
python bot.py &
```

# Heroku
Deploy with a click supported now

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

🔥 **DONT FORGET TO SCALE YOUR FREE DYNO**

# Q&A

## Q1. How do you change the welcome message?
A1.
To change the welcome message, edit your Heroku variables:
Go to Heroku's Settings, then  where it says `Config Variables` click `Reveal Config Vars` and it will reveal your message and other fields.  This will restart your Heroku instance pretty quickly and apply the changes for you

## Q2. How do I know if it worked?
A2.
After setting up the bot, your welcome message will be displayed to every new user, as soon as a they join the given slack channel - as an ephemeral message. That means it is posted in the channel, but only visible to that user.

## Q3. How do I add the channels I want to monitor?
A3.
In the `Config Variables` variables in heroku, add all the channel ids to the appropriate variable, following this syntax ["Var1","Var2","Var3"]. The channel ids can be retrieved by going to slack in your browser and opening the right channel. The id is displayed in the url after `messages/` and before `/convo`.

## Q4. Can I add attachments?
A4.
Attachments in slack lingo are links or other info that is formatted in a special way. Right now that is not possible yet, but it is to come.

## Q5. What is the differentiation between full-time employees and guests?
A5.
I have the need to send different messages to full users of the slack (full employees of the company) and external guests. Those guests can either be single or multi-channel users.