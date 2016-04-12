import renpy.store as store
import renpy.exports as renpy
from copy import copy

events_list = []

def register_event(location, *args, **kwargs):
    event = Event( location, location)
    for key in kwargs.keys():
        if key == 'tags':
            event.tags = kwargs['tags']
        if key == 'unique':
            event.unique = kwargs['unique']
    events_list.append(event)

def get_event(name):
    for event in events_list:
        if event.name == name:
            return event
class Event(object):

    def __init__(self, name, location):
        self.name = name
        self.goto = location     # RenPy location to start an event
        self.tags = []              # tags for filtering "gay", "lolicon", "bestiality", "futanari" etc
        self.unique = False         # Unique events shown once in a game instance
        self.seen = 0               # Number of times this event seen

    def trigger(self, target=None):
        """
        On event activation
        """
        if self.seen > 0 and self.unique:
            return False
        result = renpy.call_in_new_context(self.goto, target)
        if result:
            self.seen += 1
        return result






class EVUnique(Event):
    """
    Unique event for test
    """

    def __init__(self, env, location):
        super(EVUnique, self).__init__(env, location)
        self.natures = ["triggered", "turn_end", "faction"]
        self.unique = True


class EVGeneric(Event):
    """
    Generic event for test
    """

    def __init__(self, env, location):
        super(EVGeneric, self).__init__(env, location)
        self.natures = ["triggered", "turn_end", "faction"]