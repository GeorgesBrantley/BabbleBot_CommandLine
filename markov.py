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
        endEarly=0
        for x in allComs:
            if endEarly > 500:
                break
            if x["sender_type"] == "user":
                try:
                    endEarly += 1
                    strInput += x['text'] + ". "
                except:
                    pass
        if lisa:
            strInput += catchFootball()
    elif not globe:
        endEarly = 0
        for x in Users[userID].coms:
            if endEarly > 500:
                break
            try:
                # sometimes the text has errors (fucking emojis)
                endEarly += 1
                strInput += x['text']+ ". "
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

