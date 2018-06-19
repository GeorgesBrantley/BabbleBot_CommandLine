import sys
import os
import benderBot
def settingMenu(bender,fileN):
    while True:
        print "\nSettings Menu:"
        print "1. Get Information about changing Tokens" 
        print "2. Print Tokens"
        print "3. Reset Data"
        print "4. Exit!"

        try:
            inputnum = int(raw_input("\nInput Number to Select Option (1-4): "))
        except:
            inputnum = 500

        if inputnum == 1:
            print "Edit " + fileN + " in order to change tokens!"
            print """The first token is the Auth Token, you recieve this by 
                    Logging into here (https://dev.groupme.com/bots) with your 
                    groupme account"""
            print """The second token is your GroupId. That is found when you create 
                    a bot for a specfic groupme (see previous link)"""
            print """Third token is your Bot Auth Token, this is found when you create
                    a verified bot"""
            print """Fourth Token is the name of your create bot."""
            print """Fifth Token is the name of the config file. Not too important"""
            print """\nChange these tokens then restart the program. Your new bot 
                    should be in use!\n"""
        elif inputnum == 2:
            # READ FROM FILE AND PRINT
            # open file
            with open(fileN) as f:
                content = f.readlines()
            # remove whitespace characters like `\n` at the end of each line
            content = [x.strip() for x in content] 
            Auth = content[0]
            groupID = content[1]
            BotID = content[2]
            BotName = content[3]
            print "File: " + fileN + "\nTokens Used Below: "
            print "Auth Token: " + Auth
            print "BotName: " + BotName
            print "BotID: " + BotID
            print "groupID: " + groupID
        elif inputnum == 3:
            # delete DATA and close app
            print "Deleting stored data and closing application"
            os.system("rm -fr DATA.json")
            sys.exit(1)
        elif inputnum == 4:
            break
        else:
            print "Error!"


