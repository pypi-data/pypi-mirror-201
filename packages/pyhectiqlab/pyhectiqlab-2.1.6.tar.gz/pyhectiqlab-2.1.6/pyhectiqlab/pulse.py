from collections import defaultdict
from pyhectiqlab.timer import RepeatedTimer
from pyhectiqlab.events_manager import EventsManager
from pyhectiqlab.decorators import silent_method_if_dry

import logging
logger = logging.getLogger('pyhectiqlab')

class PulseManager():

    def __init__(self, run_path: str, project: str, heart_rate: int = 5, mock: bool = False):
        self.dry_mode = mock
        self.messages = defaultdict(str)
        self.run_path = run_path
        self.project = project
        self.events_manager = EventsManager()
        self.timer = RepeatedTimer(self.send_beat, heart_rate)
        self.timer.start()
        return
    
    def start(self):
        if self.timer.stopped():
            self.timer.start()

    def stop(self):
        self.timer.stop()

    def __getitem__(self, key: str):
        return self.messages[key]

    @silent_method_if_dry
    def ack(self, key: str):
        self.events_manager.add_event("ack_pulse", (self.run_path, self.project, key), async_method=True)
        self.messages.pop(key)
        
    def __delete__(self):
        if self.dry_mode==False:
            self.timer.stop()

    @silent_method_if_dry
    def send_beat(self):
        keys = list(self.messages.keys())
        new_messages = self.events_manager.add_event("pulse", (self.run_path, self.project, keys), async_method=False)
        new_messages.pop("status_code")
        for key, item in new_messages.items():
            self.messages[key] = item