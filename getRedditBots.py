#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 23:23:15 2018

@author: loey
"""

#import urllib.request
from bs4 import BeautifulSoup
import re

#botspage = "https://www.reddit.com/r/autowikibot/wiki/redditbots"
u_ = re.compile("/u/(.*)$")

with open('redditbots.txt', 'w') as w:
    #page = urllib.request.urlopen(botspage)
    page = open("redditbots-autowikibot.htm", "rb")
    soup = BeautifulSoup(page, 'html.parser')
    for link in soup.find_all('a'):
        if '/u/' in str(link):
            w.write(u_.search(link.get('href')).group(1) + "\n")
w.close()