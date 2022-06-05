# bot.py
import os # for importing env vars for the bot to use
from twitchio.ext import commands
from datetime import datetime

red_count=0
blue_count=0
red_all_in=False
blue_all_in=False
latest_bet=datetime.now()

class Bot(commands.Bot):

    def __init__(self):
        red_count=0
        blue_count=0
        red_all_in=False
        blue_all_in=False
        super().__init__(token=os.environ['TMI_TOKEN'], prefix=os.environ['BOT_PREFIX'], initial_channels=[os.environ['CHANNEL']])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        print("Current total")
        print("* Denotes that there was an all-in, undetermined amount")

    async def event_message(self, message):
        if(message.author.name == 'malphite_bot'):
            global red_count
            global blue_count
            global latest_bet
            global red_all_in
            global blue_all_in
            messageSplit=message.content.split(' ')
            if(messageSplit[1] == 'You' and messageSplit[2] == 'placed'):
                if((datetime.now() - latest_bet).total_seconds() > 300):
                    red_count=0
                    blue_count=0
                    red_all_in=False
                    blue_all_in=False
                if('all' in message.content):
                    teamColor = messageSplit[8]
                    if(teamColor == 'RED.'):
                        red_all_in = True
                    if(teamColor == 'BLUE.'):
                        blue_all_in = True
                else:
                    amount = int(messageSplit[3].replace(',', ''))
                    teamColor = messageSplit[6]
                    if(teamColor == 'RED.'):
                        red_count = red_count + amount
                    if(teamColor == 'BLUE.'):
                        blue_count = blue_count + amount
                latest_bet=datetime.now()
                response = ""
                response = response + "Blue: " + str(blue_count)
                if(blue_all_in):
                    response = response + "*"
                response = response + " Red: " + str(red_count)
                if(red_all_in):
                    response = response + "*"
                print("\t\t\t\t\t\t", end='\r')
                print(response, end='\r')


        await self.handle_commands(message)




if __name__ == "__main__":
    bot = Bot()
    bot.run()