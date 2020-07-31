# Webmail-Scraper

**Simple webmail scraper prototype**

### Description
Waits for changes in input file. When receive new URL then starts scraping. If there is no errors, it sends notification via Messenger and save screenshot of every page from web mailbox to local directory

### Requirements
* python3
* following packages: selenium, bs4, time, random, string, fbchat, os, datetime
* fb email, password to send notification and ID of fb profile as recipient
* chromium


Hint: install fbchat using command `pip install git+https://github.com/carpedm20/fbchat.git`. Run script with a non-root user