from flask import Flask,request
from twilio.twiml.messaging_response import MessagingResponse
import requests
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbott = ChatBot('Fwend')
app = Flask(__name__)                    

trainer = ChatterBotCorpusTrainer(chatbott)
trainer.train('chatterbot.corpus.english')

@app.route('/')
def home():
  return ('hello')

@app.route('/chat',methods = ['POST'])
def chat():
  inc = request.values.get('Body','').lower()
  resp = MessagingResponse()
  mess = resp.message()
  
  answ = chatbot.get_response(inc)
  mess.body(str(answ))
  
  return str(resp)
 
if __name__ == '__main__':
  app.run()
