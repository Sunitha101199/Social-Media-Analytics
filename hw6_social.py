"""
Social Media Analytics Project
Name:
Roll Number:
"""
from nltk.probability import DictionaryConditionalProbDist
import numpy
import matplotlib
import pandas
import nltk
import hw6_social_tests as test

project = "Social" # don't edit this

### PART 1 ###

import pandas as pd
import nltk
nltk.download('vader_lexicon', quiet=True)
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
endChars = [ " ", "\n", "#", ".", ",", "?", "!", ":", ";", ")" ]

'''
makeDataFrame(filename)
#3 [Check6-1]
Parameters: str
Returns: dataframe
'''
def makeDataFrame(filename):
    filename_df = pd.read_csv(filename)
    return filename_df


'''
parseName(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parseName(fromString):
    list = fromString.split()
    if '(' in list[3]:
        name = str(list[1])+" "+str(list[2])
    else:
        name = str(list[1])
    return name


'''
parsePosition(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parsePosition(fromString):
    string = str(fromString.split("(")[1])
    position = str(string.split()[0])
    return position


'''
parseState(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parseState(fromString):
    string = str(fromString.split("(")[1])
    list = string.split()
    if len(list)>3:
        state = str(list[2])+" "+str(list[3])
    else:
        state = str(list[2])
    return str(state.split(")")[0])


'''
findHashtags(message)
#5 [Check6-1]
Parameters: str
Returns: list of strs
'''
def findHashtags(message):
    hashtags = message.split("#")
    list_hashtags = []
    for i in range(1,len(hashtags)):
        string = ""
        for j in hashtags[i]:
            if j in endChars:
                break
            else:
                string+=j
        string = "#"+string
        list_hashtags.append(string) 
    return list_hashtags


'''
getRegionFromState(stateDf, state)
#6 [Check6-1]
Parameters: dataframe ; str
Returns: str
'''
def getRegionFromState(stateDf, state):
    row = stateDf.loc[stateDf['state'] == state, 'region']
    return str(row.values[0])


'''
addColumns(data, stateDf)
#7 [Check6-1]
Parameters: dataframe ; dataframe
Returns: None
'''
def addColumns(data, stateDf):
    names, positions, states, regions, hashtags = [],[],[],[],[]
    for index,row in data.iterrows():
        label = row["label"]
        names.append(parseName(label))
        positions.append(parsePosition(label))
        state=parseState(label)
        states.append(state)
        regions.append(getRegionFromState(stateDf, state))
        hashtags.append(findHashtags(row["text"]))
    data['name']=names
    data['position']=positions
    data['state']=states
    data['region']=regions
    data['hashtags']=hashtags
    return


### PART 2 ###

'''
findSentiment(classifier, message)
#1 [Check6-2]
Parameters: SentimentIntensityAnalyzer ; str
Returns: str
'''
def findSentiment(classifier, message):
    score = classifier.polarity_scores(message)['compound']
    if score >= 0.1:
        return "positive"
    elif score <= -0.1:
        return "negative"
    else:
        return "neutral"


'''
addSentimentColumn(data)
#2 [Check6-2]
Parameters: dataframe
Returns: None
'''
def addSentimentColumn(data):
    classifier = SentimentIntensityAnalyzer()
    sentiments = []
    for index,row in data.iterrows():
        sentiments.append(findSentiment(classifier,row["text"]))
    data['sentiment'] = sentiments
    return


'''
getDataCountByState(data, colName, dataToCount)
#3 [Check6-2]
Parameters: dataframe ; str ; str
Returns: dict mapping strs to ints
'''
def getDataCountByState(data, colName, dataToCount):
    dictionary = {}
    if len(colName)!=0 and len(dataToCount)!=0:
        for index,row in data.iterrows():
            if row[colName]==dataToCount:
                if row['state'] not in dictionary:
                    dictionary[row['state']]=0
                dictionary[row['state']]+=1
    if len(colName)==0 and len(dataToCount)==0: 
        for index,row in data.iterrows():
            if row['state'] not in dictionary:
                dictionary[row['state']]=0
            dictionary[row['state']]+=1
    return dictionary


'''
getDataForRegion(data, colName)
#4 [Check6-2]
Parameters: dataframe ; str
Returns: dict mapping strs to (dicts mapping strs to ints)
'''
def getDataForRegion(data, colName):
    dictionary = {}
    for index,row in data.iterrows():
        if data['region'][index] not in dictionary:
            dictionary[data['region'][index]]={}
        if row[colName] not in dictionary[data['region'][index]]:
            dictionary[data['region'][index]][row[colName]]=0
        dictionary[data['region'][index]][row[colName]]+=1   
    return dictionary


'''
getHashtagRates(data)
#5 [Check6-2]
Parameters: dataframe
Returns: dict mapping strs to ints
'''
def getHashtagRates(data):
    dictionary = {}
    for index,row in data.iterrows():
        for i in row['hashtags']:
            if i not in dictionary:
                dictionary[i] = 0
            dictionary[i]+=1
    return dictionary


'''
mostCommonHashtags(hashtags, count)
#6 [Check6-2]
Parameters: dict mapping strs to ints ; int
Returns: dict mapping strs to ints
'''
def mostCommonHashtags(hashtags, count):
    dictionary = {}
    values = sorted(hashtags.values(),reverse=True)
    i=0
    while len(dictionary) != count:
        for key,value in hashtags.items():
            if values[i]==value and key not in dictionary:
                dictionary[key]=value
                i+=1
                break 
    return dictionary


'''
getHashtagSentiment(data, hashtag)
#7 [Check6-2]
Parameters: dataframe ; str
Returns: float
'''
def getHashtagSentiment(data, hashtag):
    list_hashtags = []
    result_float = 0
    count=0
    average=0
    for index,row in data.iterrows():
        list_hashtags = findHashtags(row['text'])
        if hashtag in list_hashtags:
            count+=1
            if data['sentiment'][index] == 'positive':
                result_float+=1
            elif data['sentiment'][index] == 'negative':
                result_float-=1
            else:
                continue
    if count == 0:
        average=0
    else:
        average = result_float/count
    return average


### PART 3 ###

'''
graphStateCounts(stateCounts, title)
#2 [Hw6]
Parameters: dict mapping strs to ints ; str
Returns: None
'''
def graphStateCounts(stateCounts, title):
    import matplotlib.pyplot as plt
    keys = list(stateCounts.keys())
    values = list(stateCounts.values())
    fig = plt.figure(figsize = (10, 10))
    # creating the bar plot
    plt.bar(keys, values, color ='blue',width = 0.7)
    plt.xticks(ticks=list(range(len(keys))), labels=keys, rotation="vertical")
    plt.xlabel("States")
    plt.ylabel("Numbers")
    plt.title(title)
    plt.show() 
    return


'''
graphTopNStates(stateCounts, stateFeatureCounts, n, title)
#3 [Hw6]
Parameters: dict mapping strs to ints ; dict mapping strs to ints ; int ; str
Returns: None
'''
def graphTopNStates(stateCounts, stateFeatureCounts, n, title):
    topNStates = {}
    featureDict = {}
    for i in stateFeatureCounts:
        featureDict[i] = stateFeatureCounts[i]/stateCounts[i]
    for key,value in sorted(featureDict.items(), key=lambda item: item[1],reverse=True):
        if key not in topNStates:
            topNStates[key]=value
            if len(topNStates)==n:
                break
    graphStateCounts(topNStates,title)
    return


'''
graphRegionComparison(regionDicts, title)
#4 [Hw6]
Parameters: dict mapping strs to (dicts mapping strs to ints) ; str
Returns: None
'''
def graphRegionComparison(regionDicts, title):
    featureNames = []
    regionNames = []
    regionFeature = []
    for i in regionDicts:
        if i not in regionNames:
            regionNames.append(i)
        for j in regionDicts[i]:
            if j not in featureNames:
                featureNames.append(j)
    for i in regionDicts:
        temp_list = []
        for j in featureNames:
            if j in regionDicts[i]:
                temp_list.append(j)
            else:
                temp_list.append(0)
        regionFeature.append(temp_list)
    sideBySideBarPlots(featureNames, regionNames, regionFeature, title)  
    return


'''
graphHashtagSentimentByFrequency(data)
#4 [Hw6]
Parameters: dataframe
Returns: None
'''
def graphHashtagSentimentByFrequency(data):
    hashtagRates = getHashtagRates(data)
    top50 = mostCommonHashtags(hashtagRates,50)
    hashtags, frequencies, sentimentScores = [], [], []
    for key in top50:
        if top50[key] not in frequencies: #optional step
            hashtags.append(key)
            frequencies.append(top50[key])
            sentimentScores.append(getHashtagSentiment(data,key))
    
    scatterPlot(frequencies, sentimentScores, hashtags, "Sentiment score based on Hashtag frequencies")
    return


#### PART 3 PROVIDED CODE ####
"""
Expects 3 lists - one of x labels, one of data labels, and one of data values - and a title.
You can use it to graph any number of datasets side-by-side to compare and contrast.
"""
def sideBySideBarPlots(xLabels, labelList, valueLists, title):
    import matplotlib.pyplot as plt

    w = 0.8 / len(labelList)  # the width of the bars
    xPositions = []
    for dataset in range(len(labelList)):
        xValues = []
        for i in range(len(xLabels)):
            xValues.append(i - 0.4 + w * (dataset + 0.5))
        xPositions.append(xValues)

    for index in range(len(valueLists)):
        plt.bar(xPositions[index], valueLists[index], width=w, label=labelList[index])

    plt.xticks(ticks=list(range(len(xLabels))), labels=xLabels, rotation="vertical")
    plt.legend()
    plt.title(title)

    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Expects that the y axis will be from -1 to 1. If you want a different y axis, change plt.ylim
"""
def scatterPlot(xValues, yValues, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    plt.scatter(xValues, yValues)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xValues[i], yValues[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.title(title)
    plt.ylim(-1, 1)

    # a bit of advanced code to draw a line on y=0
    ax.plot([0, 1], [0.5, 0.5], color='black', transform=ax.transAxes)

    plt.show()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    test.week1Tests()
    print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    test.runWeek1()

    ## Uncomment these for Week 2 ##
    print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    test.week2Tests()
    print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    test.runWeek2()

    ## Uncomment these for Week 3 ##
    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()
