''' Fetch data from pretalx '''
from typing import List
from requests import Session
from pydantic import BaseModel


class Item(BaseModel):
    ''' Item '''
    code: str
    title: str
    track_id: int
    state: str
    abstract: str


class PretalxResponse(BaseModel):
    ''' PretalxResponse '''
    count: int
    next: str | None
    previous: str | None
    results: List[Item]


class Pretalx(Session):
    ''' Pretalx '''

    def __init__(self, domain: str, project: str, resource: str) -> None:
        super().__init__()
        self.url = f'https://{domain}/api/events/{project}/{resource}/'

    def fetch(self) -> PretalxResponse:
        ''' Fetch data '''
        return PretalxResponse.parse_obj(self.get(url=self.url, params={'limit': 1000}).json())
