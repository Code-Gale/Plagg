import speech_recognition as sr
import pyttsx3
import configparser
from funcs import reminder

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        recognized_text = r.recognize_google(audio)
        return recognized_text
    except sr.UnknownValueError:
        feedback = "Sorry, I could not understand what you said."
        text_to_speech(feedback)
        print(feedback)
        return ""
    except sr.RequestError as e:
        feedback = f"Sorry, there was an error with the request: {e}"
        text_to_speech(feedback)
        print(feedback)
        return ""

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def process_command(command):
    # Check for recognized commands and perform context-aware parsing.
    if "set a reminder" in command:
        text_to_speech("Please provide the date for the reminder (e.g., '2023-12-31').")
        date = recognize_speech()
        text_to_speech("Now, please provide the time for the reminder (e.g., '16:30:00').")
        time = recognize_speech()
        text_to_speech("What is the reminder for?")
        reminder_text = recognize_speech()
        response = reminder.set_reminder(reminder_text, date, time, gender)
        text_to_speech(response)
        print(response)

    elif "view my reminders" in command:
        response = reminder.view_reminders(gender)
        text_to_speech(response)
        print(response)

    elif "clear my reminders" in command:
        response = reminder.clear_reminders(gender)
        text_to_speech(response)
        print(response)

    # Add handling for other context-aware commands as needed.

def ask_for_name():
    text_to_speech("What is your name?")
    name = recognize_speech()
    return name

def ask_for_gender():
    text_to_speech("Are you male or female?")
    gender = recognize_speech()
    return gender

def save_user_info(name, gender):
    config = configparser.ConfigParser()
    config.read('user_info.ini')
    config['User'] = {
        'Name': name,
        'Gender': gender
    }
    with open('user_info.ini', 'w') as configfile:
        config.write(configfile)

def load_user_info():
    config = configparser.ConfigParser()
    config.read('user_info.ini')
    if 'User' in config:
        name = config['User'].get('Name')
        gender = config['User'].get('Gender')
        return name, gender
    else:
        return None, None

if __name__ == "__main__":
    name, gender = load_user_info()

    if not name or not gender:
        name = ask_for_name()
        gender = ask_for_gender()
        save_user_info(name, gender)

    recognized_text = recognize_speech()
    if recognized_text:
        process_command(recognized_text)
