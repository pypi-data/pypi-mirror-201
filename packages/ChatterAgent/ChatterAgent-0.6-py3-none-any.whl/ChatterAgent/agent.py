import openai

class ChatAgent:
    api_key = None

    def __init__(self, **kwargs):
        self.model = kwargs.get('model', 'gpt-3.5-turbo')
        self.start_msg = kwargs.get('start_msg', '')
        ChatAgent.api_key = kwargs.get('api_key', ChatAgent.api_key)
        
        openai.api_key = ChatAgent.api_key

        self.messages = []
        if(self.start_msg):
            self.messages.append({'role':'system', 'content':self.start_msg})
        
    def add_msg(self, role, msg):
        self.messages.append({'role':role, 'content':msg})
    
    def prompt(self, msg):
        new_message = {'role':'user', 'content':msg}
        self.messages.append(new_message)

        response = openai.ChatCompletion.create(model=self.model, messages=self.messages)['choices'][0]['message']['content']
        self.messages.append({'role':'assistant', 'content': response})

        return response