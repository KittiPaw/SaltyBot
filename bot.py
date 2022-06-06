# bot.py
import os  # for importing env vars for the bot to use
from twitchio.ext import commands
from datetime import datetime

red_count = 0
blue_count = 0
red_all_in = False
blue_all_in = False
poss_blue_all = 0
poss_red_all = 0
latest_bet = datetime.now()
balances = {}


class Bot(commands.Bot):

    def __init__(self):
        red_count = 0
        blue_count = 0
        red_all_in = False
        blue_all_in = False
        super().__init__(token=os.environ['TMI_TOKEN'], prefix=os.environ['BOT_PREFIX'], initial_channels=[
            os.environ['CHANNEL']])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        print("Current total")
        print("* Denotes that there was an all-in, undetermined amount")

    async def event_message(self, message):
        if(message.author.name == 'malphite_bot'):
            global red_count
            global blue_count
            global poss_blue_all
            global poss_red_all
            global latest_bet
            global red_all_in
            global blue_all_in
            global balances
            messageSplit = message.content.split(' ')
            username = messageSplit[0]
            # have {balance}
            # balance is {balance}
            BALANCE_IS = 'balance is '
            HAVE = 'have '
            balanceIndex = message.content.find(BALANCE_IS)
            haveIndex = message.content.find(HAVE)
            print("balance index = {}".format(balanceIndex))
            print("have index = {}".format(haveIndex))
            if(balanceIndex != -1):
                balanceIndex += len(BALANCE_IS)
                possibleBalance = message.content[balanceIndex:].split(' ')[0].replace(',', '').replace('‚', '')
                if(possibleBalance.isnumeric()):
                    balances[username] = int(possibleBalance)
                    #print("Updated user {}'s balance to {}".format(username, int(possibleBalance)))
            elif(haveIndex != -1):
                haveIndex += len(HAVE)
                possibleBalance = message.content[haveIndex:].split(' ')[0].replace('‚', '').replace(',', '')
                if(possibleBalance.isnumeric()):
                    balances[username] = int(possibleBalance)
                    #print("Updated user {}'s balance to {}".format(username, int(possibleBalance)))
            if(messageSplit[1] == 'You' and messageSplit[2] == 'placed'):
                if((datetime.now() - latest_bet).total_seconds() > 300):
                    red_count = 0
                    blue_count = 0
                    red_all_in = False
                    blue_all_in = False
                    poss_blue_all = 0
                    poss_red_all = 0
                if('all' in message.content):
                    teamColor = messageSplit[8]
                    if(teamColor == 'RED.'):
                        red_all_in = True
                        if username in balances:
                            poss_red_all += balances[username]
                    if(teamColor == 'BLUE.'):
                        blue_all_in = True
                        if username in balances:
                            poss_blue_all += balances[username]
                else:
                    amount = int(messageSplit[3].replace(',', ''))
                    teamColor = messageSplit[6]
                    if(teamColor == 'RED.'):
                        red_count = red_count + amount
                    if(teamColor == 'BLUE.'):
                        blue_count = blue_count + amount
                latest_bet = datetime.now()
                response = ""
                response = response + "Blue: " + str(blue_count)
                if(blue_all_in):
                    response = response + "*"
                    response += ' PAI: ' + str(poss_blue_all) 
                response = response + " Red: " + str(red_count)
                if(red_all_in):
                    response = response + "*"
                    response += ' PAI: ' + str(poss_blue_all) 
                print("\t\t\t\t\t\t", end='\r')
                print(response, end='\r')

        await self.handle_commands(message)


if __name__ == "__main__":
    bot = Bot()
    bot.run()
