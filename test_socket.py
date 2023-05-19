import json
import logging
from urllib.parse import urlencode

import eventlet
import socketio
from forbiddenfruit import curse

from app.client import db_client
from app.credentials import (DB_NAME, STREAMLABS_SOCKET_BASE_URL,
                             STREAMLABS_SOCKET_TOKENS_COLLECTION,
                             SUBATHON_COLLECTION)


def lower_equal(a: str, b: str) -> bool:
    return a.lower() == b.lower()

class SocketIOClient:
    def __init__(self, user_id, socket_token):
        self.sio = socketio.Client()
        self.id = user_id
        self.url = f'{STREAMLABS_SOCKET_BASE_URL}/?{urlencode({"token": socket_token})}'
        
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('message', self.on_message)
        self.sio.on('event', self.on_event)
        # self.start()

    def start(self):
        self.sio.connect(self.url)
        
    def stop(self):
        self.sio.disconnect()

    def on_connect(self):
        # print(f'Connected to {self.url}')
        pass

    def on_disconnect(self):
        print(f'Disconnected from {self.url}')

    def on_message(self, message):
        print(f'Received message on {self.url}: {message}')
    
    @staticmethod
    def payload(data: dict) -> dict:
        data = data['message'][0]
        try:
            return data['payload'] if 'payload' in data.keys() else data
        except AttributeError:
            print('exception')
            return data
    
    @staticmethod
    def add_time(timer: dict, _type: str, amount: int, base_amount: int = 1, sub_plan: int = None):
        if not sub_plan or not _type in ['subs', 'submysterygift']:
            multiplier = timer[_type]['multiplier']
        elif _type in ['subs', 'submysterygift']:
            multiplier = timer[_type][str(sub_plan)[0]]
        precision = 1000 if timer['precision'] @ 'ms' else 1
        timer['deadline'] += round(float(amount/base_amount)*multiplier) * precision
        
        
        output = f'Added {round(float(amount/base_amount)*multiplier)}s from {amount} of {_type+str(sub_plan) if sub_plan else _type}'
        logging.info(f'Timer: {output}')
        print(f'Timer: {output}')
        return timer.get('deadline')

    def on_event(self, event):
        subathon_data = subathon_collection.find_one({'user_id': self.id})
        print(subathon_data)
        for_user = event.get('for')
        event_type = event.get('type')
        if event_type @ 'donation' and subathon_data.get('donation'):
            donation = self.payload(event)
            #TODO: check event id to see if it's already been added
            new_deadline = self.add_time(subathon_data, 'donation', donation['amount'])
            print(new_deadline)
            subathon_collection.update_one({'user_id': self.id}, {'$set': {'deadline': new_deadline}})
        if for_user @ "twitch_account":
            if event_type == 'subscription':
                #TODO: add time from subscription
                pass
            elif event_type == 'resub':
                #TODO: add time from resubscription
                pass
            elif event_type == 'submysterygift':
                #TODO: add time from submysterygift
                pass
            elif event_type == 'bits':
                #TODO: add time from bits
                pass
        print(f'Received event from {self.id}: {event}')
    
    def __del__(self, self_destruct=True):
        if not self_destruct:
            print(f'Stopped {self.id}')
            self.stop()

clients = {}

class SocketIOServer:
    

    def __init__(self, ws_server_urls):
        self.ws_server_urls = ws_server_urls
        # self.server = socketio.Server()
        self.connect_clients()
        # self.server.on('connect', self.on_connect)
        # self.server.on('event', self.on_message)
        # self.server.on_namespace(socketio.Namespace('/test'))

    def on_connect(self, sid, environ, auth):
        print(f'Connected to server from {sid}')
        
    def on_message(self, sid, message):
        print('Received message', sid, message)
        
    def connect_client(self, user_id, socket_token):
        client = SocketIOClient(user_id, socket_token)
        client.start()
        clients[user_id] = client
    
    def connect_clients(self):
        for user_id, socket_token in self.ws_server_urls.items():
            self.connect_client(user_id, socket_token)
    
    def disconnect_client(self, user_id):
        clients[user_id].stop()
        del clients[user_id]

    def run(self, app):
        app = socketio.WSGIApp(self.server, app)
        # eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
        return app
    


if __name__ == '__main__':
    db = db_client[DB_NAME]
    socket_tokens_collection = db[STREAMLABS_SOCKET_TOKENS_COLLECTION]
    subathon_collection = db[SUBATHON_COLLECTION]

    # Cur531ng th3 5tr1ng cl455
    curse(str, '__matmul__', lower_equal)

    # logging.basicConfig(level=logging.INFO)

    # watch for changes in the socket tokens collection
    ws_server_urls = {}
    for token in socket_tokens_collection.find():
        user_id = token['user_id']
        ws_server_urls[user_id] = token['socket_token']
    # print(ws_server_urls)

    # from main import app
    # app.secret_key = "my_secret_key_Br41N_F@c3"
    server = SocketIOServer(ws_server_urls)
    # app = server.run(app)
    # eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

    # now watch for changes

    with socket_tokens_collection.watch() as stream:
        for change in stream:
            print(change)
            if change['operationType'] == 'insert':
                user_id = change['fullDocument']['user_id']
                socket_token = change['fullDocument']['socket_token']
                ws_server_urls[user_id] = socket_token
                server.ws_server_urls = ws_server_urls
                server.connect_client(user_id, socket_token)
                print("insert")
                
            if change['operationType'] == 'update' and (socket_token := change['updateDescription']['updatedFields'].get('socket_token')):
                user_id = change['documentKey']['_id']
                server.disconnect_client(user_id)
                ws_server_urls[user_id] = socket_token
                server.ws_server_urls = ws_server_urls
                server.connect_client(user_id, socket_token)
                print("update")
                
            if change['operationType'] == 'delete':
                user_id = change['documentKey']['_id']
                del ws_server_urls[user_id]
                client = clients[user_id]
                client.__del__(self_destruct=False)
                del client
                del clients[user_id]
                print("delete")
            print(ws_server_urls)
            print(clients)