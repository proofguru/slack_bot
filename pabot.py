#passive_aggressive slack bot v0.2

import os
import time
from slackclient import SlackClient
import openweather
import pyowm


# ID and WEATHER
BOT_ID = os.environ.get("BOT_ID")
OPEN_WEATHER_TOKEN = os.environ.get("OPEN_WEATHER_TOKEN")

# constants
AT_BOT = "<@" + BOT_ID + ">"


# instantiate Slack
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

#url for weather
owm = pyowm.OWM(OPEN_WEATHER_TOKEN)

def handle_command(command, channel):
    if 'weather' in command:
        w_dict = weather_grab()
        weather = str(w_dict.get('temp'))
        response = "The weather in Toronto is " + weather + " right now REEEE. Maybe look outside?"
        print response
    
    
    elif 'help' in command:
        response = "Hey man why don't you help yourself? Pro tip: Ask me @pabot what is the weather"
    else:
        response = "Sorry man, '" + command + "' is offensive to me"
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

#grabs the weather
def weather_grab():
    observation = owm.weather_at_place('Toronto, CA')
    weather = observation.get_weather()
    return weather.get_temperature('celsius')



def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
        """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                    output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
