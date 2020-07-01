import datetime
import re
import random


class Helpers:
    def __init__(self):
        pass

    def markov_startup(self, m):
        linect = 0
        f = open("markov-brain//markov_brain.txt", "rt+")
        for line in f:
            m.add_text(line)
            linect = linect + 1
        self.logger("Startup activity: loaded the markov_brain.txt file into the Markov chainer. Loaded " \
                    + str(linect) + " lines of text.", "Info")
        f.close()

    def markov_add(self, m, txt, exclusion):
        # ok i think it's probably for the best if we scrub out any URL's before sending it to the markov chainer
        txt_cleaned = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", "", txt)
        if len(txt_cleaned) == 0:
            # if we clean the URL and we have an empty string, then that means that was the only thing in the message
            # and there's no sense in adding it...
            # print("Just a test, should be a blank string if only a URL was sent : "+txt_cleaned)
            self.logger("We got a request to add an empty string to the markov brain, it was probably a URL. "
                        "Ignoring it.", "Info")
            return
        for w in exclusion:
            if w in txt_cleaned:
                self.logger("We found a word that's in the markov exclusion list.", "Warn")
                self.logger("the entire string is: " + txt, "Warn")
                return
        f = open("markov-brain//markov_brain.txt", "at+")
        f.write("\n" + txt_cleaned)
        f.close()
        m.add_text(txt_cleaned)
        self.logger("Added a line to the Markov chainer.", "Info")

    def butt_replace(self, txt):
        exclf = open("config//butt_exclusions.txt", "rt+")
        excl = []
        for i in exclf:
            excl.append(i)
        exclf.close()
        txt_arr = txt.split()
        victim = 0  # pycharm gets mad without this but its not required
        for w in txt_arr:
            if w.lower() == 'butt':
                self.logger("the word butt already exists in the input", "info")
                return
        sentence_length = len(txt_arr)
        if sentence_length == 0:
            # something has gone wrong if we are in here, i have no idea how we could've gotten a blank input
            self.logger("Somehow we got a request to replace butt with an empty string.", "Error")
            return "butt ass??????"
        # if there's only one word in the message, it's not really a good candidate for butt replacement
        # this will also completely break the random number generator anyway
        if sentence_length == 1:
            self.logger("We got a request to replace butt in a string that is only one word long.", "Info")
            return
        loop = True
        while loop:
            victim = random.randrange(0, sentence_length)  # randrange : lower <= rando < upper
            if txt_arr[victim] not in str(excl):
                loop = False
        replace_with = 'butt'
        # handle for a couple of edge cases like...
        # case 1: init caps
        if re.search(r'^[A-Z]', txt_arr[victim]) is not None:
            replace_with = replace_with.title()
        # case 2: possessive
        if re.search(r"\w+'[Ss]$", txt_arr[victim]) is not None:
            replace_with = replace_with + "'s"
        # case 3: all caps
        if re.search(r'^[^a-z0-9]*$', txt_arr[victim]) is not None:
            replace_with = replace_with.upper()
        txt_arr[victim] = re.sub(r'([0-9a-zA-Z\']+)', replace_with, txt_arr[victim], count=1)
        # reconstructive surgery
        s = ""
        for word in txt_arr:
            s = s + word + " "
        return s.strip()

    def logger(self, msg, level):
        # why does the built in logging module not work writing to a file, i dont get it.
        logfile = open("georgie.log", "at+")
        ts = str(datetime.datetime.now())
        log_string = ts + " | " + level + " | " + msg+"\n"
        print(log_string)
        logfile.write(log_string)
        logfile.close()
        return None
