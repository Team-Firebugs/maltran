#!/usr/bin/python3
#-*- coding:UTF-8 -*-

import requests
from bs4 import BeautifulSoup as bs

def url_get(url):

    '''
    execute download html of target: malware-traffic-analysis.net
    :param url: var target 
    :return: html.parser of target
    :return: requests
    '''
    page = requests.get(url)
    soup = bs(page.content, 'html.parser')

    return soup,page
