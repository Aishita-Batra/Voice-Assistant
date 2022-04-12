import wolframalpha
import wikipedia
import requests
import playsound
import os
import speech_recognition as sr
import pyttsx3



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices)
# print(voices[0].id)
engine.setProperty('voice', voices[0].id)

def speak(text):
    if(type(text) == bytes):    #when string too large, it is in bytes type
        text = text.decode('utf-8')
        arr = text.split('. ', 2)
        text = arr[0] + '. ' + arr[1] + '.'
     
    print("To be spoken: ", text)
    engine.say(text)
    engine.runAndWait()


def removeBrackets(variable):
    return variable.split('(')[0]


def resolveListOrDict(variable):
    if isinstance(variable, list):
        return variable[0]['plaintext']
    else:
        return variable['plaintext']


def wiki_search(question):
    results = wikipedia.search(question)

    if not results:
        print("No results found for your search")
        return

    try:
        page = wikipedia.page(results[0])
    except wikipedia.DisambiguationError as err:  #multiple results for same query (OR) question interpreted in more than one way
        page = wikipedia.page(err.options[0])     #then return 1st option
    except:
        #print("Some unexpected error occured. Please try again.")
        speak("Some unexpected error occured. Please try again.")
        return

    #title = page.title.encode('utf-8')
    content = page.summary.encode('utf-8')
    #print(content)
    speak(content)


def wolf_ram_compute(client, text):
    res = client.query(text)
    
    # question not resolved by wolfram
    if res['@success'] == 'false':
       # print('Question cannot be resolved')
        speak("Searching from wikipedia")
        wiki_search(text)        
    else:
        result = ''
        # pod[0] contains simplified question with only keywords in it.
        pod0 = res['pod'][0]
        # pod[1] may contains the answer
        pod1 = res['pod'][1]
        
        # check if pod1 has primary=true or title=result|definition
        if (('definition' in pod1['@title'].lower()) or ('result' in  pod1['@title'].lower()) or (pod1.get('@primary','false') == 'true')):
          # extracting result from pod1
          result = resolveListOrDict(pod1['subpod'])
          #print(result)
          speak(result)
          question = resolveListOrDict(pod0['subpod'])
          question = removeBrackets(question)
        else:
          # extracting wolfram question interpretation from pod0
          question = resolveListOrDict(pod0['subpod'])
          # removing unnecessary parenthesis for simplicity
          question = removeBrackets(question)
          
          #print("Searching from wiki...")
          speak("Searching from wikipedia")
          wiki_search(question)
    

def get_audio(): 
  
    rObject = sr.Recognizer() 
    audio = '' 
  
    with sr.Microphone() as source: 
        print("Speak...") 
          
        # recording the audio using speech recognition 
        audio = rObject.listen(source, phrase_time_limit = 5)  
    print("Stop.") # limit 5 secs 
  
    try: 
  
        text = rObject.recognize_google(audio, language ='en-US') 
        print("You : ", text) 
        return text 
  
    except: 
  
        speak("Could not understand your audio, Please try again!") 
        return 0




#MAIN METHOD
def main():
    text = ''
    user_id = "J4URRJ-ULPLQ7XPWP"
    client = wolframalpha.Client(user_id) # Instance of wolfram alpha 

    while text != "end" :

        text = get_audio()
        if text == 0 :
            continue
        text = text.lower()
        if text == 'exit' or text == 'stop':
            break
        wolf_ram_compute(client, text)
    
main()    


