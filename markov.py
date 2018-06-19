import markovify
import json
import markovify
import sys
from Tommy import catchFootball

def marky(userID,allComs,Users,globe=False, lisa = False):
    # returns Markvic Sentence
    strInput = ""
    if globe:
        # USE EVERYONES
        for x in allComs:
            if x["sender_type"] == "user":
                try:
                    strInput += x['text'].encode("utf8") + ". "
                except:
                    pass
        if lisa:
            strInput += catchFootball()
    elif not globe:
        for x in Users[userID].coms:
            try:
                # sometimes the text has errors (fucking emojis)
                strInput += x['text'].encode("utf8") + ". "
            except:
                pass
        if lisa:
            strInput += catchFootball()
    # build the model
    # Print one randomly-generated sentences
    for x in range (0,20): 
        text_model = markovify.Text(strInput)
        output = text_model.make_sentence()
        if output != None:
            return str(output) + "\n"
    return "Markov Chain Failed" 

