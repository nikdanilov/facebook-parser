from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.support.ui as ui
import random
import os

from bs4 import BeautifulSoup as bs
from time import sleep

import re

class FacebookParser:

    def __init__(self, turl):
        self.chrome_options = Options()
        self.chrome_options.add_argument("user-data-dir=./chrome_data/")
        self.b = webdriver.Chrome(os.getcwd() + "\chromedriver.exe", chrome_options=self.chrome_options)
        self.actions = ActionChains(self.b)

        self.url = turl

        self.login = ""
        self.password = ""

        self.checkLogin()

    def checkLogin(self):
        self.b.get('https://facebook.com')

        print("wait page load, sleep 2s")
        sleep(2)

        # LOGIN
        if "royal_pass" in self.b.page_source:  # check if account is logged in
            self.b.execute_script("document.querySelector('[data-testid=royal_email]').value = '{}';".format(self.login))
            self.b.execute_script("document.querySelector('[data-testid=royal_pass]').value = '{}';".format(self.password))
            self.b.execute_script("document.querySelector('#login_form').submit();".format(self.password))

    def getCounters(self):

        self.b.get(self.url)
        pbs = bs(self.b.page_source, "lxml")
        likes = 0
        followers = 0
        for div in pbs.findAll("div"):
            if "people like this" in div.text and str(div).count("<div ") < 2:
                likes = int(''.join(re.findall('\d+', div.text )))
                break

        for div in pbs.findAll("div"):
            if "people follow this" in div.text and str(div).count("<div ") < 2:
                followers = int(''.join(re.findall('\d+', div.text )))
                break

        return [likes, followers]

    def getInfo(self):
        self.b.get("{}about".format(self.url))
        pbs = bs(self.b.page_source, "lxml")

        born = ""
        personal_interests = ""
        affilation = ""
        about = ""
        bio = ""
        gender = ""
        personal_info = ""

        for div in pbs.findAll("div"):
            if "Born on " in div.text and str(div).count("<div ") < 2:
                born = div.text.split("Born on ")[1]

            if "Personal Interests" in div.text and str(div).count("<div ") < 2:
                personal_interests = div.findNext('div').text

            if "Affilation" in div.text and str(div).count("<div ") < 2:
                affilation = div.findNext('div').text

            if div.text == "About" and str(div).count("<div ") < 2:
                about = div.findNext('div').text

            if div.text == "Biography" and str(div).count("<div ") < 2:
                bio = div.findNext('div').text
                bio = bio.replace("...", "")
                bio = bio.replace("See More", "")

            if div.text == "Gender" and str(div).count("<div ") < 2:
                gender = div.findNext('div').text

            if div.text == "Personal Information" and str(div).count("<div ") < 2:
                personal_info = div.findNext('div').text

        return {
            "born": born,
            "personal_interests": personal_interests,
            "affilation": affilation,
            "about": about, "bio": bio,
            "gender": gender,
            "personal_info": personal_info
        }

f = FacebookParser("https://www.facebook.com/Anthony.Morrison/")
print(f.getInfo())
print(f.getCounters())