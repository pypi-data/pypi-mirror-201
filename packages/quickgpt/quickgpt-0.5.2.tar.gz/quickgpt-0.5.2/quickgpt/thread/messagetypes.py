class Message:
    def __init__(self, content, sticky=False):
        self.content = content
        self.sticky = sticky

    @property
    def role(self):
        return self.__class__.__name__.lower()

    @property
    def obj(self):
        return {
            "role": self.role,
            "content": self.content
        }

    def __str__(self):
        return "<%s> %s" % (self.role, self.content)

    def __len__(self):
        """ Returns the length of the content, in characters """
        return len(self.content)

class System(Message): pass
class User(Message): pass
class Assistant(Message): pass
