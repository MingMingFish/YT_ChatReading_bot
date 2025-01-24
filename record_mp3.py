import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty("voices")[0] 
engine.setProperty('voice', voices)
text = input('Input Your Text: ')
engine.save_to_file(text, 'text.mp3')
engine.runAndWait()