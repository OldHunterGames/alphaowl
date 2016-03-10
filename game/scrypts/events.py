import renpy.store as store
import renpy.exports as renpy


class Event(object):

    def __init__(self, env, location):
        self.env = env              # Enviroment. Instance of current game engive instance
        self.goto = location     # RenPy location to start an event
        self.natures = []           # "triggered", "turn_end", "faction", "personal", "special"
        self.tags = []              # tags for filtering "gay", "lolicon", "bestiality", "futanari" etc
        self.unique = False         # Unique events shown once in a game instance
        self.seen = 0               # Number of times this event seen

    def trigger(self):
        """
        On event activation
        """
        if self.check():
            self.seen += 1
            renpy.call_in_new_context(self.goto)
        return

    def check(self):
        """
        Check out of this event can be triggered in a particular situation
        :return: if True - event is available, else - is not
        """
        check = True
        if self.unique == True and self.seen > 0:
            check = False
        
        return check




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