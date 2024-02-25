import speech_recognition as sr
import pyttsx3
import os
from openai import OpenAI
import datetime
import platform
import unicodedata

def remove_non_ascii_characters(s):
    """
    Remove non-ASCII characters from the string.
    """
    return ''.join(c for c in s if unicodedata.category(c)[0] != 'C')

    # HEADER = '\033[95m'
    # MAVI = '\033[94m'
    # YESIL = '\033[92m'
    # SARI = '\033[93m'
    # KIRMIZI = '\033[91m'
    # BEYAZ = '\033[0m'
    # BOLD = '\033[1m'
    # UNDERLINE = '\033[4m'


client = OpenAI(
                base_url = 'http://localhost:11434/v1',
                api_key='ollama',
    )

file = open('history.txt', 'a')
now = datetime.datetime.now()
file.write(str(now)+"\n")

def beep():
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(1000, 500)  # frequency in Hz and duration in milliseconds
    else:
        # For Unix/Linux-based systems
        os.system("echo -n '\a';sleep 0.2;echo -n '\a'")  # You may adjust sleep duration

beep()


# Yapay zeka uygulamasina erismek icin kullanilacak fonksiyon
def get_ai_response(input_text):

            # Initialize ollama 
        try:
        #     client = OpenAI(
        #                     base_url = 'http://localhost:11434/v1',
        #                     api_key='ollama',
        #     )

            response = client.chat.completions.create(
                # model="phi",
                model="mistral",
                messages=[
                    {"role": "system","content": "you are a helpful ai asistant named Jarvis. Answer questions briefly, in a sentence or less. And also this is our previous conversation:" + str(chat_history)+"please dont repeat previous conversations every time."},
                    {"role": "user","content": input_text}
                ],
            )

#*******************
            if response and response.choices:
                # print('ollama:', response.choices[0].message.content)
                return response
            else:
                print("No answer from Ollama_1")
                return ()
        except Exception as e:
            print("No answer from Ollama_2")
            print("Error:", e)
            return ()


# Recognizer
recognizer = sr.Recognizer()

#(text-to-speech) 
voice = pyttsx3.init()

chat_history = []  # Sohbet gecmisini saklamak icin bos bir liste olusturun

while True:
    try:
        # Mikrofondan ses al
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)  # Calibrate the recognizer
            print("Listened for ambient noise ...")
            # beep()
            print("Dinliyorum...")
            audio_data = recognizer.listen(source)

        # Ses verisini metne cevir
        user_input = recognizer.recognize_whisper(audio_data)
        # user_input = recognizer.recognize_sphinx(audio_data)
        # user_input = recognizer.recognize_google(audio_data)
        print('\033[94m'+"Kullanici Girdisi:", user_input)
        
        kapat=1
        if "hey jarvis" in user_input.lower():

            # hello boss 
            voice.say("Hello Boss! I am listening")
            voice.setProperty('rate', 180)  # speed of reading 145

            voice.runAndWait()
            # tekrar dinlemeye başla 


            beep()
            while kapat == 1:
                
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source)  # Calibrate the recognizer
                    print("Listening to answer.")
                    audio_data = recognizer.listen(source)
                    user_input = recognizer.recognize_whisper(audio_data)
                    print("user_input ",user_input)

                    close_control= user_input.lower()
                if "close jarvis" in close_control:
                    kapat=0
                    print("Kapat geldi")                    
                    voice.say("Good bye!")
                    voice.setProperty('rate', 180)  # speed of reading 145
                    voice.runAndWait()
                    pass

                elif "exit" in user_input.lower():
                    kapat=0
                    voice.say("Exiting! Good bye!")
                    voice.setProperty('rate', 180)  # speed of reading 145
                    voice.runAndWait()
                    print("Exit geldi, Cikis yapiliyor...")
                    break

                elif "thank you" in user_input.lower():
                    kapat=0
                    voice.say("Your welcome! Good bye!")
                    voice.setProperty('rate', 180)  # speed of reading 145
                    voice.runAndWait()
                    print("Exit geldi, Cikis yapiliyor...")
                    break
                else:
                    kapat=1
                    file.write(str(user_input)+"\n")
                    # Yapay zeka uygulamasindan yanit al

                    response=get_ai_response(user_input)
                    print('\033[93m'+"Yapay Zeka Yaniti:", response.choices[0].message.content)
                    # Sohbet gecmisine inputu ekle
                    chat_history.append(remove_non_ascii_characters(user_input))        
                    # Sohbet gecmisine yaniti ekle

                    chat_history.append(response.choices[0].message)

                    try:
                        print(str(response.choices[0].message.content))
                        for_writer = remove_non_ascii_characters(response.choices[0].message.content)  # Implement remove_non_ascii_characters function as needed

                        file.write(str(for_writer)+"\n")
                    except sr.RequestError as e:
                        print("Yazmada Sorun yasandi",e)
                        # print("Yazmada Sorun yasandi; {0}".format(e))  
                        pass                      
                    # Yaniti sesli olarak kullaniciya iletiyoruz
                    voice.say(response.choices[0].message.content)
                    voice.setProperty('rate', 180)  # speed of reading 145
                    voice.runAndWait()
                    # print("chat_history:",chat_history)

                    pass

        elif "exit" in user_input.lower():
            voice.say("Exiting! Good bye!")
            voice.setProperty('rate', 180)  # speed of reading 145
            voice.runAndWait()
            print("Exit geldi, Cikis yapiliyor...")
            file.close()
            break
        
        else:
            print("not send to AI.")
    except sr.UnknownValueError:
        print("Anlasilamadi")
    except sr.RequestError as e:
        print("Sorun yasandi; {0}".format(e))
    except KeyboardInterrupt:
        print("Cikis yapiliyor...")
        file.close()
        break
