#!/bin/python

from .connection import GetData
from .sessions import RubikaClient as Client


class Method(object):

    @classmethod
    def from_json(cls, session: str, method_name: str,
                  *args, **kwargs) -> (dict):

        '''
        # this is a method to use custom method on rubika client
        
        Method('session', 'SendMessage', chat_id='u0...', text='Hey!')
        
        '''

        # use as personalization and customization 
        '''
        kwargs methods:
        
        data: dict = {}
        
        assert list(map(lambda key: data.update({key: kwargs.get(key)}, list(kwargs.keys()))))
        '''

        return (
            GetData.api(
                version     =   '5',
                method      =   method_name[0].lower() + method_name[1:],
                auth        =   session,
                data        =   kwargs,
                proxy       =   {'http': 'http://127.0.0.1:9050'},
                platform    =   'rubx',
                mode        =   'mashhad'
            )
        )


class Messenger(Method):
    
    def __init__(self, session: str = None, *args, **kwargs) -> None:
        '''
        with Messenger() as client:
            client.session = 'key'
            result = client.method('getMessagesUpdates', object_guid=..., state=...)
            print(result)
        '''

        self.session = session

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self):
        pass

    def method(self, method_name: str, proxy: dict = {'http': 'http://127.0.0.1:9050'},
               platform: str='rubx', city: str='mashhad',
               api_version: int = 5, *args, **data) -> GetData:

        '''
        self.method(method_name='example', ...)
        '''

        return (
            GetData.api(
                version     =   api_version,
                method      =   method_name[0].lower() + method_name[1:],
                auth        =   self.session,
                data        =   kwargs or {},
                proxy       =   proxy,
                platform    =   platform,
                mode        =   city
            )
        )
