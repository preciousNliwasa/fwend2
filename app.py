from flask import Flask,request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import pickle
import numpy as np
from io import BytesIO
from PIL import Image
import pandas as pd

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
        phone_number = request.form.get('From')
        
    except (ValueError, TypeError):
        return "Invalid request: invalid or missing NumMedia parameter", 400
    response = MessagingResponse()
    
    outputt = requests.get(url = "https://1atqmr.deta.dev/get_all_plant_diseases/")
    dff = pd.DataFrame(outputt.json()['_items'])
    
    outputt2 = requests.get(url = "https://1atqmr.deta.dev/get_all_animal_diseases/")
    dff2 = pd.DataFrame(outputt2.json()['_items'])
    
    output_lan = requests.get(url = 'https://lkdzzx.deta.dev/get_user_current_language/')
    dff3 = pd.DataFrame(output_lan.json()['_items'])
    
    if not int(num_media):
      
        if ('hello' in inc) | ('hi' in inc) | ('lange' in inc) :
          msg = response.message("----------------LANGUAGE-------------------- \n Use Codes given to choose an option \n ---------------------------------------------------- \n ENG -- english \n CHW -- chichewa \n ------------------------------------------------------")
        
        elif ('langc' in inc):
           msg = response.message("---------------CHIYANKHULO------------------ \n gwirisani maletala akumazele kuti musankhe \n ---------------------------------------------------- \n ENG -- english \n CHW -- chichewa \n --------------------------------------------------------")
        
        elif ("eng" in inc) | ('mn' in inc):
          
          if np.any(dff3.user_number.values == phone_number):
            outp = 'nothing'    
          else:
            requests.post(url = 'https://lkdzzx.deta.dev/language_change/',params = {'user_number':phone_number,'lan' : 'english'})
            
          msg = response.message("----------------MAIN MENU------------------\n  Use Codes given to choose an option\n----------------------------------------------------- \n KNWD -- know about diseases \n KNWP -- know about plants \n KNWA -- know about animals \n KNWS -- know about shops \n KNWM -- know about manure \n KNWMA -- know about markets \n -------------------------------------------- \n LANGE -- change language ")
          
        elif (('knwd' in inc) | ('dsm' in inc)) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          msg = response.message("----------DISEASE MENU------------ \n --------------------------------------------\n PLT -- plant diseases \n ANM -- animal diseases \n ------------------------------------------------ \n MN -- to main menu")
    
        elif ('plt' in inc) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          output = requests.get(url = "https://1atqmr.deta.dev/get_all_plant_diseases/")
          df = pd.DataFrame(output.json()['_items'])
          msg = response.message('------PLANT DISEASES MENU---------- \n ---------------------------------------------- \n' + str(df[['Code','Disease']]) + '\n ' + '------------------------------------------------ \n DSM -- to diseases Menu')
          
        elif (np.any(dff.Code.values == inc) == True) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          pld_D = dff.loc[dff['Code'] == inc,'Description'].values
          msg = response.message(str(pld_D[0]))
        
        elif ('anm' in inc) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          output = requests.get(url = "https://1atqmr.deta.dev/get_all_animal_diseases/")
          df = pd.DataFrame(output.json()['_items'])
          msg = response.message('------ANIMAL DISEASES MENU---------- \n ---------------------------------------------- \n' + str(df[['Code','Disease']]) + '\n ' + '------------------------------------------------ \n DSM -- to diseases Menu')
          
        elif (np.any(dff2.Code.values == inc) == True) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          anm_D = dff2.loc[dff2['Code'] == inc,'Description'].values
          msg = response.message(str(anm_D[0]))
        
        elif ('chw' in inc) | ('mn' in inc):
          if np.any(dff3.user_number.values == phone_number):
            outp = 'nothing'    
          else:
            requests.post(url = 'https://lkdzzx.deta.dev/language_change/',params = {'user_number':phone_number,'lan' : 'chichewa'})
            
          msg = response.message("-----------TSAMBA LALIKULU------------\n  gwirisani maletala akumazele kuti musankhe \n----------------------------------------------------- \n KNWD -- dziwani za matenda \n KNWP -- dziwani za zomera \n KNWA -- dziwani za nyama \n KNWS -- dziwani za mashopu \n KNWM -- dziwani za manyowa \n KNWMA -- dziwani za misika \n -------------------------------------------- \n LANGC -- kusintha chiyankhulo")
          
        else:
          output = 'waiting'
          msg = response.message(output)
    
          
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
