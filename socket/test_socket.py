from app.helpers import pathing
import socketio
import json
import logging

sio = socketio.Client()

socketToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IkVFNTdDMEFBRjE5M0VFOUI2NDFBIiwicmVhZF9vbmx5Ijp0cnVlLCJwcmV2ZW50X21hc3RlciI6dHJ1ZSwidHdpdGNoX2lkIjoiNTE1NjU4MzYifQ.CZRaxsLsdZ-WkUK3mpKr8JMmzNeA5HCOGegIK2ubKSU'
socketToken_1 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IkMzMDcyQzIzMUM4RDUzRTIxOEMwRUE3RTM2MUMyRDM0Qzg2NzA2QzVEODk4MEVFMDBGRTA5MDRGQjg5OEVBNDA3OEQ0N0E0MERBRkZDMzFBMTlEQjU1QzgzN0JGMTI0NzY0N0MwMEY4MEI3REM5N0MwMjJFRUM3MEYzNzg0RUVDRDM3NzU3NzM4QzdFMTFBMkQzQzE3REJERUY4NTMxODNCMUJEQURDMzNBOTM4MUVDMkI3QkZFMDBEMUU4OUQ0NkQzNkYzREYyQkMxNkQwNkI1MUVDMTU3OTBFQjE4RUFENDQzMjIzMTdDODU1OEUzQUZCQUZCODZDRUIiLCJyZWFkX29ubHkiOnRydWUsInByZXZlbnRfbWFzdGVyIjp0cnVlLCJ0d2l0Y2hfaWQiOiI0MzY1MTY5NjMifQ.ywxopUkyXnAChonGwAbCverLg1nSgNn1s9m_YnKIHic'

logging.basicConfig(filename="timer.log",
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

prev_donation_id, prev_bits_id, prev_subs_id, prev_mysterygift_id = [None]*4
not_count = 0

class MyCustomNamespace(socketio.AsyncClientNamespace):
    async def on_connect(self):
        print("I'm connected!")

    async def on_disconnect(self):
        print("I'm disconnected!")

    async def on_event(self, data):
        print(data["type"])

    async def on_message(self, data):
        print("[echo]:", data)

class mysio:
    
    def __init__(self) -> None:
        global sio
        self.sio = socketio.AsyncClient()
        self.sio.register_namespace(MyCustomNamespace('/')) # bind


@sio.event
def connect():
    logging.info('Timer: Connection to Streamlabs socket established')
    print('Timer: Connection to Streamlabs socket established')


@sio.event
def connect_error(e):
    logging.error(e)
    print(e)


@sio.event
def disconnect():
    logging.info('Timer: Connection to Streamlabs socket was closed')
    print('Timer: Disconnected from Streamlabs socket!')



@sio.event
def event(data):
    print(data['type'])


def main_1(holder = None):
    sio.connect(f"https://sockets.streamlabs.com?token={socketToken_1}")
    sio.wait()

if __name__ == '__main__':
    import asyncio
    async def main():

        async def fun1():
            sio1 = mysio().sio
            await sio1.connect(f"https://sockets.streamlabs.com?token={socketToken_1}")
            await sio1.wait()

        async def fun2():
            sio2 = mysio().sio
            await sio2.connect(f"https://sockets.streamlabs.com?token={socketToken}")
            await sio2.wait()

        tasks = [asyncio.create_task(fun1()),asyncio.create_task(fun2()) ]
        await asyncio.wait(tasks)

    asyncio.run(main())
