#!/usr/bin/python
#!-*- coding:UTF-8 -*-

import requests
import sys
import re
import time
import urlGET

from bs4 import BeautifulSoup as bs
from platform import python_version

#check a version and quit if the version is less than 3
if python_version().startswith('2', 0, len(python_version())):
    print('Are you using python version {}\nPlease, use version 3.X of python'.format(python_version()))
    sys.exit()

import urllib.request

RED, YELLOW, GREEN, END = '\33[1;91m', '\33[1;93m', '\33[1;32m', '\33[0m'

if len(sys.argv) > 1:
    use = '''
{0}maltran v0.1{1}

github.com/MalwareReverseBrasil/maltran.git
Telegram: https://t.me/MalwareReverseBR
       
Usage: 
      python3 maltran.py
    '''
    print(use.format(GREEN,END))
    sys.exit()

banner = ('''
╔╦╗╔═╗╦  ┬ ┬┌─┐┬─┐┌─┐            
║║║╠═╣║  │││├─┤├┬┘├┤             
╩ ╩╩ ╩╩═╝└┴┘┴ ┴┴└─└─┘            
      ╔╦╗╦═╗┌─┐┌─┐┌─┐┬┌─┐    \t\t{}maltran.py version 0.1{}    
       ║ ╠╦╝├─┤├┤ ├┤ ││      \t\tTelegram: https://t.me/MalwareReverseBR   
       ╩ ╩╚═┴ ┴└  └  ┴└─┘    \t\thttps://github.com/MalwareReverseBrasil  
           ╔═╗╔╗╔┌─┐┬  ┬┌─┐┬ ┬┌─┐
           ╠═╣║║║├─┤│  │└─┐└┬┘└─┐
           ╩ ╩╝╚╝┴ ┴┴─┘┴└─┘ ┴ └─┘

malware-traffic-analysis.net
eNJoY ;)''')

print(banner.format(YELLOW,END))

site = 'http://malware-traffic-analysis.net/'
prefix = 'training-exercises.html'
target = site + prefix

url = urlGET.url_get(target)[0]
topic = url('div',attrs={'class':'content'})[0].findNext('h2').text


def list_exercises():

    '''
    execute web scrapping to get list of exercises in target
    :return: list of exercises to choose 
    '''

    msg = ''
    for i,data in enumerate(url.findAll('li')):
        try:
            date = data.find('a',attrs={'class':'list_header'}).text
            exercise = data.find('a',attrs={'class':'main_menu'}).text[28::]
            msg += ('\n[{0}{1:02}{2}] {3} <--> {4}'.format(RED,i+1,END,date,exercise))
        except AttributeError:
            break

    exit_option = ('\n[{0}{1:02}{2}] {0}E x i t{2}'.format(RED,i+1,END))
    msg += exit_option
    return i + 1,msg
     

def options_down():

    '''
    show options after choosing exercises
    :return: list of options to download or view files
    '''

    show = '[{}{:02}{}] --> Show associated files'
    down = '[{}{:02}{}] --> Downloads all associated files'
    down_exercise = '[{}{:02}{}] --> Downloads exercises associated files'
    down_answers = '[{}{:02}{}] --> Downloads answers associated files'
    back = '[{}{:02}{}] --> Return the list of exercises'
    lists = [show, down, down_exercise, down_answers, back]

    for num, list1 in enumerate(lists):
        print(list1.format(RED, num + 1, END))
    print ('')
    return


def option_1(date_exercise, link_exercise):

    '''
    execute option 1: show associated files
    :param date_exercise: xxxx-xx-xx  
    :param link_exercise: prefix xxxx/xx/xx/index.html 
    :return: show exercises and answers associated
    '''

    #cut link_exercise: xxxx/xx/xx/index.html ->>> xxxx/xx/xx/
    date_exercise_2 = link_exercise[:11]

    target = site + date_exercise_2
    verify_page2 = urlGET.url_get(target + 'page2.html')[1]
    verify_page6 = urlGET.url_get(target + 'page6.html')[1]
    result = ''

    if verify_page2.status_code == 200:
        if verify_page6.status_code == 200: #page6
            page = target + 'page6.html'

            for exercises in urlGET.url_get(page)[0].findAll('li'):
                try:
                    files_all = exercises.find('a', attrs={'class': 'menu_link'})['href']
                    result += '\n' + files_all
                except TypeError:
                    pass

        else: #page2
            page = target + 'page2.html'

            for exercises in urlGET.url_get(page)[0].findAll('li'):
                try:
                    files_all = exercises.find('a', attrs={'class': 'menu_link', 'href': re.compile('^' + date_exercise + '*')})['href']
                    result += '\n' + files_all
                except TypeError:
                    pass
    else: #index

        page = site + link_exercise

        for exercises in urlGET.url_get(page)[0].findAll('li'):
            try:
                files_all = exercises.find('a', attrs={'class': 'menu_link', 'href': re.compile('^' + date_exercise + '*')})['href']
                result += '\n' + files_all
            except TypeError:
                pass

    return result

def option_2(date_exercise, link_exercise):

    '''
    execute option 2: downloads all assotiated files 
    :param date_exercise: xxxx-xx-xx
    :param link_exercise: prefix xxxx/xx/xx/index.html
    :return: downloads files and show files
    '''

    date_exercise_2 = link_exercise[:11]
    target = site + date_exercise_2
    verify_page2 = urlGET.url_get(target + 'page2.html')[1]
    verify_page6 = urlGET.url_get(target + 'page6.html')[1]
    result = ''

    if verify_page2.status_code == 200:
        if verify_page6.status_code == 200:  # page6
            print('Download in progress...\nWait...')
            page = target + 'page6.html'

            for exercises in urlGET.url_get(page)[0].findAll('li'):
                try:
                    files_all = exercises.find('a', attrs={'class': 'menu_link'})['href']
                    result += '\n' + files_all

                    try:
                        f = urllib.request.urlopen(target + files_all)
                        data = f.read()
                        with open(files_all, "wb") as code:
                            code.write(data)

                    except FileNotFoundError:
                        pass

                except TypeError:
                    pass

        else:  # page2
            print('Download in progress...\nWait...')
            page = target + 'page2.html'

            for exercises in urlGET.url_get(page)[0].findAll('li'):
                try:
                    files_all = exercises.find('a', attrs={'class': 'menu_link', 'href': re.compile('^' + date_exercise + '*')})['href']
                    result += '\n' + files_all

                    try:
                        f = urllib.request.urlopen(target + files_all)
                        data = f.read()
                        with open(files_all, "wb") as code:
                            code.write(data)

                    except FileNotFoundError:
                        pass

                except TypeError:
                    pass
    else:  # index
        print('Download in progress...\nWait...')
        page = site + link_exercise

        for exercises in urlGET.url_get(page)[0].findAll('li'):
            try:
                files_all = exercises.find('a', attrs={'class': 'menu_link', 'href': re.compile('^' + date_exercise + '*')})['href']
                result += '\n' + files_all

                try:
                    f = urllib.request.urlopen(target + files_all)
                    data = f.read()
                    with open(files_all, "wb") as code:
                        code.write(data)
                except FileNotFoundError:
                    pass

            except TypeError:
                pass

    result += '\n\n{}Downloads Successful{} \n'.format(GREEN,END)
    return result

def option_3(date_exercise, link_exercise):

    '''
    execute option 3: show associated exercises files and downloads
    :param date_exercise: xxxx-xx-xx  
    :param link_exercise: prefix xxxx/xx/xx/index.html 
    :return: downloads associated exercises files
    '''

    date_exercise_2 = link_exercise[:11]
    target = site + date_exercise_2
    verify_page2 = urlGET.url_get(target + 'page2.html')[1]
    verify_page6 = urlGET.url_get(target + 'page6.html')[1]
    result = ''

    if verify_page2.status_code == 200:
        if verify_page6.status_code == 200:  # page6
            print('Download in progress...\nWait...')
            page = target + 'page6.html'

            for exercises in urlGET.url_get(page)[0].findAll('a'):
                if 'href' in exercises.attrs:
                    if not 'answers' in exercises.attrs['href'] and date_exercise in exercises.attrs['href']:

                        files_all = exercises.attrs['href']
                        result += '\n' + files_all

                        try:
                            f = urllib.request.urlopen(target + files_all)
                            data = f.read()
                            with open(files_all, "wb") as code:
                                code.write(data)

                        except FileNotFoundError:
                            pass

        else:  # page2
            print('Download in progress...\nWait...')
            page = target + 'page2.html'

            for exercises in urlGET.url_get(page)[0].findAll('a'):
                if 'href' in exercises.attrs:
                    if not 'answers' in exercises.attrs['href'] and date_exercise in exercises.attrs['href']:

                        files_all = exercises.attrs['href']
                        result += '\n' + files_all

                        try:
                            f = urllib.request.urlopen(target + files_all)
                            data = f.read()
                            with open(files_all, "wb") as code:
                               code.write(data)

                        except FileNotFoundError:
                            pass

    else:  # index
        print('Download in progress...\nWait...')
        page = site + link_exercise
        regular_expression = '^' + date_exercise + '*!answers*'
        print(regular_expression)

        for exercises in urlGET.url_get(page)[0].findAll('a'):
            if 'href' in exercises.attrs:
                if not 'answers' in exercises.attrs['href'] and date_exercise in exercises.attrs['href']:

                    files_all = exercises.attrs['href']
                    result += '\n' + files_all

                    try:
                        f = urllib.request.urlopen(target + files_all)
                        data = f.read()
                        with open(files_all, "wb") as code:
                            code.write(data)

                    except FileNotFoundError:
                        pass

    result += '\n\n{}Downloads Successful{} \n'.format(GREEN, END)
    return result


def option_4(date_exercise, link_exercise):

    '''
    execute option 3: show associated exercises files and downloads
    :param date_exercise: xxxx-xx-xx  
    :param link_exercise: prefix xxxx/xx/xx/index.html 
    :return: downloads associated exercises files
    '''

    date_exercise_2 = link_exercise[:11]
    target = site + date_exercise_2
    verify_page2 = urlGET.url_get(target + 'page2.html')[1]
    verify_page6 = urlGET.url_get(target + 'page6.html')[1]
    result = ''

    if verify_page2.status_code == 200:
        if verify_page6.status_code == 200:  # page6
            print('Download in progress...\nWait...')
            page = target + 'page6.html'

            for exercises in urlGET.url_get(page)[0].findAll('li'):
                try:
                    files_all = \
                        exercises.find('a', attrs={'class': 'menu_link',
                                                   'href': re.compile('^' + date_exercise + '.*answers.*')})['href']
                    result += '\n' + files_all

                    try:
                        f = urllib.request.urlopen(target + files_all)
                        data = f.read()
                        with open(files_all, "wb") as code:
                            code.write(data)

                    except FileNotFoundError:
                        pass

                except TypeError:
                    pass

        else:  # page2
            print('Download in progress...\nWait...')
            page = target + 'page2.html'

            for exercises in urlGET.url_get(page)[0].findAll('li'):
                try:
                    files_all = \
                        exercises.find('a', attrs={'class': 'menu_link',
                                                   'href': re.compile('^' + date_exercise + '.*answers.*')})['href']
                    result += '\n' + files_all

                    try:
                        f = urllib.request.urlopen(target + files_all)
                        data = f.read()
                        with open(files_all, "wb") as code:
                            code.write(data)

                    except FileNotFoundError:
                        pass

                except TypeError:
                    pass
    else:  # index
        print('Download in progress...\nWait...')
        page = site + link_exercise

        for exercises in urlGET.url_get(page)[0].findAll('li'):
            try:
                files_all = \
                    exercises.find('a', attrs={'class': 'menu_link',
                                               'href': re.compile('^' + date_exercise + '.*answers.*')})['href']
                result += '\n' + files_all

                try:
                    f = urllib.request.urlopen(target + files_all)
                    data = f.read()
                    with open(files_all, "wb") as code:
                        code.write(data)
                except FileNotFoundError:
                    pass

            except TypeError:
                pass

    if result == '':
        result = '\n\n{}There is no answer file{}\n'.format(GREEN, END)
    else:
        result += '\n\n{}Downloads Successful{} \n'.format(GREEN, END)

    return result


def main():

    print('{}'.format(GREEN) + topic + '{}'.format(END))
    time.sleep(1.8)
    print(list_exercises()[1])

    while True:
        try:
            select_exercise = int(input('\nSelect an exercise: '))
            if select_exercise not in range(1, list_exercises()[0] + 1):
                print('Select a number between 01 and {:02}'.format(list_exercises()[0]))
                pass
        except ValueError:
            print('Enter only with numbers.')
            pass

        if select_exercise == list_exercises()[0]: #exit environment
            print('\nBye!\n')
            break

        for num, list1 in enumerate(url.findAll('li')):
            try:
                if select_exercise == num + 1:
                    choice = list1.find('a',attrs={'class':'main_menu'}).text[28::] #title of exercise selected
                    date = list1.find('a', attrs={'class': 'list_header'}).text #date xxxx-xx-xx
                    prefix_choice = list1.find('a',attrs={'class':'main_menu'})['href'] #prefix xxxx/xx/xx/index.html

                    print('\nYou chose the exercise {0}{2}{1}\n'.format(YELLOW,END,choice))

                    options_down()

                    while True:
                        try:
                            select_down = int(input('Select an option: '))

                            if select_down not in range(1,6):
                                print('Select a number between 01 and 05')
                                pass

                            if select_down == 1:
                                print(option_1(date,prefix_choice))
                                print('')

                            if select_down == 2:
                                print(option_2(date,prefix_choice))
                                print('')

                            if select_down == 3:
                                print(option_3(date,prefix_choice))
                                print('')

                            if select_down == 4:
                                print(option_4(date,prefix_choice))
                                print('')

                            if select_down == 5:
                                print(list_exercises()[1])
                                break

                        except ValueError:
                            print('Enter only with numbers.')
                            pass

            except AttributeError:
                break
    return

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nBye\n')
        sys.exit()
    except SystemExit:
        pass