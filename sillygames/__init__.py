import sillygames
import speech_recognition as sr
import logging

logger = logging.getLogger()

def setAudioSourceAndRecognizer(source, recognizer):
    global audioSource, audioRecognizer
    audioSource = source
    audioRecognizer = recognizer

def recognize(func=None):
    audio = audioRecognizer.listen(audioSource)
    try:
        if func is not None:
            func()
        logger.debug("recognizing...")
        recognized = audioRecognizer.recognize_google(audio)
        logger.debug("recognized: " + recognized)
        return recognized

    except sr.UnknownValueError:
        logger.error("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        logger.error("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None