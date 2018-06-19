# BenderBot
## Forwarning ##

BenderBot was coded organically (new features were sugguested and then incorperated). While the code remains documented and commented, there may be some repetition or poor foresight. Lessons were definitely learned.

## Current Capabilities
- Create a bot with your Groupme, Not hardcoded for any specific group/user-auth tokens! (See Start Up)
- All output can be easily posted to the specified groupme as a Bot. Easily share your findings!
- Create a User Specific Markov Chain sentence, its hilarious.
- Create a Markov Chain for all input added to the Groupme!
- Gather information about number of posts a user has posted. Also create a leaderboard for all users. 
- Gather information about number of likes a user has aquired. Create a leaderbaord for all users.
- Look at User's 'Best Friends', see who they like most out of the other comments, weighted
- Global Look at User's Best Friends to compare friendships, weighted!
- List ration of Likes/Comments
- Lists Medal Counts for specific Medals
- Get list of common words by person
- Medal Limits Changable in Configs
- Added ability to split global statistics so they fit in more than one message

## Planned Capabilities
- Sexism Bot. See if people are more likely to like one sex over an other
- Like Percentage, see how people are spending their likes on other people (Name: Valentines/Cupid?)

## PROBLEMS
- Probably a bug I didn't see

## BACKEND 
- DIFF storage that pulls only necessary comments (doesn't pull every comment every time)
- This does make it insecure if you upload the JSON file.

## Planned Backend Changes
- Potential multithreading of time consuming tasks

# Start UP
1. Needs python 2.7
2. pip install markovify (https://github.com/jsvine/markovify)
3. Download these files in their own directory, make sure DATA is cleared of everything
4. Create a groupme Bot (https://dev.groupme.com/bots/new)

  4a. Sign in using your groupme account

  4b. Choose the group you wish the bot to collect data from and post in (same group)

5. Once the bot is made, collect this data:
  
  5a. Your Bot's Name
  
  5b. Your Bots Auth ID (really long id)
  
  5c. Your Access Token (called Auth token in this program)
  
  5d. Your Groupme Group's ID (around 6-10 digits)

6. Int the directory containing these files, create 'config.txt'

  6a. Edit the file like below:
  
  6b. a,b,c,d,e should be REPLACED with # of likes required to get a Diamond (a), Platinum (b), Gold (c), Silver(d), and Bronze (e).
  
      Do not surround a,b,c,d,e in [brackets] or (parathensis), just right the list out seperated by commas.
  
--------Below is config.txt file -----------

[Personal Auth/Access token here]

[Group ID here]

[Bot Auth Token here]

[Bot name here]

config.txt

a,b,c,d,e

----------config.txt done ------------------

7. Run Benderbot: './benderBot.py'

