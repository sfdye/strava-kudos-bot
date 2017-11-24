from __future__ import print_function
from flask import Flask, request
from stravalib import Client
import json
import os
import sys
import logging

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)
logger = logging.getLogger(__name__)

def give_kudos(activity_id):
    client = Client(access_token=os.environ.get('STRAVA_ACCESS_TOKEN'))
    athlete = client.get_athlete()
    # activity = client.get_activity(207650614)
    logger.info('Giving kudos to {}'.format(athlete.username))
    logger.info('Email: {}'.format(athlete.email))

@app.route("/webhook", methods=['POST'])
def webhook():
    logger.info('payload = \n{}'.format(request.json))
    data = request.json
    activity_id = data['activity_link'].strip().split('/')[-1]
    give_kudos(activity_id)
    return 'ok'
