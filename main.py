import requests
import pyttsx3
import speech_recognition as sr
from decouple import config
from datetime import datetime
from functions.on_os import get_random_joke, find_my_ip, get_random_advice, get_latest_news, get_trending_movies, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, send_whatsapp_message
from functions.os_os import open_cmd, open_calculator, open_camera, open_notepad, open_discord
from random import choice
from utils import opening_text
from pprint import pprint


USERNAME = config('USER')
BOTNAME = config('BOTNAME')


engine = pyttsx3.init('sapi5')

# Setting speech Rate
engine.setProperty('rate', 170)

# Setting the Volume
engine.setProperty('volume', 100.0)

# Setting Voice Tone(Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


# Text to Speech Conversion
def speak(text):
    """speaks whatever text is passed to it"""

    engine.say(text)
    engine.runAndWait()


# Greet the user
def greet_user():
    """Greets the user according to the time currently"""
    
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning joke, {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Evening time, cookies time {USERNAME}")
    else:
        speak(f"Hello,{USERNAME}, Is it dark outside? My time, right?")
    speak(f"I am {BOTNAME} from Suicide Squad. What do you want from Harley?")


# Takes Input from User
def take_user_input():
    """user input, recognizes it using Speech Recognition module and converts it into text"""
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        if not 'exit' in query or 'stop' in query:
            speak(choice(opening_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good night joke, take care!")
            else:
                speak('Have a good day! keep hunting bats')
            exit()
    except Exception:
        speak('Sorry, could you speak what I understand. Could you repeat like that batsy?')
        query = 'None'
    return query


if __name__ == '__main__':
    greet_user()
    while True:
        query = take_user_input().lower()

        if 'open notepad' in query:
            open_notepad()

        elif 'open discord' in query:
            open_discord()

        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()

        elif 'open camera' in query:
            open_camera()

        elif 'open calculator' in query:
            open_calculator()

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f'Joke your IP is {ip_address}.\n For your sins, I am printing it on the screen as well.')
            print(f'Your IP Address is {ip_address}')

        elif 'wikipedia' in query:
            speak('What is there so intersting on Wikipedia, joke?')
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            speak(f"According to Wikipedia, {results}")
            speak("For your fun, I am printing it on the screen joke.")
            print(results)

        elif 'youtube' in query:
            speak('What do you want to play on Youtube, is it on harley sir?')
            video = take_user_input().lower()
            play_on_youtube(video)

        elif 'search on google' in query:
            speak('What do I say Google to search for, sir?')
            query = take_user_input().lower()
            search_on_google(query)

        elif "send whatsapp message" in query:
            speak(
                'Whom should I send the message sir? Please enter in the console: ')
            number = input("Enter the number: ")
            speak("What is the message you wish to convey?")
            message = take_user_input().lower()
            send_whatsapp_message(number, message)
            speak("I've sent the message joke.")

        elif "send an email" in query:
            speak("Tell me the email? will you? Please enter in the console: ")
            receiver_address = input("Enter email address: ")
            speak("What should be the subject joke?")
            subject = take_user_input().capitalize()
            speak("And, your message?")
            message = take_user_input().capitalize()
            if send_email(receiver_address, subject, message):
                speak("I've sent the mail.")
            else:
                speak("Something went wrong while I was sending the mail. Please check the error logs joke")

        elif 'joke' in query:
            speak(f"Why so serious? joker wants a joke...")
            joke = get_random_joke()
            speak(joke)
            speak("I am printing it on the screen. laugh on it")
            pprint(joke)

        elif "advice" in query:
            speak(f"Joke wants an advice from harley. Ok tell you some")
            advice = get_random_advice()
            speak(advice)
            speak("I am printing it on the screen.")
            pprint(advice)

        elif "trending movies" in query:
            speak(f"Suicide Squad please do watch and other trending movies are: {get_trending_movies()}")
            speak("I am also printing it on the screen joke.")
            print(*get_trending_movies(), sep='\n')

        elif 'news' in query:
            speak(f"Reading funny and laughable, oops! sorry latest news headlines")
            speak(get_latest_news())
            speak("You can also find it on screen")
            print(*get_latest_news(), sep='\n')

        elif 'weather' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(f"Getting weather over your city {city}")
            weather, temperature, feels_like = get_weather_report(city)
            speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
            speak(f"Also, as it says {weather}")
            speak("See the screen")
            print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")
