import json

# Returns list of top 5 words
# Will feed list of common words through a bording library
def getCommonWords(user,x):
    # passed a user object
    wordList = []
    wordList = comWords(user.coms)
    output= "Most Common Words for User " + user.name + ":\n"
    for x in range (0,x):
        try:
            output+= wordList[x][1] + ": " + str(wordList[x][0]) +"\n"
        except:
            pass
    return output

def comWords(coms):
    #gets a list of json objects
    #returns a Dict of words
    words = {}
    comments = []
    # pull out text from comments
    for com in coms:
        try:
           comments.append(com['text'].encode("utf8")) 
        except:
            pass

    # pull out words from text
    for com in comments:
        word = com.split()
        # add them to dicts
        for x in word:
            # get rid of caps
            x = x.lower()
            # get rid of !.
            x = x.translate(None,".!?><,:'[]{}()@")
            if x not in words:
                words[x] = 1
            else:
                words[x] = words[x] + 1
    
    # get rid of boring
    boring = ["the","i","to","a","is","you","that","if","im","and",\
            "it","for","that","of","my","in","its","this","but","on",\
            "but","just","so","me","not","have","was","be","0","we","at",\
            "can"]
    for b in boring:
        if b in words:
            del words[b]
    # Put into list
    tmp = [(v,k) for k,v in words.iteritems() ]
    # Sort
    tmp.sort(reverse=True)
    # Return top 5
    return tmp

if __name__ == "__main__":
    comments=[]
    words = {}
    for com in comments:
        word = com.split()
        # add them to dicts
        for x in word:
            x = x.lower()
            x = x.translate(None,".!?><,:'[]{}()")
            if x not in words:
                words[x] = 1
            else:
                words[x] = words[x] + 1

    tmp = [(v,k) for k,v in words.iteritems() ]
    tmp.sort(reverse=True)
    print str(tmp) 
