import os 
from slackclient import SlackClient

BOT_NAME = 'pabot'

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
print os.environ.get('SLACK_BOT_TOKEN')
if __name__ == "__main__":
	api_call = slack_client.api_call("users.list")
	if api_call.get('ok'):
		#retrieve all users so bot is findable 
		users = api_call.get('members')
		for user in users: 
			if 'name' in user and user.get('name') == BOT_NAME:
				print("Bot ID for '" + user['name'] + "' is " + user.get('id'))

	else:
		print("sorry couldn't find the bot with name " + BOT_NAME)
