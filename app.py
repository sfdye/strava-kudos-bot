from __future__ import print_function

import logging
import json
import os
import sys

from flask import Flask, request
import requests
import sendgrid
from sendgrid.helpers.mail import *
from stravalib import Client

MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN')
STRAVA_ACCESS_TOKEN = os.environ.get('STRAVA_ACCESS_TOKEN')


logger = logging.getLogger(__name__)

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)


def sendgrid_email(to_email):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("test@example.com")
    subject = "Hello World from the SendGrid Python Library!"
    to_email = Email(to_email)
    content = Content("text/plain", "Hello, Email!")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    logger.info(response.status_code)
    logger.info(response.body)
    logger.info(response.headers)


def send_email(to_addr):
    logger.info('Sending email to {}'.format(to_addr))
    requests.post(
        "https://api.mailgun.net/v3/{}/messages".format(MAILGUN_DOMAIN),
        auth=("api", MAILGUN_API_KEY),
        data={"from": "Excited User <mailgun@YOUR_DOMAIN_NAME>",
              "to": [to_addr, "YOU@YOUR_DOMAIN_NAME"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomness!"})


def give_kudos(activity_id):
    client = Client(access_token=STRAVA_ACCESS_TOKEN)
    athlete = client.get_athlete()
    logger.info('Giving kudos to {}'.format(athlete.username))
    logger.info('Email: {}'.format(athlete.email))
    sendgrid_email(athlete.email)

@app.route("/webhook", methods=['POST'])
def webhook():
    logger.info('payload = \n{}'.format(request.json))
    data = request.json
    activity_id = data['activity_link'].strip().split('/')[-1]
    give_kudos(activity_id)
    return 'ok'
