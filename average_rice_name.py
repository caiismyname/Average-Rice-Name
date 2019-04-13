import re
import urllib3
import operator

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

def computeAverage(names, longest):
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
       for i in range(len(name), longest):
           average[i][" "] += 1
        
        
    mostFreq = [sorted(x.items(), key=operator.itemgetter(1)) for x in average]        
    mostFreq = [x[-1][0] for x in mostFreq]
    
    return "".join(mostFreq)
    


def run():
    allColleges = ["will+rice", "baker", "lovett", "sid", "hanszen", "wiess", "mcmurtry", "duncan", "brown", "jones", "martel"]

    allNames = []
    for college in allColleges:
        allNames += searchForCollege(college)

    longestFirst = max([len(x[0]) for x in allNames])
    longestLast = max([len(x[1]) for x in allNames])

    averageFirst = computeAverage([x[0] for x in allNames], longestFirst)
    averageLast = computeAverage([x[1] for x in allNames], longestLast)

    print("It's {} {}".format(averageFirst, averageLast))

run()
