import os

from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)
app.config.from_object('config')

@app.route("/answer", methods=['GET', 'POST'])
def voice():
    response = VoiceResponse()
    response.dial(app.config.get("PHONE"),timeout=30, action="/status")
    return str(response)

@app.route("/error", methods=['POST'])
def error():
    response = VoiceResponse()
    response.say("Sorry, I am not able to reach him, please try again!")
    return str(response)

@app.route("/status", methods=['GET','POST'])
def status():
    status=request.values.get("DialCallStatus")
    hasFailed = status == "failed" or status == "busy" or status =="no-answer" or status =="cancelled"
    if hasFailed:
        response = VoiceResponse()
        response.say("The caller you dialed is currently busy!, please try again later")
        response.hangup()
    return str(response)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",port=3000)
