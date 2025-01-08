from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
from gtts import gTTS
import speech_recognition as sr
import playsound
import os
import datetime
import pandas as pd
import re
import random
import pyaudio
import wave
from pydub import AudioSegment


# Create a sample DataFrame
data_en = ({'Text':["FEVER", "COUGH", "ACIDITY", "DIABETES", "HEADACHE", "JOINT PAIN", "COMMON COLD", "STOMACH PAIN", "PERIOD PROBLEMS", "FEELING SAD", "UNWANTED HAIR", "HOARSNESS", "VISION PROBLEM", "BURNING OF EYE", "SWELLING IN EYES", "MIGRAINE", "NOT ABLE TO HAVE A CHILD [FEMALE]", "HAIR LOSS", "MUSCLE CRAMPS", "OVERWEIGHT", "BLOOD IN VOMIT","STOMACH FEELING FULL", "DRY MOUTH", "COVID-19", "SEIZURE", "SNEEZING", "IRRITABILITY", "FEELING FAINT", "CHEST PAIN", 
            "KNOT AROUND NECK", "DOUBLE VISION", "DIFFICULTY IN SWALLOWING", "TOOTH EROSION", "TOOTH PAIN", "CAVITIES", "DECREASED OR NO URINE", "FASTER HEARTBEAT", "SENSITIVE TO LIGHT", "EAR FULLNESS", "PAIN IN EAR", "SKIN RASH", "NOSE BLEED", "FOREIGN BODY IN EYE", "SINUS PAIN", "SNORING", "FOOD POISONING", "FEAR", "NECK SWELLING", "NECK PAIN", "STUNTED GROWTH", "SORE THROAT", "KIDNEY STONES", "DIFFICULTY IN BREATHING", "BAD BREATH", "BLOOD IN URINE", 
            "HEARING LOSS ", "NO SENSATION", "DRY/ ITCHY EYES", "HEAD INJURY", "ITCHING IN NOSE", "JAUNDICE", "NOT ABLE TO SLEEP", "FEELING LIKE VOMITING", "DELAYED PUBERTY", "DEFORMITY OF JOINTS", "JAW PAIN", "WATERY EYES", "TIREDNESS/ WEAKNESS", "EAR DISCHARGE", "INJURY", "BLOOD IN STOOLS", "BLACK SPOT", "NOT FEELING HUNGRY", "LOSE MOTIONS", "MOOD SWING", "PROBLEM WITH GUMS", "LUMP IN MOUTH", "WEIGHT GAIN", "RUNNY NOSE", "PAIN IN NOSE", "BLOCKED NOSE", 
            "NASAL OBSTRUCTION", "LUMP IN NOSE", "EYE PAIN", "NOT ABLE TO HAVE A CHILD [MALE]", "INCREASE IN URINE FREQUENCY", "BURNING URINE", "CONSTIPATION", "SHAKING", "NOSE DEFORMITY", "REDNESS OF EYE", "RINGING IN EAR", "REDUCED STREAM OF URINATION", "NOISY BREATHING", "WHEEZING", "ANXIETY", "STRESS", "MOUTH ULCERS", "BLADDER STONES",  "BREAKAGE IN URINE FLOW", "NOT ABLE TO CONTROL URINE", "CONFUSION", "VOMITING", "SLEEP APNEA", "EXCESSIVE FEELING", 
            "SWELLING AROUND NOSE", "SEMEN IN URINE", "FEELING FAINT WHEN STANDING"]})

data_ta = ({'Text':['காய்ச்சல்','இருமல்','அமிலத்தன்மை' ,'நீரிழிவு நோய்','தலைவலி' ,'முட்டு வலி' ,'பொதுவான சளி','வயிற்று வலி','மாதவிடாய்  சிக்கல்கள்', 'சோகம்','தேவையற்ற முடி' ,'கம்மிய குரல்' ,'பார்வை கோளாறு', 'கண் எரிச்சல்' ,'கண் வீக்கம்','ஒற்றைத் தலைவலி','மலட்டுத்தன்மை  [பெண்கள்]','முடி இழப்பு','தசைப்பிடிப்பு ','அதிக உடல் எடை' ,'வாந்தியில் இரத்தம்','உலர்வான வாய்' ,'கோவிட்-19','வலிப்பு','எரிச்சல்' ,'மயக்கம் உணர்தல்','நெஞ்சு வலி','கழுத்தைச் சுற்றி சுழலை', 'இரட்டை பார்வை', 'பல் தேய்மானம்','பல் வலி','பல் சொத்தை', 'சிறுநீர் குறைவு அல்லது சிறுநீர் வாய்மை', 'இதயம் வேகமாக துடித்தல்', 'அதிக ஒளி உணர்திறன்','காது அடைப்பு' ,'காது வலி','தோல் வெடிப்பு ','மூக்கில் இரத்தம் வடித்தல்',
             'கண்ணில் வெளிப்புற பொருட்கள்', 'சைனக்ஸ் வலி','குறட்டை','உணவு விஷம்','பயம்','கழுத்து விக்கம்', 'கழுத்து வலி', 'குன்றிய வளர்ச்சி', 'தொண்டை கரகரப்பு', 'சிறுநீரக கல்','மூச்சு விடுவதில் சிரமம்', 'வாய் துர்நாற்றம்','சிறுநீரில் இரத்தம்','காது  கேளாமை','கூச்சம்','உலர்வான கண் /  கண் அரிப்பு','தலையில் காயம்', 'மூக்கில் அரிப்பு','மஞ்சள் காமாலை','தூங்க முடியவில்லை','வாந்தி வருவது போன்ற உணர்வு','தாமதமான பருவமடைதல்', 'மூட்டுகளில் சிதைவு','தாடை வலி','கண்ணில் நீர் வடித்தல்', 'சோர்வு / பலவீனம்','காது சீழ் வடித்தல்','காயம்','மலத்தில்  இரத்தம்','கரும்புள்ளி', 'பசியுணர்வு இல்லாமை', 'வயிற்று போக்கு','மனநிலை ஊசலாட்டம்','ஈறு பிரச்னை','வாயில் சிறு கொப்புளங்கள்',
             'எடை அதிகரிப்பு','மூக்கு ஒழுகுதல்', 'மூக்கு வலி','மூக்கடைப்பு', 'மூக்கு தடை', 'மூக்கில் கட்டி', 'கண் வலி','மலட்டுத்தன்மை  [ஆண்]','அடிக்கடி சிறுநீர் கழித்தல்', 'சிறுநீர் கழிக்கும் போது எரிச்சல்','மலச்சிக்கல்', 'தடுமாற்றம்','மூக்கு வடிவம் மாற்றம்', 'கண் சிவத்தல்','காதில் இரைச்சல்','குறைவான சிறுநீர் அளவு', 'ஒலி எழுப்பும் சுவாசம்','மூச்சிறைப்பு', 'பதற்றம்','மன அழுத்தம்','வாய்ப்புன்','சிறுநீர்ப்பையில் கல்','விட்டு விட்டு சிறுநீர் கழித்தல்',
             'சிறுநீர் கட்டுபடுத்த முடியவில்லை','குழப்பம்','வாந்தி', 'தூக்கத்தில் மூச்சுதிணறல்', 'அசெளகரியமாக உணர்தல்','மூக்கை சுற்றி வீக்கம்','சிறுநீரில் விந்துணுக்கல் நிற்கும் போது மயக்கம்']})

# Initialize the recognizer
recognizer = sr.Recognizer()

def speak_en(mytext):
    myobj = gTTS(text=mytext, lang='en', slow=False)
    date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    filename = "voice"+date_string+".mp3"
    myobj.save(filename)
    playsound.playsound(filename)
    time.sleep(0.5)
    os.remove(filename)

def speak_ta(mytext):
    myobj = gTTS(text=mytext, lang='ta', slow=False)
    date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    filename = "voice"+date_string+".mp3"
    myobj.save(filename)
    playsound.playsound(filename)
    time.sleep(0.5)
    os.remove(filename)

def Rem_Brac(s):
    if '(' in s:
        s = s[:s.index('(')]
    return s

def ip_processing_en(texts):
    if ' to ' in texts:
        texts = texts.replace(' to ','-')
    if ' or ' in texts:
        texts = texts.replace(' or ','/')
    if 'one' in texts:
        texts = texts.replace('one','1')
    if 'two' in texts:
        texts = texts.replace('two','2')
    return texts

def ip_processing_ta(texts):
    if ' முதல் ' in texts:
        texts = texts.replace(' முதல் ','-')
    if ' அல்லது ' in texts:
        texts = texts.replace(' அல்லது ','/')
    if 'ஒன்று' in texts:
        texts = texts.replace('ஒன்று','1')
    if 'இரண்டு' in texts:
        texts = texts.replace('இரண்டு','2')
    return texts

def input_text_ta(options):
    ip = audio_ip_tamil()
    print("Next Input : ",ip)
    ip = ip_processing_ta(ip)
    print("Processed Ip : ",ip)

    crt = None
    
    for opt in options:
        if Rem_Brac(opt.text) in ip:
            crt = opt.text
    print("crt_ip = ",crt)
    
    if crt == None:
        crt = input_text_ta(options)
        return crt
    else:
        return crt

def input_text_en(options):
    ip = audio_ip_english()
    print("Next Input : ",ip)

    ip = ip_processing_en(ip)
    print("Processed Ip : ",ip)
    crt = None
    for opt in options:
        if (Rem_Brac(opt.text)).upper() in ip.upper():
            crt = opt.text
    print("crt_ip = ",crt)

    if crt == None:
        crt = input_text_en(options)
        return crt
    else:
        return crt
                
# Function to record audio with noise cancellation
def record_audio_with_noise_cancellation():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 10
    FILENAME = "temp.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("Listening...")
    speak_en("Listening")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished")
    speak_en("Recording Finished , please wait")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return FILENAME

# Function to recognize Tamil speech
def recognize_english_speech(audio_file):
    try:
        audio = AudioSegment.from_wav(audio_file)
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)
        audio.export(audio_file, format="wav")

        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)

        recognized_text = recognizer.recognize_google(audio_data, language="en-IN")
        print("You said:", recognized_text)
        return recognized_text

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        speak_en("Sorry, I couldn't understand what you said.")
        return audio_ip_english()
    except sr.RequestError as e:
        print("Sorry, I encountered an error while trying to process your request:", str(e))

# Function to recognize Tamil speech
def recognize_tamil_speech(audio_file):
    try:
        audio = AudioSegment.from_wav(audio_file)
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)
        audio.export(audio_file, format="wav")

        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)

        recognized_text = recognizer.recognize_google(audio_data, language="ta-IN")
        print("You said:", recognized_text)
        return recognized_text

    except sr.UnknownValueError:
        print("மன்னிக்கவும், நீங்கள் சொன்னதை என்னால் புரிந்து கொள்ள முடியவில்லை.")
        speak_en("மன்னிக்கவும், நீங்கள் சொன்னதை என்னால் புரிந்து கொள்ள முடியவில்லை.")
        return audio_ip_tamil()
    except sr.RequestError as e:
        print("மன்னிக்கவும், உங்கள் கோரிக்கையைச் செயல்படுத்த முயற்சிக்கும்போது பிழை ஏற்பட்டது:", str(e))

def audio_ip_english():
    audio_file = record_audio_with_noise_cancellation()
    # Phrase to compare
    Speech_Input = recognize_english_speech(audio_file)
    return Speech_Input

def audio_ip_tamil():
    audio_file = record_audio_with_noise_cancellation()
    # Phrase to compare
    Speech_Input = recognize_tamil_speech(audio_file)
    return Speech_Input

def Yes_no(ip):
    if 'yes' in ip:
        return 'y'
    else:
        return 'n'

def language():
    lang_ip = audio_ip_english()
    if lang_ip.lower() == 'tamil':
        return 'ta'
    elif lang_ip.lower() == 'english':
        return 'en'
    else:
        speak_en("Cant Understand please repeat")
        speak_ta("புரியவில்லை மீண்டும் சொல்லுங்கள்")
        return language()

speak_en("Do you want the AI assistant to be in English or Tamil")
speak_ta("AI உதவியாளர் ஆங்கிலம் அல்லது தமிழில் இருக்க வேண்டுமா?")

lang = language()
# lang = 'ta'
print(lang)
if lang == 'ta':
    speak_ta("வணக்கம்")
else:
    speak_en("Greetings")
# Asking whether this is a follow up visit
if lang == 'ta':
    speak_ta("இது ஃபாலோ அப் விசிட்டா")
    speak_ta("yes or no சொல்லுங்க")
else:
    speak_en("Is this a Follow up visit")
    speak_en("Say yes or no")

visit = Yes_no(audio_ip_english())
#This Number can be Extracted from aadhar
# Phone_Number = input("Enter your Mobile Number\t: ")

if __name__ == "__main__":
    if lang == 'ta':
        speak_ta("உங்கள் அறிகுறிகளை விவரிக்கவும்")
        Speech_Input = audio_ip_tamil()
    else:
        speak_en("Describe your symptoms")
        Speech_Input = audio_ip_english()

confirmed_symptom = []
if lang == 'ta':
    for sym in data_ta["Text"]:
        if sym in Speech_Input:
            confirmed_symptom.append(sym)
else:
    for sym in data_en["Text"]:
        if sym in Speech_Input.upper():
            confirmed_symptom.append(sym.capitalize())

#List of symptoms
print("Symptoms are : ",confirmed_symptom)


#Opening Chrome Browser
driver = webdriver.Chrome(service=ChromeService(executable_path="C:\Program Files (x86)\chromedriver.exe"))

#Opening the e-sanjeevani sign-in website
driver.get("https://esanjeevani.mohfw.gov.in/#/patient/signin")
driver.maximize_window()

#Writing the phone number in the Text box
search = driver.find_element(By.CLASS_NAME,"mat-input-element")
search.send_keys("9445986532")

time.sleep(3)

#Clicking on Get OTP button
otp = driver.find_element(By.LINK_TEXT,"Get OTP")
otp.click()

time.sleep(5)

#Clicking OTP bar
search = driver.find_element(By.XPATH,'//*[@id="mat-input-2"]').click()
if lang == 'ta':
    speak_ta("உங்கள் தொலைபேசியிலிருந்து பெறப்பட்ட OTP ஐ உள்ளிடவும்")
else:
    speak_en("enter the received OTP from your phone")

time.sleep(23)

#Changing the language
if lang == 'ta':
    driver.find_element(By.CLASS_NAME,"mat-icon").click()
    time.sleep(1.5)
    driver.find_element(By.XPATH,"//span[contains(text(),'(Tamil)')]").click()
    time.sleep(3)

#Clicking Login Button
button = driver.find_element(By.CSS_SELECTOR,"button[type='submit']")
button.click()

time.sleep(5)

#Clicking Consult Now Button
consult = driver.find_element(By.CLASS_NAME,"btn")
consult.click()


time.sleep(5)

#Follow up visit 
if visit == 'y':
    driver.find_element(By.CLASS_NAME,"mat-radio-inner-circle").click()
    time.sleep(5)

#Entering into iframe
iframe = driver.find_element(By.TAG_NAME,"iframe")
driver.switch_to.frame(iframe)
driver.implicitly_wait(30)

#Ticking off the symptoms
for symptom in confirmed_symptom:
    search_bar = driver.find_element(By.CLASS_NAME,"searchText_input")
    search_bar.send_keys(symptom)
    sym = driver.find_element(By.XPATH,"//span[1][text()='%s']"%symptom)
    time.sleep(1)
    sym.click()
    time.sleep(1)
    search_bar.clear()
    time.sleep(1)

time.sleep(5)  


#Clicking Save and Next Button
btn = driver.find_element(By.CLASS_NAME,("saveBtn"))
driver.execute_script("arguments[0].click();", btn)

for i in range(5):
    driver.find_element(By.TAG_NAME,"html").send_keys(Keys.ARROW_DOWN)


time.sleep(2)

condition = True
i = 3
while condition==True:
    try:
        #Next Question
        print(driver.find_element(By.XPATH,"//*[@id='chatArea']/div[1]/div[%d]/div/p"%i).text)
        if lang == 'ta':
            speak_ta(driver.find_element(By.XPATH,"//*[@id='chatArea']/div[1]/div[%d]/div/p"%i).text)
        else:
            speak_en(driver.find_element(By.XPATH,"//*[@id='chatArea']/div[1]/div[%d]/div/p"%i).text)
        #Options
        try:
            reason = True
            #text input
            options = driver.find_elements(By.XPATH,'//*[@id="chatArea"]/div[2]/div/div/span')
            if options == []:
                #Image Input
                options = driver.find_elements(By.XPATH,"//*[@id='chatArea']/div[2]/div[1]/div/div[2]/p")
                if options == []:
                    options = driver.find_elements(By.XPATH,'//*[@id="chatArea"]/div[2]/div[2]/div/div/span')    
                    if options == []:
                        text_bar = driver.find_element(By.XPATH,'//*[@id="chatArea"]/div[2]/div[1]/div[1]/input')
                        print("Enter the number using numpad")
                        # text_bar.send_keys("102")
                        time.wait(10)
                        print("before enter")
                        text_bar.send_keys(Keys.ENTER) 
                        print("after enter")
                        reason = False                
        except:
            print("Element Not Found")
            reason = False
        finally:
            pass
        for opt in options:
            #Printing Option Can be later turned into speech
            print(opt.text)
            if lang == 'ta':
                speak_ta(opt.text)
            else:
                speak_en(opt.text)
        time.sleep(2)
        while (reason == True):
            #Enter Options Later can Be changed to voice input
            #Options need to be exact and are case sensitive
            if lang == 'ta':
                crt_ip = input_text_ta(options)
                print("crt2 = ",crt_ip)
            else:
                crt_ip = input_text_en(options)
            
            try:
                the_ele = driver.find_element(By.XPATH,'//*[@id="chatArea"]/div[2]/div[1]')
                # Get the class attribute
                class_attr = the_ele.get_attribute('class')
                # Split into list of class name
                class_names = class_attr.split(' ')
                #Clicking Text Options 
                op = driver.find_element(By.XPATH,"//span[text()='%s']"%crt_ip)
                op.click()
            except:
                #Clicking Img Options
                try:
                    driver.find_element(By.XPATH,"//p[text()='%s']"%crt_ip).click()
                except:
                    driver.find_element(By.XPATH,'//*[@id="chatArea"]/div[2]/div[2]/div/div')
            finally:
                if "multiSelectOpt" in class_names:
                    #For Multiple Selection options only if Only One options is selectable give n as input
                    if lang == 'ta':
                        speak_ta("வேறு ஏதேனும் விருப்பங்கள் தேர்ந்தெடுக்கப்பட வேண்டுமா?")
                        speak_en("Yes or No")
                    else:
                        speak_en("do you want any other options to be selected?")
                        speak_en("Say Yes or No")
                    ip1 = Yes_no(audio_ip_english())
                    if(ip1 == 'y'):
                        pass
                    else:
                        reason = False
                else:
                    reason = False
        try:
            #Clicking Save and Next Button
            btn = driver.find_element(By.CLASS_NAME,("saveBtn"))
            driver.execute_script("arguments[0].click();", btn)
        except:
            pass
        finally:
            print("\n\nNext Question")
            if lang == 'ta':
                speak_ta("அடுத்த கேள்வி, காத்திருக்கவும்")
            else:
                speak_en("Next Question, please wait")
        i += 2
        time.sleep(2)
    except:
        condition = False
        if lang == 'ta':
            print("கேள்விகள் முடிந்தது தயவு செய்து காத்திருங்கள்")
            speak_ta("AI ஆலோசனை முடிந்தது, டோக்கனை உருவாக்குகிறது")
        else:
            print("Questions Finished please wait")
            speak_en("AI consultation over, generating token")
    finally:
        pass


driver.switch_to.default_content()
driver.implicitly_wait(30)


query = driver.find_element(By.XPATH,'//*[@id="mat-input-6"]')
query.send_keys(Speech_Input)
print("\n\n\nEOP")


time.sleep(30)