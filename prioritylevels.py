import logging
import re

import requests
import json
logger = logging.getLogger(__name__)

class Priorities:
    lp_topics = []
    hp_topics = []
    high_prio_message = ""
    low_prio_message = ""

    def __init__(self, token):
		#Change to your own gitlabs url.
        self.url = 'GITLAB_URL/projects/NUMBERS/issues?private_token=' + token + '&per_page=200'
        self.r = requests.request("GET", self.url)
        self.response = json.loads(self.r.text)

    def showhptopics(self):
        message = "__**In Verification**__ \n"
        for topic in self.hp_topics:
            message = message + "> {} \n".format(topic)
        self.high_prio_message = message

    def showlptopics(self):
        message = "__**In Progress**__ \n"
        for topic in self.lp_topics:
            message = message + "> {} \n".format(topic)
        self.low_prio_message = message
    
    def get_topics(self):
        self.hp_topics.clear()
        self.lp_topics.clear()
        for element in self.response:
            if "In Verification" in element["labels"]:
                new_hp_topic = "#" + str(element["iid"]) + ": " + element["title"]
                if element["assignee"]:
                    new_hp_topic = new_hp_topic + " - **" + element["assignee"]["name"]+ "**"
                self.hp_topics.append(new_hp_topic)
            if "In Progress" in element["labels"]:
                new_lp_topic = "#" + str(element["iid"]) + ": " + element["title"]
                if element["assignee"]:
                    new_lp_topic = new_lp_topic + " - **" + element["assignee"]["name"]+ "**"
                self.lp_topics.append(new_lp_topic)
        self.showhptopics()
        self.showlptopics()
