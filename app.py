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


bird = "https://49t059.deta.dev/stream/birdtensor.jpg"
zuki = "https://49t059.deta.dev/stream/zuki.jpg"
gh = "https://49t059.deta.dev/stream/gh.jpg"

from skimage.transform import  resize

@app.route("/whatsapp", methods=["GET", "POST"])
def reply_whatsapp():

    try:
        num_media = request.values.get("NumMedia")
        inc = request.values.get("Body","").lower()
    except (ValueError, TypeError):
        return "Invalid request: invalid or missing NumMedia parameter", 400
    response = MessagingResponse()
    if not int(num_media):
        if 'bird' in inc:
          msg = response.message('Here is the bird')
          msg.media(bird)
          
        elif 'chanco' in inc:
          msg = response.message('Here is chanco')
          msg.media(gh)
          
        else:
          msg = response.message("Send nliwasa an image or make a request!")
          
    else:
        msg = response.message('Thank you for sending nliwasa an image')
        msg.media(zuki)
    return str(response)
 
if __name__ == '__main__':
  app.run()
