from flask import Flask,request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import pickle
import numpy as np

app = Flask(__name__)                    

@app.route('/')
def home():
  return ('hello')

## this function cant work , some variables were removed
@app.route('/chat',methods = ['POST'])
def chat():
  inc = request.values.get('Body','').lower()
  resp = MessagingResponse()
  mess = resp.message()
  
  answ = chatbot.get_response(inc)
  mess.body(str(answ))
  
  return str(resp)


GOOD_BOY_URL = "https://49t059.deta.dev/stream/"

from skimage.transform import  resize

@app.route("/whatsapp", methods=["GET", "POST"])
def reply_whatsapp():

    try:
        num_media = request.values.get("NumMedia")
    except (ValueError, TypeError):
        return "Invalid request: invalid or missing NumMedia parameter", 400
    response = MessagingResponse()
    if not int(num_media):
        inc = request.values.get("Body","").lower()
        if inc in requests.get("https://49t059.deta.dev/get_photos_list").text:
          msg.media(GOOD_BOY_URL + inc)
          
        msg = response.message("Send nliwasa an image!")
    else:
        msg = response.message('Thank you for sending nliwasa an image')
        msg.media(GOOD_BOY_URL)
    return str(response)
 
if __name__ == '__main__':
  app.run()
