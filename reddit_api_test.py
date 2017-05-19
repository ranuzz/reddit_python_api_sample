# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 10:59:06 2016

@author: ranu
"""

import requests
import requests.auth
import time
import logging

"""Authenticate and get token"""
""" client ID : ** """
""" secret : ** """
""" app name : testredboat """
""" redboatflag  : 9********* """

logging.basicConfig(filename='example.log',level=logging.DEBUG)

def getToken():
    client_auth = requests.auth.HTTPBasicAuth('7OjMGN0wjNfnug',
                                          'DFYIF7wmxc-9_FYKXg-VOp3_LLY')
    headers = {"User-Agent": "TestinAPI/0.2 by redboatflag"}
           
    post_data = {"grant_type": "password",
                 "username": "redboatflag",
                 "password": "9*********"}
    
    response = requests.post("https://ssl.reddit.com/api/v1/access_token",
                             auth=client_auth,
                             data=post_data,
                             headers=headers)
    
    jsonData = response.json()
    
    if 'error' in jsonData:
        logging.critical("authentication failed")
        return None
    logging.info("authentication successful : token : " +
                jsonData['access_token'])
    return jsonData['access_token']

def getRandomHotLink(token):
    headers = {"Authorization": "bearer "+token,
               "User-Agent": "TestinAPI/0.1 by RedditOfficialBot"}
    
    
    params = {}
    params['limit'] = 1
    response = requests.get("https://oauth.reddit.com/r/random/new",
                            params=params,
                            headers=headers)
    return response.json()

def postComment(comment, token, linkname):
    headers = {"Authorization": "bearer "+token,
               "User-Agent": "TestinAPI/0.1 by RedditOfficialBot"} 
    data = {}
    data['api_type'] = "json"
    data['text'] = comment.strip()
    data['thing_id'] = linkname
    
    response = requests.post("https://oauth.reddit.com/api/comment",
                             data=data,
                             headers=headers)
    rData = response.json()
    if 'error' in rData:
        logging.critical("comment failed")
    else:
        logging.info("comment submitted :" + comment)

def upVote(token, linkname):
    headers = {"Authorization": "bearer "+token,
               "User-Agent": "TestinAPI/0.1 by RedditOfficialBot"} 
    data = {}
    data['dir'] = 1
    data['id'] = linkname

    response = requests.post("https://oauth.reddit.com/api/vote",
                             data=data,
                             headers=headers)
    rData = response.json()
    if 'error' in rData:
        logging.critical("upVote failed")
    else:
        logging.info("upVote successful")

def listSubreddit(token, subreddit, method):
    headers = {"Authorization": "bearer "+token,
               "User-Agent": "TestinAPI/0.1 by RedditOfficialBot"}
    params = {}
    params['limit'] = 100
    params['count'] = 100
    response = requests.get("https://oauth.reddit.com/r/"+subreddit+"/"+method,
                            params=params,
                            headers=headers)
    return response.json()

token = "RJRTMiL7qMLoUdvXe3f-TEdlU60"

respData = None
timeStamp = int(time.time())
lastCommentTime = int(time.time())
timeout = 30

while (int(time.time()) - timeStamp) < 10:
    if (token == None):
        token = getToken()
    respData = listSubreddit(token, "fasdfasfasdfsadfasfasfasdf", "top")
    if 'error' in respData:
        logging.warning("token ["+token+"] expired")
        token = getToken()
        continue
    logging.info(respData)
    logging.info("\n\n\n")
    time.sleep(2)
    
