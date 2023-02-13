#-------IMPORTS-------

import discord
from discord.ext import commands
import random
import os #For finding .env
from dotenv import load_dotenv,find_dotenv 
import mysql.connector
#import requests
#import json

#.env GRAB, API KEYS, GLOBALS, AND BOT INITIALIZIATION 
#---------------------------------------------------------
load_dotenv(find_dotenv()) #Find .env file in directory
key= os.getenv('DISCORDKEY') #Grab the variable from .env file called 'discordkey' (API KEY)
commandpref = os.getenv('DISCBOTPREF')
#Discord API setup stuff:
intent = discord.Intents.default()
intent.members = True
intent.message_content = True
#client = discord.Client(intents=intent)
activity = discord.Activity(name='roblox love', type=discord.ActivityType.watching)
client = commands.Bot(command_prefix=commandpref, intents=intent, activity = activity)

passwrd= os.getenv('MYSQLPASSWORD') #MySQL password to connect to local database.
dict = { #Login info for MySQL
    'host': '127.0.0.1',
    'database':'discordbot',
    'user' : 'root',
    'password': passwrd
}
database = mysql.connector.connect(**dict) #Connect to database using login info.
print("MYSQL CONNECTION SUCCESSFUL")

#------------------------START---------------------------

@client.event
async def on_ready():
    print("Logged in as {.user}".format(client))
    print("--------------------------------\n")

#----------------------END START-------------------------

#------------------------GENERAL---------------------------
#Globals:
randNum = 2 #For welcome message.

@client.event
async def on_member_join(member):
    global randNum
    entryMessagesDict = {1:"Welcome to the server, " + member.name + "!",2:"Glad you came, " + member.name + "!", 3: "Look what the dogs dragged in. You look like shit, " + member.name + ", come in and get washed up."}
    await member.send("Hello, " +member.name + ", welcome to my development server! I'm still in development, so don't mind me. ;)") #DM's the user who joined a welcome message.
    channel = client.get_channel(1052802486978756670) #Channel ID for general chat for our server (hardcoded)
    await channel.send(entryMessagesDict[randNum]) #Sends message to the channel we just defined.
    print(member, "\n", randNum) #Prints the member who joined into terminal.
    if randNum == 3:
        randNum = 1
        return
    randNum+= 1

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1052802486978756670) #Channel ID for general chat for our server (hardcoded)
    await channel.send(member.name + " just left the server, bro " + member.name + " u suck lol")
    print(member)

@client.command(pass_context = True)
async def join(ctx): #Joins voice channel
    print(ctx)
    print(ctx.message)
    if(ctx.author.voice): #If the user is in a voice channel
        channel = ctx.message.author.voice.channel #Grab the voice channel
        await channel.connect() #Connect to it
    else:
        await ctx.send("bruh u aint in no channel :sob:")

@client.command(pass_context = True)
async def leave(ctx): #Leave voice channel
    if(ctx.voice_client): #If bot is in a voice channel
        await ctx.guild.voice_client.disconnect() #Disconnect
        await ctx.send("Im gone bru")
    else:
        await ctx.send("bruh i aint in no channel :sob:")

@client.command()
async def hello(ctx):
    await ctx.send("Hello bozo")

@client.command()
async def work(ctx):
    userID = ctx.message.author.id
    Cursor = database.cursor(buffered=True)
    currsql = "SELECT currency FROM initialtable WHERE discordID = %s" #Check for discordID from author in database
    Cursor.execute(currsql, [userID]) #Execute
    for x in Cursor:
        usercurrency = x[0]
    paycheck = random.randint(36, 61)
    paysql = "UPDATE initialtable SET currency = currency + {} WHERE discordID = %s".format(paycheck)
    Cursor.execute(paysql,[userID])
    database.commit()

    #await ctx.message.channel.send("Thanks for workin, " + ctx.author.mention + ". You got $" + str(paycheck) + ", so now you got $" + str(usercurrency + paycheck) + ".")
    print(usercurrency)
    print("Thanks for workin, " + ctx.author.mention + ". You got $" + str(paycheck) + ", so now you got $" + str(usercurrency + paycheck) + ".")

@client.command()
async def todo(ctx):
    flag = ctx.message.content.split(" ")[1].lower()
    if flag == "view":
        pass

#--------------------END OF GENERAL-----------------------
@client.command()
async def show(ctx):
    Cursor = database.cursor(buffered = True) #Initialize instance to interact with database, buffered allows object to be declared multiple times during runtime.
    Cursor.execute("SELECT discordID FROM initialtable") #Select all discord ID's from the table.
    for x in Cursor: #For every value grabbed by MySQL within this object
        await ctx.send(x[0]) #Print them to the channel
#------------------------GAMES---------------------------

#Globals:
playerList = []
roulettecounter = 0
startflag = False #If false, players join, if true, game starts.
roulettemessage = "holder"
#-----------------ROULETTE-----------------
@client.command()
async def roulette(ctx):
    global startflag
    if(startflag): #If join message was already sent:
        await ctx.message.channel.send("Welcome to roulette. There will be one bullet loaded into the gun. I will aim the gun at the current user and pull the trigger. If you get shot, you're dead. If you don't, you're still in and keep playing.")
        await ctx.message.channel.send("Say 'Selenity shoot' when you're ready. " + playerList[roulettecounter].mention + ", you're up first :)")
        return
    #playerList.append(ctx.message.author)
    global roulettemessage
    print(roulettemessage)
    if roulettemessage != "holder": #Doesnt work
        roulettemessage.delete() #Doesnt work, is supposed to delete last roulette message sent by Selenity.
    roulettemessage = await ctx.message.channel.send("Anyone who wants to join gotta react with '✅', including you, " + ctx.message.author.mention + ".")
    await roulettemessage.add_reaction('✅') #Add initial reaction to message for people to join.
    startflag = True #So for next time command is called, it is to start the game.

@client.command()
async def shoot(ctx):
    global roulettecounter
    currentUser = playerList[roulettecounter] #Getting user whos turn it is
    chance = random.randint(1,6) #Chance to lose
    print ( chance)
    if ctx.message.author != currentUser: #If user who said command isn't the user whos turn it is
        await ctx.message.channel.send("bruh "+ ctx.message.author.mention + " get outta here u aint " + currentUser.mention + " :skull:")
        return
    if chance == 6: # You lose if you roll a 6.
        await ctx.message.channel.send("*BOOM!* You're dead, " + currentUser.mention + ". you're just unlucky asf :skull:")
        playerList.remove(currentUser) #Remove player from playerlist
        #await currentUser.kick() #Can be activated to kick the user who loses from server for fun
        await ctx.message.channel.send("Remaining players:")
        for player in playerList:
            await ctx.message.channel.send(player.name)
    else: #You didn't roll a 6, you're alive.
        await ctx.message.channel.send("*click* ig you're alive for the next round, " + currentUser.mention + " :/")

    if len(playerList) == 1: #Only one person left.
        await ctx.message.channel.send("congrats, " + playerList[0].name + ", you get to live, idk if thats a win tho tbh.")
        # Reset Globals for next game
        global startflag
        startflag = False
        playerList.clear()
        print(playerList)
        print(startflag)
    #Reset Roulette counter
    if roulettecounter < len(playerList):
        roulettecounter += 1
    elif roulettecounter >= len(playerList):
        roulettecounter = 0
    print(roulettecounter)

'''
@client.command()
async def joingame(ctx):
    if(len(playerList) < 5):
        playerList.append(ctx.message.author)
        await ctx.message.channel.send("Player " + ctx.message.author.mention + " added.")
    else:
        await ctx.message.channel.send("Game is full.")
        await ctx.message.channel.send("List of players:")
        for player in playerList:
            await ctx.message.channel.send(player.name)
        await ctx.message.channel.send("To start game, say 'Selenity roulette'.")
'''
@client.event
async def on_raw_reaction_add(ctx):
    global roulettemessage
    global startflag
    print(ctx)
    limit = 2
    #Grabbers ------
    channel = client.get_channel(ctx.channel_id)
    message = await channel.fetch_message(ctx.message_id)
    user = client.get_user(ctx.user_id)
    #---------------
    #await roulettemessage.channel.send("ctx " + str(ctx.message_id) + " global " + str(roulettemessage.id))
    if startflag: #REMOVE LATER / If not in roulette game
        return #REMOVE LATER

    if ctx.message_id != roulettemessage.id or ctx.member.name == 'Selenity': #If this message isn't the roulette message or the reaction is by Selenity, exit the function.
        return
    
    if(len(playerList) < limit): #Check to see if game is full
        if ctx.member in playerList: #If the user already reacted to join the game
            await roulettemessage.channel.send("bruh " + ctx.member.name + " you already in chill out.")
            await message.remove_reaction('✅', user) #Remove the reaction from this message
            return
        playerList.append(ctx.member) #Add user who reacted to message to playerList array
        await roulettemessage.channel.send("Player " + ctx.member.mention + " added.")
        await message.remove_reaction('✅', user)
        if len(playerList) == limit: #After adding, if game is full:
            pass #Continue on to game is full code
        else:
            return #Exit function to allow other users to join.
    await message.remove_reaction('✅', user)
    await roulettemessage.channel.send("Game is full.")
    await roulettemessage.channel.send("List of players:")
    for player in playerList:
        await roulettemessage.channel.send(player.name)
    await roulettemessage.channel.send("To start game, say 'Selenity roulette'.")

#---------------END OF ROULETTE---------------
rolldiceflag = False
@client.command()
async def rolldice(ctx): #Currency Test
    global rolldiceflag
    rolldiceflag = True
    diceroll = random.randint(1,6)
    userID = ctx.message.author.id
    Cursor = database.cursor(buffered=True)
    currsql = "SELECT currency FROM initialtable WHERE discordID = %s" #Check for discordID from author in database
    Cursor.execute(currsql, [userID]) #Execute
    for x in Cursor:
        usercurrency = x[0]
    rolldiceflag = True
    value = int(ctx.message.content.split(" ")[2])
    bet = int(ctx.message.content.split(" ")[3])
    if bet > usercurrency:
        await ctx.message.reply("Your bet is too big")
        return
    await ctx.message.channel.send("Dice has been rolled and landed on a " + str(diceroll) + ".")
    if value == diceroll:
        await ctx.message.channel.send("You win, " + ctx.message.author.mention + ".")
        addcurrsql = "UPDATE initialtable SET currency = currency + {} WHERE discordID = %s".format(bet)
        Cursor.execute(addcurrsql,[userID])
    else:
        await ctx.message.channel.send("You lose, " + ctx.message.author.mention + ".")
        subcurrsql = "UPDATE initialtable SET currency = currency - {} WHERE discordID = %s".format(bet)
        Cursor.execute(subcurrsql,[userID])
    rolldiceflag = False
    return

#-------------------BLACKJACK-------------------

    #https://deckofcardsapi.com/
    #https://www.youtube.com/watch?v=qF6zUptypGE

#------------------- END OF BLACKJACK-------------------

#---------------------END OF GAMES------------------------

#------------------------XP & LEVELS---------------------------

@client.event
async def on_message(message): #Called whenever a message is sent.
    if message.author == client.user: #If the message is from the bot:
        return #Ignore it
    await client.process_commands(message) #Process the message to see if it contains any commands.
    if message.content == 'Selenity': #Basic Selenity response
        await message.channel.send("Whats up, " + message.author.mention + "?")
    Cursor = database.cursor(buffered=True) #Initialize instance to interact with database, buffered allows object to be declared multiple times during runtime.
    checksql = "SELECT discordID FROM initialtable WHERE discordID = %s" #Check for discordID from author in database
    Cursor.execute(checksql, [message.author.id]) #Execute
    for x in Cursor: #Should only be the one discordID if user is in database, if user isn't in database, this will be skipped.
        userID = x[0] #Initialize the userID variable to be the grabbed discordID
    try:
        if userID == message.author.id: #Double checking id comparison, if user not in database, userID wont be initialized and this will throw the UnboundLocalError error.
            updatemessagesql = "UPDATE initialtable SET messages = messages + 1 WHERE discordID = %s" #Update message count
            Cursor.execute(updatemessagesql, [userID])
            database.commit() #Commit change to database
            print("Message Count Updated for " + message.author.name + ".")
    except UnboundLocalError: #Error thrown when the userID isnt initialized. i.e: The user isn't in the database already.
        addsql = "INSERT INTO initialtable (discordID, messages) VALUES (%s, 1)" #Insert authors discordID into database.
        Cursor.execute(addsql,[message.author.id])
        database.commit()
        print("User " + message.author.name + " added to database.")
        return #Exit function once user is added to database
    
    checklevelsql = "SELECT messages, userlevel FROM initialtable WHERE discordID = %s" #Check for discordID from author in database and select their messages value
    Cursor.execute(checklevelsql, [message.author.id]) #Execute
    for y in Cursor: #Grabs returned values saved in cursor object from mysql
        messages = y[0] #Initialize the messages variable to be the grabbed number of messages sent by author
        level = y[1] #Initialize level variable to be the grabbed level number of author from database
    levelflag = levelhandler(messages,level)
    if levelflag:
         updatelevelsql = "UPDATE initialtable SET userlevel = userlevel + 1 WHERE discordID = %s" #Update level
         Cursor.execute(updatelevelsql, [userID])
         database.commit() #Commit change to database
         #await message.channel.send("Congrats, " + message.author.mention + "! You leveled up to level " + str(level+1) + ". You have no life fucking bozo.") #congrats message

    #----LEVEL BENCHMARKS----

def levelhandler(messagecount, level):
    levelupval = 25 #benchmark to level up
    if level == 0 and messagecount >= 15: #initial levelup
        return True
    elif messagecount >= levelupval * level * 2.2: #scaling level up
        return True
    return False


#--------------------END OF XP & LEVELS-----------------------

#------------------------ADMIN---------------------------

@client.event
async def on_message_edit(before,after):
    adminChannel = client.get_channel(1056003072951844876) #Hardcoded admin channel channelID
    await adminChannel.send("MESSAGE CHANGE LOG:\nUser: " + before.author.name + "#" + before.author.discriminator + " EDITTED MESSAGE FROM: \"" +before.content + "\"  TO: \"" + after.content + "\"." )

#---------------------END OF ADMIN------------------------

#----------------------INITIALIZE-------------------------

client.run(key) #Start bot using key grabbed from .env file.