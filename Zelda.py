import pyttsx3
import speech_recognition as sr
import pywhatkit
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import datetime
import wikipedia
import webbrowser
import pytz


tz = pytz.timezone("America/Chicago")

alarm_hour = "0"
alarm_minute = "0"

SPOTIPY_CLIENT_ID  = '8370e985cf264f3e91e29e34b8909f74'
SPOTIPY_CLIENT_SECRET = 'b0bdb78d33dd43ceafa2f0666447bde2'
SPOTIPY_REDIRECT_URI = 'http://www.google.com/'
scope = "user-read-playback-state,user-modify-playback-state"
#https://open.spotify.com/user/12838150?si=VdIFKVftSQeZ5ljQhwAuTg
username = '12838150'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri = SPOTIPY_REDIRECT_URI,
                                               scope = scope))

res = sp.devices()
player = res['devices'][0]['id']
playlists = sp.current_user_playlists()



listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[3].id)
def talk(text):
    engine.say(text)
    engine.runAndWait()

def current_time():
    all = datetime.datetime.now(tz=tz).isoformat()
    time = all[11:16]
    return time

def bow_down():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'zelda' in command:
                command = command.replace('zelda', '')


    except:
        command = ''
    return command

def run(alarm_hour, alarm_minute):
    alarm_time = alarm_hour+":"+alarm_minute
    if current_time() == alarm_time:
        sp.start_playback(device_id=player, context_uri=f"spotify:playlist:3YAWWAgBiQbY2atHxVshvM")
        sp.volume(volume_percent=60, device_id=player)
    command = bow_down()
    if 'anime' in command:
        webbrowser.open(url="http://crunchyroll.com/")
    if 'pause' in command:
        sp.pause_playback(device_id=player)
    if 'play' in command:
        if 'spotify' in command:
            talk("你想听什么呀？")
            command = bow_down()

            for playlist in playlists['items']:
              name = playlist['name'].split(" ")[0].lower()
              id = playlist['id']
              if name in command:

                  sp.start_playback(device_id=player, context_uri=f"spotify:playlist:"+id)
              else:
                  pass
        if 'youtube' in command:
            talk("你想听什么呀？")
            command = bow_down()
            song = command.replace('play', '')
            pywhatkit.playonyt(song)
            talk("正在播放音乐")

    elif "time" in command:
        time = datetime.datetime.now().strftime("%H:%M")


        talk("现在是" + time)

    elif "date" in command:

        month = str(datetime.datetime.now().month)
        day = str(datetime.datetime.now().day)

        talk("现在是" + month + "月" + day + "日")
    # ADD WEATHER
    # ADD IS "?"
    # ADD WHERE WHEN WHY HOW
    elif "who" in command or "what" in command:
        try:
            thing = command.replace("who", "")
        except:
            thing = command.replace("what", "")
        info = wikipedia.summary(thing, 1)
        talk(info)
    elif "shut down" in command:
        exit()
    elif "alarm" in command:
        talk("你要几点钟起来啊？")
        command = bow_down()
        time  = command.split(" ")[0].split(":")
        alarm_hour = time[0]
        alarm_minute = time[1]
        print(alarm_hour)
        print(alarm_minute)

    else:
        pass

    return alarm_hour, alarm_minute
while True:
    alarm_hour, alarm_minute = run(alarm_hour, alarm_minute)
