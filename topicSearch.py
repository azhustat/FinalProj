import time;
class nList(list):
    """ 
    nList is a data structure that stores n elements. One can 
    add to the nList a new item by invoking the update method
    of a nList object. If the number of elements in the nList
    exceeds n, then the last element of the list will be 
    dropped.
    """
    def __init__(self,n):
        list.__init__(self);
        self.n = n;
        
    def update(self,obj):
        self.insert(0,obj);
        if len(self) > self.n:
            self.pop(-1);


def topicSearch(keywords,maxTweets,outputFileName = './test.txt', tweetsPerSearch = 50, sleepTime = 60,cacheSize = 50):
    """ search for keywords (given as a list of keywords)
    Input arguments:
    keywords: as the name suggests...
    maxTweets: number of tweets that match one of the keywords;
    tweetsPerSearch: (maximum) number of tweet returned by the api search fcn;
    An example:
    >>> keywords = ['USC','南加大','南加州','枪击'];
    >>> topicSearch(keywords,maxTweets = 100,outputFileName = './USCKilling.txt');
    """
    idCache = nList(cacheSize);
    i = 0;
    while i < maxTweets:
        if i > 0:  time.sleep(sleepTime); # sleep for a while in order not to piss off the server...
        fout = open(outputFileName,'a');
        for keyword in keywords:
            s = api.search(keyword,rpp=tweetsPerSearch);
            for t in s[::-1]:
                currentID = t.from_user_id;
                if currentID in idCache: # check for duplicates of user id.
                    continue;
                else:
                    strTemp = currentID.__str__() + " " + t.created_at.__str__() + " " + t.text.encode('utf8');
                    print >> fout, strTemp;
                    idCache.update(currentID);
                    i += 1;
                    print strTemp;
                    print i;
        fout.close();
        
