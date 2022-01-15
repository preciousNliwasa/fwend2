from flask import Flask,request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import pickle
import numpy as np
from io import BytesIO
from PIL import Image

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
know_api= "https://r1lp8q.deta.dev/know/"

def post_photo(url):
  rr = requests.get(url)
  img = Image.open(BytesIO(rr.content))
  return str(type(img)) + 'was submitted'

from skimage.transform import  resize

@app.route("/whatsapp", methods=["GET", "POST"])
def reply_whatsapp():

    try:
        num_media = request.values.get("NumMedia")
        inc = request.values.get("Body","").lower()
        media = request.values.get('MediaContentType0', '')
    except (ValueError, TypeError):
        return "Invalid request: invalid or missing NumMedia parameter", 400
    response = MessagingResponse()
    if not int(num_media):
        if (("hello") | ("hi")) in inc:
          msg = response.message(''' knwd -- know disease
                                       knwdp -- know plant
                                       knwa -- know animal''')
        elif 'knwd' in inc:
          url_data = requests.get(know_api,params = {request : 'knwd'})
          msg = response.message(url_data.text)
            
        else:
          msg = 'waiting'
          
    else:
        if media.startswith('image/'):
            file_url = request.values['MediaUrl0']
            msg = response.message(post_photo(file_url))
            msg.media(file_url)
            
        elif media.startswith('video/'):
            file_url = request.values['MediaUrl0']
            msg = response.message('you sent us this video')
            msg.media(file_url)
            
        else:
            msg = response.message('we dont understand what you have given')
          
    return str(response)
 
if __name__ == '__main__':
  app.run()
