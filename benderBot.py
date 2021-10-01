#!/usr/bin/python
import requests
import re
import sys
import os
from pprint import pprint
import subprocess
import json
import markovify
import sys
import settings
from markov import marky# marky chat
from Tommy import ohHai
from Tommy import catchFootball
import menuOpts
from commonWords import getCommonWords

#TODO Sexism

# Bot Globals
Auth = "" 
BotID = ""
groupID = ""
BotName = ""
confFileName = "config.txt"

# MEDALS (Defaults)
bronze = 0 
silver = 0
gold = 0
platinum = 0 
diamond = 0 

# GLOBAL STRUCTURES
Users = {}
allComs = []

class bot():
    name = ""
    botID = ""
    commentsURL = ""
    def __init__(self):
        global Auth
        global groupID
        global BotName
        global BotID
        self.name = BotName
        self.botID = BotID
        self.commentsURL = "https://api.groupme.com/v3/groups/" + groupID + "/messages?token="+Auth+"&limit=100"

class user():
    userID = ""
    name = ""
    # array of comments?
    coms = []
    # num of comments posted
    numPosts = 0
    # array of amount of likes on comments
    likes = []
    # Amount of self likes on posts under 7
    shameLikes = 0
    broMedal = 0
    silMedal = 0
    golMedal = 0
    plaMedal = 0
    diaMedal = 0

    def __init__(self, userID, name):
        global diamond
        self.userID = userID
        self.name = name
        self.coms = []
        numPosts = 0
        self.shameLikes = 0
        broMedal = 0
        silMedal = 0
        golMedal = 0
        plaMedal = 0
        diaMedal = 0
        self.likes = []
        for x in range(0,diamond+1):
            self.likes.append(0)
        
    def addToComs(self,com):
        global gold
        # com is a json for comment!
        # add to list of comments
        self.coms.append(com)
        self.numPosts+=1
        # figure out value of likes
        numFavs = len(com["favorited_by"])
        # check for shame likes
        if numFavs < gold:
            for x in com["favorited_by"]:
                # if self is in chat and its less than 7, SHAME
                if x == self.userID:
                    self.shameLikes += 1
                    numFavs -= 1
                    
        self.likes[numFavs] += 1 
        
    def numLikes(self):
        total = 0
        multi = 0
        for x in self.likes:
            total += multi * x
            multi += 1
        return total
    def calcMedals(self):
        # GET VALUES FROM CONFIG.TXT
        global bronze
        global silver
        global gold
        global platinum
        global diamond
        place = 0
        for x in self.likes:
            if place >= bronze:
                self.broMedal+=x
            if place >= silver:
                self.silMedal+=x
            if place >= gold:
                self.golMedal+=x
            if place >= platinum:
                self.plaMedal+=x
            if place >= diamond:
                self.diaMedal+=x
            place+=1

def getTokens(prin = True):
    # pull tokens from seperate file
    global groupID
    global Auth
    global BotID
    global BotName
    global confFileName
    global bronze
    global silver
    global gold
    global platinum
    global diamond

    # open file
    with open(confFileName) as f:
        content = f.readlines()
    # remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content] 
    Auth = content[0]
    groupID = content[1]
    BotID = content[2]
    BotName = content[3]
    name = content[4]
    medalList = content[5].split(',')

    diamond = int(medalList[0])
    platinum = int(medalList[1])
    gold = int(medalList[2])
    silver = int(medalList[3])
    bronze = int(medalList[4])

    if prin:
        print ("File: " + confFileName + "\nTokens Used Below: ")
        print ("Auth Token: " + Auth)
        print ("BotName: " + BotName)
        print ("BotID: " + BotID)
        print ("groupID: " + groupID)

def comment(bot, burp):
    # posts comment to groupme
    payload={"bot_id":bot.botID, "text":burp}
    r = requests.post("https://api.groupme.com/v3/bots/post",params=payload)
    print(r)


def generateContent(bot):
    # DIFF KEEPING
    # get json of all comments, store each message as an object, [0] = latest
    # also generate Users!
    global allComs
    global Users
    # Get Data File
    lastCommentSaved = None # stores the ID of the last comment 
    data = "" # stores json files
    try:
        fileBig = open("DATA.json","r")
        data = fileBig.read()
        fileBig.close()
        # find first comment ID
        idPos = data.find("\"id\"") # find location
        idPos += 7 # shift it over by one
        lastPos = idPos 
        while str(data[lastPos]) != "\"": # find last number
            lastPos+=1
        print ("DATA FOUND, LAST COMMENT ID IS : " + str(data[idPos:lastPos]))
        lastCommentSaved =  str(data[idPos:lastPos])
    except:
        print( "DATA file is not json, or doesn't exist")
        lastCommentSaved = None

    # test json thingy
    # Iterate through json
    output = ""
    beforeID = ""
    flag = True
    output = ""
    beforeID = ""
    
    # Generate Users Vars
    flag = True
    json2 = open("DATA2.json","a")
    newComments = 0
    # GO THROUGH NEW DATA
    while flag:
        # while there are comments remaining
        output = requests.get(bot.commentsURL+"&before_id="+beforeID)
        try:
            output = output.json()
        except:
            flag = False
            break;
        for x in output['response']['messages']: 
            # iterates through json objects of messages (by everyone)
            if x['id'] != lastCommentSaved:
                # if it is a new comment!
                allComs.append(x)
                beforeID = x['id']
                # Generate Users!
                if x["sender_type"] == "user":
                    if x["user_id"] not in Users:
                        # add user to Users
                        Users[x["user_id"]] = user(x["user_id"],x["name"])
                # add this comment to that users object
                if x["sender_type"] == "user":
                    if x["user_id"] in Users:
                        newComments += 1
                        # add comments to users
                        Users[x["user_id"]].addToComs(x)
                # add to new json file
                json.dump(x,json2)
                # seperates the comments
                json2.write("|453345[][]123~~|")
            elif x['id'] == lastCommentSaved:
                # last comment reached!
                # do not save! move on to reading from old comments
                flag = False
                break;

    print (str(newComments) + " new Comments!")
    json2.close()

    # GO THROUGH OLD DATA (STORED)
    if lastCommentSaved != None:
        oldData = open("DATA.json","r")
        data = oldData.read()
        oldData.close()
        data = data.split("|453345[][]123~~|")
        # ADD DATA TO SCRIPT
        for x in data:
            try:
                x = json.loads(x)
                allComs.append(x)
                # Generate Users!
                if x["sender_type"] == "user":
                    if x["user_id"] not in Users:
                        # add user to Users
                        Users[x["user_id"]] = user(x["user_id"],x["name"])
                # add this comment to that users object
                if x["sender_type"] == "user":
                    if x["user_id"] in Users:
                        # add comments to users
                        Users[x["user_id"]].addToComs(x)
            except:
                pass

    # APPEND OLD DATA TO NEW DATA, CHANGE FILE NAMES
    for key,value in Users.items():
        value.calcMedals()
    os.system("cat DATA.json >> DATA2.json")
    os.system("rm -fr DATA.json")
    os.system("mv DATA2.json DATA.json")


def smallOptions(user, bot):
    global allComs
    global Users
    # options for indiviual users
    while True: 
        print ("User " + user.name + " Selected\nSelect an Option")
        print ("1. Markov Chain Generator")
        print ("2. Number of Likes")
        print ("3. Number of Comments")
        print ("4. Ratio Likes/Comment")
        print ("5. Medal Count")
        print ("6. Most Common Words")
        print ("7. Best Friends")
        print ("8. Exit")
        
        
        try:
            inputOpt = int(input("Input Option Choice (1-8): "))
        except:
            inputOpt = 0

        output = ""
        if inputOpt == 1:
            # Marky stuff
            output = menuOpts.userMarkChain(user.name,user.userID,allComs,Users)
        elif inputOpt == 88:
            output = menuOpts.userTommyMarkChain(user.name,user.userID,allComs,Users)
        elif inputOpt == 2:
            # Number of Likes
            output = menuOpts.userLikeCount(user.name,user.numLikes())
        elif inputOpt == 3:
            # Return amount of Comments
            output = menuOpts.userPostCount(user.name,user.numPosts)
        elif inputOpt == 4:
            # Ratio
            output = menuOpts.userRatio(user.name,user.numLikes(),user.numPosts)
        elif inputOpt == 5:
            # Medal Count
            output = menuOpts.userMedalCount(user)
        elif inputOpt == 6:
            # Most Common Words
            output = menuOpts.userCommonWords(user,10)
        elif inputOpt == 7:
            # Best Friends
            output = menuOpts.userBestFriends(user, Users) 
        elif inputOpt == 8:
            return
        else:
            print( "Error!")
            return
        print (output)

        ans = input("Do you wish to send this to the group chat? (y/n): ")
        if ans == 'y':
            comment(bot,output)
        print( "\n")

def globeOptions(bot):
    global Users
    global allComs
    while True: 
        print( "GLOBAL SELECTED\nSelect an Option" )
        print( "1. Global Markov Generator")
        print( "2. Ranking of Likes")
        print( "3. Ranking of Comments")
        print( "4. Ratio Likes/Comment")
        print( "5. Most Common Words")
        print( "6. Global Best Friends")
        print( "7. GLobal Sexism Tracker")
        print( "8. MEDALS")
        print( "9. Exit")
        inputOpt = input("Input Option Choice (1-9): ")
        try:
            inputOpt = int(inputOpt)
        except:
            inputOpt = 0

        output = ""
        if inputOpt == 1:
            # Marky stuff
            output = menuOpts.globalMarkChain(allComs,Users)
        elif inputOpt == 88:
            # TOMMYBOT
            output = menuOpts.globalTommyMarkChain(allComs,Users)
        elif inputOpt == 2:
            # Ranking of likes!
            output = menuOpts.globalLikeRanks(Users)
        elif inputOpt == 3:
            # ranking of comments
            output = menuOpts.globalCommentsRanks(Users)
        elif inputOpt == 4:
            # Ranking of Likes/Comments 
            output = menuOpts.globalRatioRanks(Users)
        elif inputOpt == 5:
            #most common words
            output = menuOpts.globalCommonWords(Users)
        elif inputOpt == 6:
            #Best Friends!
            output = menuOpts.globalBestFriends(Users)
        elif inputOpt == 7:
            #Best Friends!
            output = menuOpts.globalSexismTracker(Users)
        elif inputOpt == 8:
            medalOptions(bot)
        elif inputOpt == 9:
            break
        else:
            print ("Error!")

        print (output)

        ans = input("Do you wish to send this to the group chat? (y/n): ")
        if ans == 'y':
            if len(output) <500:
                comment(bot,output)
            else:
                # Comment too long, gonna have to mash it together
                print ("Splitting it!")
                newOut = output.split("\n\n")
                x = 0
                while x < len(newOut):
                    if x + 2 < len(newOut):
                        threer = newOut[x] + "\n\n" + newOut[x+1] + \
                        "\n\n" + newOut[x+2] + "\n\n"
                        comment(bot,threer)
                        x+=3
                    elif x + 1 < len(newOut):
                        twoer = newOut[x] + "\n\n" + newOut[x+1] + \
                        "\n\n" 
                        comment(bot,twoer)
                        x+=2
                    elif x + 1 < len(newOut):
                        oner = newOut[x] + "\n\n" 
                        comment(bot,oner)
                        x+=1 
        print ("\n")

def medalOptions(bot):
    global Users
    global allComs
    while True: 
        print ("\nMEDALS SELECTED\nSelect an Option" )
        print ("1. Bronze Medals")
        print ("2. Silver Medals")
        print ("3. Gold Medals")
        print ("4. Platinum Medals")
        print ("5. Diamond medals")
        print ("6. Shame Medals")
        print ("7. Exit")

        inputOpt = input("Input Option Choice (1-8): ")
        try:
            inputOpt = int(inputOpt)
        except:
            inputOpt = 0

        output = ""
        if inputOpt == 1:
            # Print Bronze medals of everyone
            output = menuOpts.globalBronzeCount(Users)
        elif inputOpt == 2:
            output = menuOpts.globalSilverCount(Users)
        elif inputOpt == 3:
            output = menuOpts.globalGoldCount(Users)
        elif inputOpt == 4:
            output = menuOpts.globalPlatinumCount(Users)
        elif inputOpt == 5:
            output = menuOpts.globalDiamondCount(Users)
        elif inputOpt == 6:
            output = menuOpts.globalShameCount(Users)
        elif inputOpt == 7:
            return
        else:
            print ("Error!")
        print ("\n")
        print (output)

        ans = input("Do you wish to send this to the group chat? (y/n): ")
        if ans == 'y':
            comment(bot,output)
        print ("\n")


def userMenu(bender):
    while True:
        num = 0
        print ("\nUsers Selection: ")
        # list items
        for key,value in Users.items():
            num+=1
            print (str(num) + ". " + value.name + ": " + key)
        num+=1
        exit = num
        print (str(num) + ". Return\n")
        try:
            inputnum = int(input("Input Number to Select Option " +\
                    "(1," + str(num) + "): "))
        except:
            inputnum = 5000
        # check if input is in 

        if inputnum == exit:
            print ("Returning to Main Menu\n")
            break;
        elif inputnum < num and inputnum > 0:
            for key,value in Users.items():
                inputnum-=1
                if inputnum == 0:
                    smallOptions(Users[key], bender)        
        else:
            print ("Input not found!\n")
            return

if __name__ == "__main__":
    # Get AUTH, GroupID, BotID, and more from config.txt
    getTokens() 
    # create bot, uses info in file
    bender = bot()
    # Compile Comments (Will make DIFF later)
    # creates users
    generateContent(bender)
    # Higher Menu! 
    while True:
        print ("\nSelect A Menu:")
        print ("1. User Menu")
        print ("2. Global Menu")
        print ("3. Settings Menu")
        print ("4. Exit Program")

        try:
            inputnum = int(input("\nInput Number to Select Option (1-4): "))
        except:
            inputnum = 5000
        # check if input is in 

        if inputnum == 4:
            print ("Thank you for using this program\n")
            break;
        elif inputnum ==3:
            settings.settingMenu(bender,confFileName)
            getTokens(False)
        elif inputnum == 2:
            globeOptions(bender)
        elif inputnum == 1:
            userMenu(bender)
        elif inputnum == 88:
            # SECRET TOMMY BOT
            room = ohHai()
            print (room )
            shouldI = input("\ny/n to post: ")
            if shouldI == "y":
                comment(bender,room)
        else:
            print ("Input not found, try again!\n")
            break 
