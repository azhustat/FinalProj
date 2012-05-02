from Tkinter import *
import codecs

class TagInputGui(Frame):
    """ 
    An graphic-user interface for tagging the tweets.
    filename: the file containing the tweets; must be in "myfile.txt" format.
    the output tag file would be named as "myfileTag.txt".
    The GUI allows you to use keyboard shortcut: e.g. press p for positive
    """
    def __init__(self, filename, master=None):
        fp = codecs.open(filename, "r", "utf-8");
        self.outFileName = filename[0:(len(filename)-4)] + "Tag.txt";
        self.tweets = fp.readlines();
        fp.close();
        self.numOfTweets = len(self.tweets);
        self.category = [-999 for i in range(self.numOfTweets)];
        self.currentTweetIndex = -1;
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.next();

    def quit(self):
        print self.category;
        self.save();
        Frame.quit(self);
        
    def save(self):
        fout = open(self.outFileName,"w");
        for i in self.category:
            print >> fout, i.__str__()+" ";
        fout.close();


    def next(self):
        print self.category;
        if self.currentTweetIndex < self.numOfTweets - 1:
            self.currentTweetIndex += 1;
            print self.tweets[self.currentTweetIndex].encode('utf8');
        else:
            print 'reaching the end of the tweet list...\n';
    
    def nextTweet(self):
        self.currentTweetIndex += 1;
        print self.tweets[self.currentTweetIndex].encode('utf8');
        
    def positive(self):
        self.category[self.currentTweetIndex] = 1;
        self.next();

    def negative(self):
        self.category[self.currentTweetIndex] = -1;
        self.next();

    def neutral(self):
        # this is in fact the unidentifiable case... 
        self.category[self.currentTweetIndex] = 0;
        self.next();

    def spam(self):
        self.category[self.currentTweetIndex] = 9;
        self.next();

    def previous(self):
        if self.currentTweetIndex == 0:
            print 'This is the beginning of the tweet list\n';
            return;

        self.currentTweetIndex -= 1;
        print self.tweets[self.currentTweetIndex].encode('utf8');

    def callback(self,event):
        print "yia";
        print event;
        if event == 'p':
            self.positive();

    def createWidgets(self):
        self.Pos = Button(self,underline = 0)
        self.Pos["text"] = "Positive"
        self.Pos["fg"]   = "blue"
        self.Pos["command"] =  self.positive

        self.Pos.pack({"side": "top"})
        
        self.focus_set();
        self.bind("<p>",lambda event: self.positive())

        self.Neg = Button(self,underline = 0)
        self.Neg["text"] = "Negative"
        self.Neg["fg"]   = "red"
        self.Neg["command"] =  self.negative

        self.Neg.pack({"side": "top"})
        self.bind("<n>",lambda event: self.negative())


        self.Neu = Button(self,underline = 0)
        self.Neu["text"] = "Unidentifiable"
        self.Neu["fg"]   = "black"
        self.Neu["command"] =  self.neutral

        self.Neu.pack({"side": "top"})
        self.bind("<u>",lambda event: self.neutral())


        self.Spam = Button(self,underline = 0)
        self.Spam["text"] = "Spam"
        self.Spam["fg"]   = "black"
        self.Spam["command"] =  self.spam

        self.Spam.pack({"side": "top"})
        self.bind("<s>",lambda event: self.spam())

        self.Prev = Button(self)
        self.Prev["text"] = "Previous (<-)"
        self.Prev["fg"]   = "black"
        self.Prev["command"] =  self.previous

        self.Prev.pack({"side": "top"})
        self.bind("<Left>",lambda event: self.previous())

        self.Next = Button(self)
        self.Next["text"] = "Next (->)"
        self.Next["fg"]   = "black"
        self.Next["command"] =  self.next

        self.Next.pack({"side": "top"})
        self.bind("<Right>",lambda event: self.next())

        self.Save = Button(self)
        self.Save["text"] = "Save"
        self.Save["fg"]   = "black"
        self.Save["command"] =  self.save

        self.Save.pack({"side": "top"})
        self.bind("<S>",lambda event: self.save())

        self.Quit = Button(self,underline = 0)
        self.Quit["text"] = "Quit"
        self.Quit["fg"]   = "black"
        self.Quit["command"] =  self.quit

        self.Quit.pack({"side": "top"})
        self.bind("<q>",lambda event: self.quit())


root = Tk()
app = TagInputGui(filename = './testsetae.txt',master=root)
app.mainloop()
root.destroy()
