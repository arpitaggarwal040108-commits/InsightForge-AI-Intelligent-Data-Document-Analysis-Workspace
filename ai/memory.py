"""
Conversation Memory
"""

class ConversationMemory:

    def __init__(self):

        self.messages = []

    def add_user(self, message):

        self.messages.append({

            "role": "user",

            "content": message

        })

    def add_ai(self, message):

        self.messages.append({

            "role": "assistant",

            "content": message

        })

    def get_history(self):

        history = ""

        for msg in self.messages:

            history += f"""

{msg["role"].upper()}:

{msg["content"]}

"""

        return history

    def clear(self):

        self.messages = []