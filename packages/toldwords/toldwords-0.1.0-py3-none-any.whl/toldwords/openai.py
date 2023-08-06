''' OpenAI API Connect '''
from typing import List
from requests import Session
from pydantic import BaseModel


class Message(BaseModel):
    ''' Message in chat format '''
    role: str
    content: str


class OpenAIAPI(Session):
    ''' OpenAI API '''

    def __init__(self, token: str, organization: str | None) -> None:
        super().__init__()
        self.url = 'https://api.openai.com/v1'
        self.headers['Authorization'] = f'Bearer {token}'

        if organization:
            self.headers['OpenAI-Organization'] = organization

    def chat_completions(self,
                         messages: List[Message],
                         model='gpt-3.5-turbo',
                         temperature=1,
                         n=1,
                         user='api'):
        ''' chat completions '''
        data = {
            'model': model,
            'messages': [msg.dict() for msg in messages],
            'temperature': temperature,
            'n': n,
            'user': user,
        }
        return self.post(self.url + '/chat/completions', json=data).json()
