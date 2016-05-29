# -*- coding: utf-8-*-
import re
from client import app_utils
from classes.wordpresspost import Wordpresspost
import datetime

WORDS = ["POSTING"]
PRIORITY = 1
target = 0
action = ""

def isValid(text):
    print text
    return bool(re.search(r'\b(Posting)\b', text, re.IGNORECASE))

def handle(text, mic, profile):
    wp = Wordpresspost()
    while True:
        mic.say("Go to Word press scenario")
        inScenario(mic, wp)
        break
    mic.say("Done from Word Press.")

def getTarget(mic, t):
    global target
    try:
        target = int(t)
    except ValueError:
        print("That's not an int!")
    mic.say("Target change to %d " % target)
    return target

def inScenario(mic, wp):
    global target
    doOptions(mic,wp)

def doOptions(mic, wp):
    #texts = tuple(map(str,texts))
    #print texts
    while True:
        mic.say("What do you want to do? New posting? Publish posting? Draft posting? Or get all the post?")
        texts = mic.activeListenToAllOptions()
        if input:
            for text in texts:
                print text
                if bool(re.search(r'\b(New posting)\b', str(text), re.IGNORECASE)):
                    createPost(mic, wp)
                    break
                elif bool(re.search(r'\b(Publish)\b', str(text), re.IGNORECASE)):
                    changePostStatus(mic, wp, "publish")
                    break
                elif bool(re.search(r'\b(Draft)\b', str(text), re.IGNORECASE)):
                    changePostStatus(mic, wp, "draft")
                    break
                elif bool(re.search(r'\b(GET)\b', str(text), re.IGNORECASE)):
                    getPosts(mic, wp)
                    break
                elif bool(re.search(r'\b(OUT)\b', text, re.IGNORECASE)):
                    # jump out of the Wordpress scenario
                    return
                else:
                    continue
        else:
            print "Keep listening..."

def getPosts(mic, wp):
    ps = wp.getAllPosts()
    for post in ps:
        print "post id %s, post title is: %s." % (post.id, post.title)
        mic.say("post id %s, post title is: %s." % (post.id, post.title))

def createTitle(mic):
    while True:
        mic.say("What's the new post's title?")
        title = mic.activeListen()
        print title
        mic.say("The title is %s. Do you want to change it?" % title)
        ans = mic.activeListen()
        if app_utils.isPositive(ans):
            continue
        elif app_utils.isNegative(ans):
            mic.say("The title is %s." % title)
            return title
        elif bool(re.search(r'\bOUT\b', ans, re.IGNORECASE)):
            # if I don't want to create new post, just jump out
            return False
        else:
            continue

def createContent(mic):
    content = ""
    while True:
        mic.say("What's the new post's content?")
        paragraph = mic.activeListenToAllOptions()
        commandstr = ""
        for ph in paragraph:
            commandstr += ph
            commandstr += " "
        print "------------commandstr: %s " % commandstr
        if bool(re.search(r"\bThat's it\b", commandstr, re.IGNORECASE)):
            break
        elif bool(re.search(r'\bJump out\b', commandstr, re.IGNORECASE)):
            # if I don't want to create new post, just jump out
            return False
        else:
            content += paragraph[0]
            content += "\n"
    print "The content is: %s " % content
    mic.say("The content is %s." % content)
    return content

def createPost(mic, wp):
    global target
    while True:
        mic.say("Going to create a new post")
        title = createTitle(mic)
        if not title:
            return
        content = createContent(mic)
        if not content:
            return
        # new post create
        new_post = wp.createPost(title, content)
        getTarget(mic, new_post.id)
        mic.say("Do you want to publish this ?")
        ans = mic.activeListen()
        if app_utils.isPositive(ans):
            wp.publishPost(new_post.id)
            mic.say("The new posting %s is published." % new_post.title)
        elif app_utils.isNegative(ans):
            mic.say("The new posting %s is draft." % new_post.title)
        else:
            mic.say("I will keep it as draft")

        return new_post

def changePostStatus(mic, wp, status):
    global target
    while True:
        ps = wp.getAllPosts()
        if status == "publish":
            mic.say("Here is the posts list, which posting would you like to publish? Tell me the id.")
        elif status == "draft":
            mic.say("Here is the posts list, which posting would you like to keep in draft? Tell me the id.")
        else:
            mic.say("no status change. Return")
            return
        print "Title \tId"
        for post in ps:
            print "%s \t%s " % (post.title, post.id)
        nums = mic.activeListen()
        numText = nums
        #for numText in nums:
        try:
            # check if it's a number
            num = int(numText)
            print num
            print type(num)
            while True:
                mic.say("is it %d ?" % num)
                ans = mic.activeListen()
                if ans:
                    if app_utils.isPositive(ans):
                        # make the post draft
                        target = getTarget(mic, num)
                        if status == "publish":
                            wp.publishPost(target)
                            p = wp.getThePost(target)
                            mic.say("The posting %s is published." % p.title)
                        elif status == "draft":
                            wp.unpublishPost(target)
                            p = wp.getThePost(target)
                            mic.say("The posting %s is kept as draft." % p.title)
                        else:
                            mic.say("it's hard to get here. Just in case")
                            return
                        return
                    elif app_utils.isNegative(ans):
                        # go to listen to the number
                        break
                    elif bool(re.search(r'\bOUT\b', ans, re.IGNORECASE)):
                        return
                    else:
                        pass
                else:
                    continue
        except ValueError:
            print("%s not an int!") % numText
