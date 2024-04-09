import speech_recognition as sr
import pyttsx3

#initialize recognizer
r = sr.Recognizer()

def record_text():
    #loop in case of errors
    while(1):
        try:
            #use microphone as input source
            with sr.Microphone() as source2:
                #prepare recognizer to receive input
                r.adjust_for_ambient_noise(source2, duration=0.2)
                
                #listen for user input
                audio2 = r.listen(source2)
                
                #using google to recognize audio
                MyText = r.recognize_whisper(audio2)
    
                return MyText 
    
    
        except sr.RequestError as e:
            print("could not request results ; {e}".format(e))
            
        except sr.UnknownValueError:
            print("unknown error occured")
    
    return

def output_text(text):
    f = open("output.txt", "a")
    f.write(text)
    f.write("\n")
    f.close()
    return

while(1):
    text = record_text()
    output_text(text)
    
    print("wrote text")