from app.helpers import pathing
import socketio
import json
import logging

sio = socketio.Client()

socketToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IkVFNTdDMEFBRjE5M0VFOUI2NDFBIiwicmVhZF9vbmx5Ijp0cnVlLCJwcmV2ZW50X21hc3RlciI6dHJ1ZSwidHdpdGNoX2lkIjoiNTE1NjU4MzYifQ.CZRaxsLsdZ-WkUK3mpKr8JMmzNeA5HCOGegIK2ubKSU'
socketToken_1 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6Ijc4MDA5NzVFMkEyQ0NDOTVBODJGQTZDNDFGMEU2OTRBOTkzRUZDQzM4OEM0NjRGNjUyNjhFRTVGM0M5Rjg2NjhFNTYxOTM4NEMwOTE4MEVCREQ4RTBDQkM4OTU5NjdFOURCMzA3MTc2MzY1NEFCMzVEQUI3QkUwNkIzOTdFOEJCNTU5RTQ2NjE2NTEwNEQ0RTcwNEEwQTg5Q0REQjA2RUNDMDg2NzgwQ0VEQ0JBMTkxODk3REFGNjY2NUNCRDY4Q0Q0QURERjI3NkMxQ0YyMzk3NTcyRTNCMDYzNDU3QzUyQTM4NDg4MzkzMUMxNjA3MzNCRDUzRkYzQzgiLCJyZWFkX29ubHkiOnRydWUsInByZXZlbnRfbWFzdGVyIjp0cnVlLCJ0d2l0Y2hfaWQiOiI0MzY1MTY5NjMifQ.icq3w4MRXwIGVHCr-r7yAuV6Xz5nuI9UzFY-0hindsI'

logging.basicConfig(filename="timer.log",
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

prev_donation_id, prev_bits_id, prev_subs_id, prev_mysterygift_id = [None]*4
not_count = 0

class Mysio(socketio.Client):
    @sio.event
    def connected(self):
        logging.info('Timer: Connection to Streamlabs socket established')
        print('Timer: Connection to Streamlabs socket established')


    @sio.event
    def connect_error(self, e):
        logging.error(e)
        print(e)


    @sio.event
    def disconnect(self):
        logging.info('Timer: Connection to Streamlabs socket was closed')
        print('Timer: Disconnected from Streamlabs socket!')

    @staticmethod
    def lower_equal(a: str, b: str):
        return a.lower() == b.lower()

    @staticmethod
    def payload(self, data):
        data = data['message'][0]
        try:
            return data['payload'] if 'payload' in data.keys() else data
        except AttributeError:
            print('exception')
            return data

    @staticmethod
    def add_time(self, _type: str, amount: int, base_amount: int = 1, sub_plan: int = None):
        with open(pathing('json', 'subathon_timer.json'), "r", encoding='utf-8') as dt:
            timer = json.load(dt)
        if not sub_plan or not _type in ['subs', 'submysterygift']:
            multiplier = timer[_type]['multiplier']
        elif _type in ['subs', 'submysterygift']:
            multiplier = timer[_type][str(sub_plan)[0]]
        timer['deadline'] += round(float(amount/base_amount)*multiplier)
        with open(pathing('json', 'subathon_timer.json'), "w", encoding='utf-8') as dt:
            json.dump(timer, dt, indent=4)
        output = f'Added {round(float(amount/base_amount)*multiplier)}s from {amount} of {_type+str(sub_plan) if sub_plan else _type}'
        logging.info(f'Timer: {output}')
        print(f'Timer: {output}')
        return 0


    @sio.event
    def event(self, data):
        global prev_donation_id, prev_bits_id, prev_subs_id, prev_mysterygift_id
        global not_count
        print(data['type'])


def main_1(holder = None):
    sio = Mysio()
    sio.connect(f"https://sockets.streamlabs.com?token={socketToken_1}")
    sio.wait()

if __name__ == '__main__':
    main_1()
