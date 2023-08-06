import datetime

class Response:
    def __init__(self, response_obj):
        self._ = response_obj

    def __str__(self):
        return "<assistant> %s" % self.message

    def __len__(self):
        """ Returns the length of the text, in characters """
        return len(self.message)

    @property
    def id(self):
        return self._["id"]

    @property
    def created(self):
        return datetime.fromtimestamp(self._["created"])

    @property
    def usage(self):
        return self._["usage"]

    @property
    def model(self):
        return self._["model"]

    @property
    def choices(self):
        return self._["choices"]

    @property
    def message(self):
        """ Returns the message from the first generated choice """

        # The first generation or so typically has newlines, so
        # I'm .strip()'ing them out.
        return self.choices[0]["message"]["content"].strip()
