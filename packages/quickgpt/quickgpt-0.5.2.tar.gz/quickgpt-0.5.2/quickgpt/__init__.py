from quickgpt.thread import Thread

__version__ = "0.5.2"

import os

class QuickGPT:
    def __init__(self, api_key=None, retry_count=3):
        """ Main QuickGPT object

        Args:
            api_key (str): API Key provided by OpenAI
            retry_count (int, optional): In the event of an unexpected error, how many
                retries before we fail? Defaults to 3.
        """

        if not api_key:
            api_key = os.environ.get("OPENAI_API_KEY")

        self.api_key = api_key
        self.retry_count = retry_count

        self.threads = []

    def new_thread(self, model="gpt-3.5-turbo"):
        """ Creates a brand new Thread.

        Args:
            model (str):

        Returns:
            Thread: A new Thread for managing a conversation
        """

        thread = Thread(self, model=model)

        self.threads.append(thread)

        return thread

    def restore_thread(self, obj):
        """ Restores an existing Thread, using the dict format
        returned by thread.serialize().

        Args:
            obj (dict): The Thread, serialized into a dict from thread.serialize()

        Returns:
            Thread: The resulting Thread object
        """

        thread = self.new_thread()
        thread.restore(obj)

        return thread

    def run(self, *messages):
        """ Quickly generate a one-off response without
        managing a full-blown Thread.

        Returns:
            Response: The resulting Response object from OpenAI
        """

        thread = self.new_thread()

        return thread.run(*messages)
