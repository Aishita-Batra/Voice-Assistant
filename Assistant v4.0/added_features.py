import wolframalpha
import wikipedia
import requests
import os
import speech_recognition as sr
import pyttsx3
import config
import webbrowser
import datetime
import time


engine = pyttsx3.init()
voices = engine.getProperty('voices')
# print(voices)
# print(voices[0].id)
engine.setProperty('voice', voices[0].id)
# print(engine.getProperty('rate'))
engine.setProperty('rate', 175)


def speak(text):
    if(type(text) == bytes):  # when string too large, it is in bytes type
        text = text.decode('utf-8')
        arr = text.split('. ', 2)
        if len(arr) > 1:
            text = arr[0] + '. ' + arr[1] + '.'
        else:
            text = arr[0] + '. '

    print("Assistant: ", text)
    engine.say(text)
    engine.runAndWait()


def get_audio():

    rObject = sr.Recognizer()
    audio = ''

    with sr.Microphone() as source:
        print("Listening...")
        audio = rObject.listen(source, phrase_time_limit=5)

    try:
        print("Recognizing...")
        text = rObject.recognize_google(audio, language='en-US')
        print("You : ", text)
        return text

    except:

        speak("Could not understand your audio, Please say that again!")
        return 0


def welcome():

    hour = int(datetime.datetime.now().hour)

    if(hour >= 0 and hour < 12):
        speak("Good Morning!")

    elif(hour >= 12 and hour < 18):
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    time.sleep(0.1)
    speak("Please tell how may I help you?")


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
    # multiple results for same query (OR) question interpreted in more than one way
    except wikipedia.DisambiguationError as err:
        page = wikipedia.page(err.options[0])  # then return 1st option
    except:
        #print("Some unexpected error occured. Please try again.")
        speak("Some unexpected error occured. Please try again.")
        return

    #title = page.title.encode('utf-8')
    content = page.summary.encode('utf-8')
    # print(content)
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
        if (('definition' in pod1['@title'].lower()) or ('result' in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true')):
            # extracting result from pod1
            result = resolveListOrDict(pod1['subpod'])
            # print(result)
            speak(result)
            question = resolveListOrDict(pod0['subpod'])
            question = removeBrackets(question)
        else:
            # extracting wolfram question interpretation from pod0
            question = resolveListOrDict(pod0['subpod'])
            # removing unnecessary parenthesis for simplicity
            question = removeBrackets(question)

            print("Searching from Wikipedia...")
            #speak("Searching from wikipedia")
            wiki_search(question)


def location_search():
    speak("What do you want to search?")
    search_term = get_audio()
    url = f"https://google.nl/maps/place/{search_term}/&amp;"
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open(url)
    speak(f"Here is the location of {search_term}")


def giveNews():
    apiKey_news = 'a4e8129886fd4f9ea96d0ff90bbb8618'
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={apiKey_news}"
    response = requests.get(url)
    data = response.json()
    data = data["articles"]
    flag = True
    count = 0
    for items in data:
        count += 1
        if count > 10:
            break
        # print(items["title"])
        to_speak = items["title"].split(" - ")[0]
        if flag:
            speak("Today's top ten Headlines are:")
            flag = False
        else:
            speak("Next news:")
        speak(to_speak)


def open_application(input):

    if "chrome" in input:
        speak("Opening Google Chrome")
        os.startfile(
            'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
        return

    elif 'open google' in input:
        url = "google.com"
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url)

    elif "word" in input:
        speak("Opening Microsoft Word")
        os.startfile(
            'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\\Word 2016.lnk')
        return

    elif "excel" in input:
        speak("Opening Microsoft Excel")
        os.startfile(
            'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\\Excel 2016.lnk')
        return

    elif 'open youtube' in input:
        speak("Opening YouTube")
        url = "youtube.com"
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url)

    elif "control panel" in input or "settings" in input:
        speak("Opening Control Panel")
        os.startfile(
            r'C:\Users\shiva\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\System Tools\Settings.exe %s')
        return

    elif "opera" in input:
        speak("Opening Opera Browser")
        os.startfile(
            'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\\Opera Browser.lnk')
        return

    elif "edge" in input:
        speak("Opening Microsoft Edge")
        os.startfile(
            'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\\Microsoft Edge.lnk')
        return

    elif "notepad" in input:
        speak("Opening Notepad++")
        os.startfile(
            'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\\Notepad++.lnk')
        return

    elif "powerpoint" in input or "power point" in input:
        speak("Opening Powerpoint")
        os.startfile(
            'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\\PowerPoint 2016.lnk')
        return

    else:
        speak("Application not available")
        return


# MAIN METHOD
def main():
    text = ''
    wolfram_user_id = "J4URRJ-ULPLQ7XPWP"
    client = wolframalpha.Client(wolfram_user_id)
    welcome()

    while text != "end":

        text = get_audio()
        if text == 0:
            continue
        text = text.lower()
        if text == 'exit' or text == 'stop' or 'bye' in text or 'thank you' in text or 'thanks' in text:
            break

        elif 'news' in text or 'headlines' in text:
            giveNews()

        elif 'location' in text:
            location_search()

        elif "calculate" in text:

            client = wolframalpha.Client(wolfram_user_id)

            indx = text.lower().split().index('calculate')
            query = text.split()[indx + 1:]
            try:
                res = client.query(' '.join(query))
                answer = next(res.results).text
                speak("The answer is " + answer)
            except:
                speak(
                    "Could not calculate your result. Please query after the keyword \"calculate\".")

        elif 'open' in text.lower():
            open_application(text.lower())

        else:
            wolf_ram_compute(client, text)

        time.sleep(2)
        speak("What else can I do for you?")

main()
