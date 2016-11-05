import sillygames
import speech_recognition as sr
import logging
import asyncio

logger = logging.getLogger()

class SpeechCommandsChannel():
    
    def __init__(self, commandWord):
        self.stop_listening = None
        self.commandWord = commandWord.lower()
        self.queue = asyncio.PriorityQueue()

    def start(self):
        r = sr.Recognizer()
        m = sr.Microphone()
        with m as source:
            r.adjust_for_ambient_noise(source)

        self.stop_listening = r.listen_in_background(m, lambda recognizer, audio: self.callback(recognizer, audio))
    
    def stop(self):
        if callable(self.stop_listening):
            self.stop_listening()
            self.stop_listening = None
            
    async def get(self):
        res = await self.queue.get()

        self.queue.task_done()

        return res

    def get_nowait(self):
        if self.queue.empty():
            return None

        res = self.queue.get_nowait()
        self.queue.task_done()
        
        return res
        
    def callback(self, recognizer, audio):
        try:
            logger.debug("recognizing...")
            recognized = recognizer.recognize_google(audio)
            logger.debug("recognized: " + recognized)
            
            if self.commandWord in recognized.lower():
                logger.debug("Action command recognized")
                command = recognized[len(self.commandWord):].strip().lower()
                
                self.queue.put_nowait(command)        
            else:
                # await robot.say_text("You did not say the magic word " + command_activate).wait_for_completed()
                logger.debug("No magic word")


        except sr.UnknownValueError:
            logger.error("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error("Could not request results from Google Speech Recognition service; {0}".format(e))
            return None
        