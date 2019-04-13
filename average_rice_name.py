import re
import urllib3
import operator
import sys
import numpy as np
from collections import defaultdict

# Returns (first, last) tuple of strings
def cleanName(raw):
    clean = raw.replace("class=\"name\" >", "")
    clean = clean.replace("</a>", "")
    clean = clean.strip().lower()
    last = clean.split(",")[0]
    first = clean.split(",")[1].strip().split(" ")[0]

    last = last.replace("-", "").replace("'", "").replace('"', "").replace(".", "").replace("&#39;", "").replace("\xc3", "").replace("\xa9", "").replace("\xb3", "").replace("\xba", "").replace("\xa7", "").replace("\xa1", "").replace("`", "")
    first = first.replace("-", "").replace("'", "").replace('"', "").replace(".", "").replace("&#39;", "").replace("\xc3", "").replace("\xa9", "").replace("\xb3", "").replace("\xba", "").replace("\xa7", "").replace("\xa1", "").replace("`", "")
    return (first, last)

def searchForCollege(college):
    queryBase = "https://search.rice.edu/html/people/p/0/0/?firstname=&lastname=&phone=&title=&department=&college={}&major="

    query = queryBase.format(college)
    all = []

    http = urllib3.PoolManager()
    site = str(http.request('GET', query).data)
    matches = re.finditer(r'class=\"name\" >.{1,100}<\/a>', site)
    
    for match in matches:
        all.append(cleanName(match.group()))

    print("Found {} for {}".format(str(len(all)), college))

    return all

def computeAverage(names, longest, useLongName):
    average = [{} for _ in range(longest)]
    alphabet = "abcdefghijklmnopqrstuvwxyz " # The space at the end is important

    # Initialize the dict
    for d in average:
        for char in alphabet:
            d[char] = 0

    # Count them up
    for name in names:
        for idx, char in enumerate(name):
            average[idx][char] += 1
        if not useLongName:
            for i in range(len(name), longest):
                average[i][" "] += 1
        
        
    mostFreq = [sorted(x.items(), key=operator.itemgetter(1)) for x in average]        
    mostFreq = [x[-1][0] for x in mostFreq]
    
    return "".join(mostFreq)
    
'''
a -> 0
z -> 25
whitespace -> 26
'''
def charToNum(c):
    if c == " ":
        return 26

    return(ord(c.lower()) - 97)

def numToChar(n):
    if n == 26:
        return " "
    else:
        return chr(n + 97)

def computeAverage2(names, longest, trueAverage):
    # Convert all names into "stretched" version
    longest_f = float(longest)
    normalizedNames = []
    for name in names:
        scalingFactor = longest_f / len(name)
        scaled = []
        count = 0
        for char in name:
            for _ in range(int(scalingFactor + .5)):
                if count < longest:
                    scaled.append(char)
                    count += 1
                else:
                    break
        while count < longest:
            scaled.append(name[-1])
            count += 1

        normalizedNames.append(scaled)

    # All names are now normalized to the length of the maximum name

    # Compute the average name of max size
    # Method 1: True average
    averageNameMax = []
    if trueAverage:
        numNames = [[charToNum(c) for c in name] for name in normalizedNames]
        averageNameMax = np.sum(numNames, axis=0) / len(names)
        averageNameMax = [numToChar(int(x)) for x in averageNameMax]
    else:
    # Method 2: Frequency 
        for i in range(longest):
            freqs = defaultdict(int)
            for name in normalizedNames:
                freqs[name[i]] += 1
            
            vals = sorted(freqs.items(), key=operator.itemgetter(1))
            vals.reverse()
            averageNameMax.append(vals[0][0])
        
    averageNameLen = sum([len(x) for x in names]) / len(names)
    averageScalingFactor = longest_f / averageNameLen
    averageName = []
    idx = 0.0
    while idx < longest:
        averageName.append(averageNameMax[min(int(idx), longest - 1)])
        idx += averageScalingFactor

    return "".join(averageName)


def run(useSmooth, useTrueAverage, useLongName):
    allColleges = ["will+rice", "baker", "lovett", "sid", "hanszen", "wiess", "mcmurtry", "duncan", "brown", "jones", "martel"]

    allNames = []
    for college in allColleges:
        allNames += searchForCollege(college)

    longestFirst = max([len(x[0]) for x in allNames])
    longestLast = max([len(x[1]) for x in allNames])
    
    averageFirst = ""
    averageLast = ""

    if useSmooth:
        averageFirst = computeAverage2([x[0] for x in allNames], longestFirst, useTrueAverage)
        averageLast = computeAverage2([x[1] for x in allNames], longestLast, useTrueAverage)
    else:
        averageFirst = computeAverage([x[0] for x in allNames], longestFirst, useLongName)
        averageLast = computeAverage([x[1] for x in allNames], longestLast, useLongName)

    print("It's {} {}".format(averageFirst, averageLast))


if len(sys.argv) == 1:
    run(False, False, False)
else:
    run("-s" in sys.argv, "-a" in sys.argv, "-l" in sys.argv)
