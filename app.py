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
    
    # api output to get all plant diseases
    outputt = requests.get(url = "https://1atqmr.deta.dev/get_all_plant_diseases/")
    dff = pd.DataFrame(outputt.json()['_items'])
    
    # api output to get all plant diseases (chichewa)
    output5 = requests.get(url = "https://1atqmr.deta.dev/nthenda_zonse/")
    df5 = pd.DataFrame(output5.json()['_items'])
    
    # api output to get all animal diseases (chichewa)
    output6 = requests.get(url = "https://1atqmr.deta.dev/nthenda_zonse_za_ziweto/")
    df6 = pd.DataFrame(output6.json()['_items'])
    
    # api output to get all animal diseases 
    outputt2 = requests.get(url = "https://1atqmr.deta.dev/get_all_animal_diseases/")
    dff2 = pd.DataFrame(outputt2.json()['_items'])
    
    # api output to get user current languange of choice
    output_lan = requests.get(url = 'https://lkdzzx.deta.dev/get_user_current_language/')
    dff3 = pd.DataFrame(output_lan.json()['_items'])
    
    # api to get user current operation
    output_op = requests.get(url = 'https://lkdzzx.deta.dev/get_user_current_operation/')
    dff4 = pd.DataFrame(output_op.json()['_items'])
    
    output7 = requests.get(url = "https://1atqmr.deta.dev/get_animals/")
    dff7 = pd.DataFrame(output7.json()['_items'])
    
    output8 = requests.get(url = "https://1atqmr.deta.dev/get_crops/")
    dff8 = pd.DataFrame(output8.json()['_items'])
    
    
    
    if not int(num_media):
      
        # intro ,default language = eng,
        if ('hello' in inc) | ('hi' in inc) | ('lange' in inc) :
          msg = response.message("----------------LANGUAGE-------------------- \n Use Codes given to choose an option \n ---------------------------------------------------- \n ENG -- english \n CHW -- chichewa \n VN -- audio \n ------------------------------------------------------")
        
        # chichewa (language change)
        elif ('langc' in inc):
           msg = response.message("---------------CHIYANKHULO------------------ \n gwirisani maletala akumazele kuti musankhe \n ---------------------------------------------------- \n ENG -- english \n CHW -- chichewa \n VN -- audio \n --------------------------------------------------------")
        
        # changing to english
        elif ("eng" in inc) | ('mn' in inc):
          
          # updating to english if language was in chichewa
          if np.any(dff3.user_number.values == phone_number):
             requests.put(url = 'https://lkdzzx.deta.dev/update_language/',params = {'key':dff3.loc[dff3['user_number'] == phone_number,'key'].values[0],'user_number':phone_number,'lan' : 'english'})  
              
          else:
            # registering a new number in english
            requests.post(url = 'https://lkdzzx.deta.dev/language_change/',params = {'user_number':phone_number,'lan' : 'english'})
            
          msg = response.message("----------------MAIN MENU------------------\n  Use Codes given to choose an option\n----------------------------------------------------- \n KNWD -- know about diseases \n KNWP -- know about plants \n KNWA -- know about animals \n KNWS -- know about shops \n KNWM -- know about manure \n KNWMA -- know about markets \n -------------------------------------------- \n LANGE -- change language ")
        
        # knowing about diseases (english)
        elif (('knwd' in inc) | ('dsm' in inc)) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
                 
          msg = response.message("----------DISEASE MENU------------ \n --------------------------------------------\n PLT -- plant diseases \n ANM -- animal diseases \n ------------------------------------------------ \n MN -- to main menu")
        
        # knowing about plant diseases (english)
        elif ('plt' in inc) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          output = requests.get(url = "https://1atqmr.deta.dev/get_all_plant_diseases/")
          df = pd.DataFrame(output.json()['_items'])
          msg = response.message('------PLANT DISEASES MENU---------- \n ---------------------------------------------- \n' + str(df[['Code','Disease']]) + '\n ' + '------------------------------------------------ \n DSM -- to diseases Menu')
        
        # description of choosen plant disease (english)  
        elif (np.any(dff.Code.values == inc) == True) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          pld_D = dff.loc[dff['Code'] == inc,'Description'].values
          msg = response.message(str(pld_D[0]))
        
        # knowing about animal diseases (english)
        elif ('anm' in inc) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          output = requests.get(url = "https://1atqmr.deta.dev/get_all_animal_diseases/")
          df = pd.DataFrame(output.json()['_items'])
          msg = response.message('------ANIMAL DISEASES MENU---------- \n ---------------------------------------------- \n' + str(df[['Code','Disease']]) + '\n ' + '------------------------------------------------ \n DSM -- to diseases Menu')
         
        # description of choosen animal disease (english)
        elif (np.any(dff2.Code.values == inc) == True) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          anm_D = dff2.loc[dff2['Code'] == inc,'Description'].values
          msg = response.message(str(anm_D[0]))
          
        elif ('knwp' in inc) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          
          output = requests.get(url = "https://1atqmr.deta.dev/get_crops/")
          df = pd.DataFrame(output.json()['_items'])
          msg = response.message("----------CROPS MENU------------ \n --------------------------------------------\n" + str(df[['Code','Crop']]) + " ------------------------------------------------ \n MN -- to main menu")
          
        elif (np.any(dff8.Code.values == inc) == True) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          crops = dff8.loc[dff8['Code'] == inc,'Description'].values
          msg = response.message(str(crops[0]))
        
        elif ('knwa' in inc) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          
          output = requests.get(url = "https://1atqmr.deta.dev/get_animals/")
          df = pd.DataFrame(output.json()['_items'])
          msg = response.message("----------ANIMALS MENU------------ \n --------------------------------------------\n" + str(df[['Code','Animal']]) + " ------------------------------------------------ \n MN -- to main menu")
          
        elif (np.any(dff7.Code.values == inc) == True) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          animals = dff7.loc[dff7['Code'] == inc,'Description'].values
          msg = response.message(str(animals[0]))
        
        # changing to chichewa
        elif ('chw' in inc) | ('tsam' in inc):
          
          # updating lan to chichewa
          if np.any(dff3.user_number.values == phone_number):
            requests.put(url = 'https://lkdzzx.deta.dev/update_language/',params = {'key':dff3.loc[dff3['user_number'] == phone_number,'key'].values[0],'user_number':phone_number,'lan' : 'chichewa'}) 
           
          else:
            # lan to chichewa
            requests.post(url = 'https://lkdzzx.deta.dev/language_change/',params = {'user_number':phone_number,'lan' : 'chichewa'})
            
          msg = response.message("-----------TSAMBA LALIKULU------------\n  gwirisani maletala akumazele kuti musankhe \n----------------------------------------------------- \n KNWD -- dziwani za matenda \n KNWP -- dziwani za zomera \n KNWA -- dziwani za nyama \n KNWS -- dziwani za mashopu \n KNWM -- dziwani za manyowa \n KNWMA -- dziwani za misika \n -------------------------------------------- \n LANGC -- kusintha chiyankhulo")
        
        # knowing about diseases (chichewa)
        elif (('knwd' in inc) | ('tsaz' in inc)) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'chichewa'):
          msg = response.message("--------TSAMBA LA MATENDA---------- \n --------------------------------------------\n PLT -- matenda a zomera \n ANM -- matenda a nyama \n ------------------------------------------------ \n tsam -- tsamba lalikulu")
        
        # knowing about plant disease (chichewa)
        elif ('plt' in inc) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'chichewa'):
          output = requests.get(url = "https://1atqmr.deta.dev/nthenda_zonse/")
          df = pd.DataFrame(output.json()['_items'])
          msg = response.message('--TSAMBA LA MATENDA A ZOMERA-- \n ---------------------------------------------- \n' + str(df[['Letala','Matenda']]) + '\n ' + '------------------------------------------------ \n tsaz -- tsamba la zomera')
        
        # description of plant diseases (chichewa)
        elif (np.any(df5.Letala.values == inc) == True) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'chichewa'):
          pld_D = df5.loc[df5['Letala'] == inc,'Kulongosola'].values
          msg = response.message(str(pld_D[0]))
         
        # knowing about animal diseases (chichewa)
        elif ('anm' in inc) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'chichewa'):
          output = requests.get(url = "https://1atqmr.deta.dev/nthenda_zonse_za_ziweto/")
          df = pd.DataFrame(output.json()['_items'])
          msg = response.message('TSAMBA LA MATENDA A ZIWETO \n ---------------------------------------------- \n' + str(df[['Letala','Matenda']]) + '\n ' + '------------------------------------------------ \n tsaz -- tsamba la zomera')
        
        # description of choosen animal disease (chichewa)
        elif (np.any(df6.Letala.values == inc) == True) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'chichewa'):
          pld_D = df6.loc[df6['Letala'] == inc,'Kulongosola'].values
          msg = response.message(str(pld_D[0]))
          
        elif ('knwp' in inc) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'chichewa'):
          output = requests.get(url = "https://1atqmr.deta.dev/zomera_zonse/")
          df = pd.DataFrame(output.json()['_items'])
          msg = response.message("------TSAMBA LA ZOMERA------- \n --------------------------------------------\n" + str(df[['Letala','Zomera']]) + + "\n " + " ------------------------------------------------ \n tsam -- tsamba lalikulu")
          
        elif (np.any(dff8.Code.values == inc) == True) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'chichewa'):
          crops = dff8.loc[dff8['Code'] == inc,'Description'].values
          msg = response.message(str(crops[0]))  
          
        elif ("vn" in inc) | ('mx' in inc):
          
          # updating to english_vn if language was in chichewa or eng
          if np.any(dff3.user_number.values == phone_number):
             requests.put(url = 'https://lkdzzx.deta.dev/update_language/',params = {'key':dff3.loc[dff3['user_number'] == phone_number,'key'].values[0],'user_number':phone_number,'lan' : 'english_vn'})  
              
          else:
            # registering a new number in english_vn
            requests.post(url = 'https://lkdzzx.deta.dev/language_change/',params = {'user_number':phone_number,'lan' : 'english_vn'})
            
          msg = response.message('VN MENU')
          msg.media('https://1atqmr.deta.dev/stream/menu.mp4')
        
        else:
          output = 'still in development'
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
            msg = response.message('we dont understand what you have given bro')
          
    return str(response)
 
if __name__ == '__main__':
  app.run()
