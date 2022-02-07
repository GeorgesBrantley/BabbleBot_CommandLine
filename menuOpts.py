# This is a seperate file for menu commands
# Returns information back to benderBot
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
from commonWords import getCommonWords

# Small Options
def userMarkChain(name,ID,allComs,Users):
    # single Users Mark chain
    return "Markov Chain for " + name + " :\n> " + marky(ID,allComs,Users,False)
def userTommyMarkChain(name,ID,allComs,Users):
    # Single User ANd TOmmy Mark chain
    return "TOMMY MARKOV CHAIN for " + name + " :\n> " + marky(ID,allComs,Users,False,True)
def userLikeCount(name,numLikes):
    # Single useres # of likes
    return "> User " + name + " has " + str(numLikes) + " Likes\n" 
def userPostCount(name,numPosts):
    # Single Users # of posts
    return "> User " + name + " has " + str(numPosts) + " Shitposts!\n"
def userRatio(name,numLikes,numPosts):
    # Single User amount of likes/comments
    return "> User " + name + " has a Like/Comment ratio of " + str(numLikes/float(numPosts)) +"\n"
def userMedalCount(user):
    # Counts the amount of Shame Medals a User has
    output = "> User " + user.name + "'s Medals:" + \
            "\nShame Medals    : " + str(user.shameLikes) +\
            "\nBronze Medals   : " + str(user.broMedal) +\
            "\nSilver Medals   : " + str(user.silMedal) +\
            "\nGold Medals     : " + str(user.golMedal) +\
            "\nPlatinum Medals : " + str(user.plaMedal) +\
            "\nDiamond Medals  : " + str(user.diaMedal) + "\n"
    return output

def userCommonWords(user,x):
    # get 10 most common words for user
    output = getCommonWords(user,x)
    return output

def userBestFriends(user,Users,limit=0):
    #Somebody that you like the Majority of their Comments
   
    # Dictionary of Other People and % of likes
    Others = {} #contains userName:(#likes,%)
    totalLikes = 0 # used later for weighing
 
    # iterate through Users
    for key,person in Users.items():
        # no circle Jerking
        if key != user.userID:
            # Creates Dict obj
            Others[person.name] = ["",0,0,0] # NAME, % formated, Total likes, division            
            # total messages of this person (useful later)
            totalMes = person.numPosts
            myLikes = 0
            # Iterate through person's list of comments (com), find one user like
            for c in person.coms:
                # check if user is in list of fav by
                for f in c["favorited_by"]:
                    if f == user.userID:
                        myLikes+=1  
            # edit Dict Object
            perc = format(myLikes/float(totalMes)*100.0,'.1f') # round it
            Others[person.name] = [person.name,perc,myLikes,myLikes/float(totalMes)]
            totalLikes += myLikes

    
    # iterate through Others, find top 3
    tmp = []
    for key,usr in Others.items():
        tmp.append(usr)

    # WEIGH LIKES, Person with less comments -> less friends power
    # use total number of likes
    for rel in tmp:
        ratio = rel[2]/float(totalLikes)
        power = 0
        if ratio < .01:
           power = rel[3] - .20 
        elif ratio < .03:
            power = rel[3] - .10
        elif ratio < .06:
            power = rel[3] - .05
        elif ratio < .09:
            power = rel[3]
        elif ratio < .12:
            power = rel[3] + .05
        elif ratio < .15:
            power = rel[3] + .07
        elif ratio < .18:
            power = rel[3] + .10
        elif ratio < .21:
            power = rel[3] + .13
        elif ratio < .24:
            power = rel[3] + .16
        elif ratio >= .24:
            power = rel[3] + .10

        if power < 0:
            power = 0
        rel.append(format(power*100.0,'.1f'))
        rel.append(float(power))

    # sort based on POWER LEVEL 
    tmp = sorted(tmp, key=lambda aaa: aaa[5])

    # create str, user/global 
    if limit == 0:
        output = user.name + "'s BEST FRIENDS\n(Friendship Weight takes in account of raw likes)\n"
    else:
        output = "\n"+user.name + "'s BEST FRIENDS:"
        
    x = 0
    # Print out info
    for a,b,c,d,e,f in reversed(tmp):
        # Name, total likes, %, ..., Pwer Points
        if limit == 0 or limit > x:
            output += "\n" + a + ": " + str(e) + "% Friendship Weight," + str(b) + "% likes/comments"
        x+=1
    output += "\n"
    return output 

# Global Options
def globalBestFriends(Users):
    output = "" 
    output = "GLOBAL BEST FRIENDS\n(Weighted Friendship takes in account of raw likes)\n\n"
    for key,person in Users.items():
       output+=userBestFriends(person,Users,3) 
    return output

def globalMarkChain(allComs,Users):
    # Creates mark chain for everyone
    return "Markov Chain for Everyone :\n> " + marky(False,allComs,Users,True)

def globalTommyMarkChain(allComs,Users):
    # Creates a mark chain for everyone and TOMMY
    return "TOMMY Markov Chain for Everyone :\n> " + marky(False,allComs,Users,True,True)

def globalLikeRanks(Users):
    # Ranks all users by # of likes
    tmp = []
    for key,usr in Users.items():
        tmp.append(usr) 
    tmp = sorted(tmp, key=lambda user:user.numLikes())        
    output = "Number of Likes per User: \n"
    total = 0
    for x in reversed(tmp):
        likes = x.numLikes()
        total += likes
        output += x.name + ": " + str(likes) + " Likes\n"
    output += "\nTotal Likes: " + str(total)
    return output

def globalCommentsRanks(Users):
    # Ranks all users by number of comments
    tmp = []
    for key,usr in Users.items():
        tmp.append(usr) 
    tmp = sorted(tmp, key=lambda user:user.numPosts)        
    output = "Number of Shitposts per User: \n"
    total = 0
    for x in reversed(tmp):
        total += x.numPosts
        output += x.name + ": " + str(x.numPosts) + " Shitposts\n"
    output += "\nTotal Shitposts: " + str(total)
    return output
def globalRatioRanks(Users):
    # Ranking of Likes/Comments 
    tmp = []
    for key,usr in Users.items():
        tmp.append(usr) 
    for u in tmp:
        u.ratio = float(u.numLikes())/u.numPosts
    tmp = sorted(tmp, key=lambda user:user.ratio)        
    output = "Likes/Shitpost per User: \n"
    for x in reversed(tmp):
        output += x.name + ": " + str(round(x.ratio,2)) + " Likes/Shitpost\n"
    return output

def globalCommonWords(Users):
    output = ""
    for key,u in Users.items():
        output += getCommonWords(u,3)  
    return output

def globalSexismTracker(Users):
    output = ""
    # Find total # of Likes Given
    # Label users as W/M
    # Find ratio of W/M in group

    # Make dictionary of Users of touples
    People = {} #[Name:Name,ID,M/W,#likes given to women, #likes total?] 

    # iterate through Users, get as much info as possible
    for key,usr in Users.items():
        # Ask for Gender:
        try:
            gender = raw_input("What Gender does " + usr.name + \
                                    " identify as? (M/W/O): ") 
        except:
            gender = "?"
        #TODO add check to make sure it is valid. 
        People[usr.name] = [usr.name,usr.userID,'?',0,0]
    return output

def globalWordle(Users):
    wordle = []
    for key,user in Users.items():
        wordle.append(user)
     
    for user in wordle:
        user.wordlePoints = 0
        user.wordleTries = 0
        for comment in user.coms:
            try:
                if re.match(r"Wordle \d{3} [123456X]/6\*?\n", comment['text']):        
                    w = re.findall(r"Wordle (\d{3}) ([123456X])/6\*?\n", comment['text'])
                    ww = w[0]
                    session, score = ww
                    if score == "X":
                        user.wordlePoints += 1
                    elif score == "6":
                        user.wordlePoints += 2
                    elif score == "5":
                        user.wordlePoints += 3
                    elif score == "4":
                        user.wordlePoints += 4
                    elif score == "3":
                        user.wordlePoints += 5
                    elif score == "2":
                        user.wordlePoints += 6
                    elif score == "1":
                        user.wordlePoints += 7
                    user.wordleTries += 1
            except:
                dog = 0
    wordle = sorted(wordle,key=lambda user:user.wordlePoints)
    output = "Total Wordles:\n"
    for x in reversed(wordle):
        if x.wordlePoints>0:
            output += x.name + ": " + str(x.wordlePoints) + " Points (/"+str(x.wordleTries)+")\n"
    return output


def globalShameCount(Users):
    # List all Shame Values
    # I could have made this a loop thing, but fuck it
    tmp = []
    for key,usr in Users.items():
        tmp.append(usr) 
    output = "SHAME Medals Per User: \n"
    tmp = sorted(tmp, key=lambda user:user.shameLikes)        
    for u in reversed(tmp):
        if u.shameLikes > 1:
            output += "User " + u.name + " has " + \
            str(u.shameLikes) + " Shame Medals\n"
        elif u.shameLikes ==1:
            output += "User " + u.name + " has " + \
            str(u.shameLikes) + " Shame Medal\n"
    return output

def globalBronzeCount(Users):
    # Get lists of all the Users and their Medals
    # I could have made this a loop thing, but fuck it
    tmp = []
    for key,usr in Users.items():
        tmp.append(usr) 
    output = "\nBronze Medals Per User: \n"
    tmp = sorted(tmp, key=lambda user:user.broMedal)        
    for u in reversed(tmp):
        if u.broMedal > 1:
            output += "User " + u.name + " has " + \
                    str(u.broMedal) + " Bronze Medals\n"
        elif u.broMedal == 1:
            output += "User " + u.name + " has " + \
                    str(u.broMedal) + " Bronze Medal\n"
    return output    

def globalSilverCount(Users):
    # get list of Silver Medals
    # I could have made this a loop thing, but fuck it
    tmp = []
    for key,usr in Users.items():
        tmp.append(usr) 
    output = "Silver Medals Per User: \n"
    tmp = sorted(tmp, key=lambda user:user.silMedal)        
    for u in reversed(tmp):
        if u.silMedal > 1:
            output += "User " + u.name + " has " + \
                    str(u.silMedal) + " Silver Medals\n"
        elif u.silMedal == 1:
            output += "User " + u.name + " has " + \
                    str(u.silMedal) + " Silver Medal\n"
    return output

def globalGoldCount(Users):
    # get list of GOld Medals
    # I could have made this a loop thing, but fuck it
    tmp = []
    for key,usr in Users.items():
        tmp.append(usr) 
    output = "Gold Medals Per User:\n"
    tmp = sorted(tmp, key=lambda user:user.golMedal)        
    for u in reversed(tmp):
        if u.golMedal > 1:
            output += "User " + u.name + " has " + str(u.golMedal) + " Gold Medals\n"
        elif u.golMedal == 1:
            output += "User " + u.name + " has " + str(u.golMedal) + " Gold Medal\n"
    return output

def globalPlatinumCount(Users):
    # get list of Platinum medals
    # I could have made this a loop thing, but fuck it
    tmp = []
    for key,usr in Users.items():
        tmp.append(usr) 
    output = "Platinum Medals Per User:\n"
    tmp = sorted(tmp, key=lambda user:user.plaMedal)        
    for u in reversed(tmp):
        if u.plaMedal > 1:
            output += "User " + u.name + " has " \
                    + str(u.plaMedal) + " Platinum Medals\n"
        elif u.plaMedal == 1:
            output += "User " + u.name + " has " \
                    + str(u.plaMedal) + " Platinum Medal\n"
    return output

def globalDiamondCount(Users):
    # get list of Diamond medals
    # I could have made this a loop thing, but fuck it
    tmp = []
    for key,usr in Users.items():
        tmp.append(usr) 
    output = "Diamond Medals Per User:\n"
    tmp = sorted(tmp, key=lambda user:user.diaMedal)        
    for u in reversed(tmp):
        if u.diaMedal > 1:
            output += "User " + u.name + " has " \
                    + str(u.diaMedal) + " Diamond Medals\n"
        elif u.diaMedal == 1:
            output += "User " + u.name + " has " \
                    + str(u.diaMedal) + " Diamond Medal\n"
    return output
