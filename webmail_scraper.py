from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import random
import string
import fbchat
import os
import datetime

# Path to log file
filePath = '/var/log/nginx/access.log'

#Initialize chrome driver
options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome( options=options)

#Get random string function (if cant get email)
def get_random_string():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(5))
    return result_str
#Make screenshot
def make_screenshot(prefix):
    sleep(1)
    try:
        S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
        driver.set_window_size(S('Width'),S('Height'))
        driver.find_element_by_tag_name('body').screenshot( './' + date + '/' + prefix + '_' + screenshotName + '.png')
    except Exception as e:
        print('Exception: ', e)
#Send alert via messenger
def send_alert(text):
    session = fbchat.Session.login("<email>", "<password")
    print("Own id: {}".format(session.user.id))
    thread = fbchat.User(session=session, id="<recipient_id>")
    thread.send_text(text)
    thread.send_text("😍")
    session.logout()

#Check last line of file
lastLine = None
with open(filePath,'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            lastLine = line

#Wait for changes in file
while True:
    with open(filePath,'r') as f:
        lines = f.readlines()
    if lines[-1] != lastLine:
        lastLine = lines[-1]
        print("New item: ", lastLine)
        #Start geting website when find new URL
        url = lastLine
        #Skip if url not contain specified string
        if not '<domain>' in url: continue
        driver.get(url)
        sleep(1)
        #Find recipient of email
        try:
            bsObjInbox = BeautifulSoup(driver.page_source, features="html.parser")
            email = bsObjInbox.find(text='Do :').findNext('a').text
            email = email.translate(str.maketrans(dict.fromkeys('<>+[]')))
            email = email.split("@"); email = email[0]
            print("Email: ", email)
            screenshotName = email
        except Exception as e:
            print('Exception: ', e)
            screenshotName = get_random_string()
        finally:
            date = datetime.datetime.now().strftime("%Y%m%d-%H%M")
            os.mkdir(date)
            #Make screenshot
            make_screenshot('First')

        try:
            #Go to inbox and make screenshot
            inboxButton = driver.find_element_by_link_text("Odbierz Wiadomości")
            #Send alert
            send_alert(driver.current_url)

        except Exception as e:
            print('Exception: ', e)
            continue    
        inboxButton.click()
        make_screenshot('Inbox')
        #Go to folders
        foldersButton = driver.find_element_by_link_text("Foldery")
        foldersButton.click()
        make_screenshot('Foldery')
        #Go to sent items
        sentfolderButton = driver.find_element_by_link_text("Wysłane")
        sentfolderButton.click()
        make_screenshot('Wysłane')
        #Iterate inbox
        print('Start making screenshot in inbox')
        driver.find_element_by_link_text("Odbierz Wiadomości").click()
        baseURL = driver.current_url.split('readmail')[0]
        bsObjInbox = BeautifulSoup(driver.page_source, features="html.parser")
        for link in bsObjInbox.find_all('a'):
            urlIteam = baseURL + link.get('href')
            if ("http" in urlIteam) and ("view" in urlIteam):
                driver.get(urlIteam)            
                try:
                    bsObjItem = BeautifulSoup(driver.page_source, features="html.parser")
                    subject = bsObjItem.find(text='Temat :').findNext('td').text
                except Exception as e:
                    print('Exception: ', e)
                    subject = 'NoSubject'
                    if 'Twoja sesja nie jest już aktywna.' in driver.page_source:
                        print('Sesion expired')
                        break
                # Remove special characters from subject
                subject = subject.translate(str.maketrans(dict.fromkeys(' ')))
                print(subject)
                name = subject.translate(str.maketrans(dict.fromkeys(' :/|*?<>+[]')))
                name = 'Subject_' + name + get_random_string() + '_'
                make_screenshot(name)

        #Iterate sent folder
        print('Start making screenshot in sent folder')
        try:
            driver.find_element_by_link_text("Foldery").click(); driver.find_element_by_link_text("Wysłane").click()
        except Exception as e:
            print('Exception: ', e)
            err = str(e)
            if 'no such element' in err:
                continue
        baseURL = driver.current_url.split('readmail')[0]
        bsObjInbox = BeautifulSoup(driver.page_source, features="html.parser")
        for link in bsObjInbox.find_all('a'):
            urlIteam = baseURL + link.get('href')
            if ("http" in urlIteam) and ("view" in urlIteam):
                driver.get(urlIteam)            
                try:
                    bsObjItem = BeautifulSoup(driver.page_source, features="html.parser")
                    subject = bsObjItem.find(text='Temat :').findNext('td').text
                except Exception as e:
                    print('Exception: ', e)
                    subject = 'NoSubject'
                    if 'Twoja sesja nie jest już aktywna.' in driver.page_source:
                        print('Sesion expired')
                        break
                # Remove special characters from subject
                subject = subject.translate(str.maketrans(dict.fromkeys(' ')))
                print(subject)
                name = subject.translate(str.maketrans(dict.fromkeys(' :/|*?<>+[]')))
                name = 'Subject_' + name + get_random_string() + '_'
                make_screenshot(name)
    sleep(0.1)
