# -*- coding:utf-8 -*-
# @Author :songtao

# -*- coding:utf-8 -*-
# @Author :songtao

import websocket
import json
import redis

url ='wss://www.bitmex.com/realtime?subscribe=instrument,orderBook:XBTUSD'
redis_options = {
    'host':'127.0.0.1',
    'port':6379,
    'socket_timeout':3
}

class RedisStore(object):
    def __init__(self):
        self._tick_cli = redis.StrictRedis(**redis_options)
        self._tick_ps = self._tick_cli.pubsub()
        pass

    def set(self, k, v):
        self._tick_cli.set(k, v)

    def get(self, k):
        return self._tick_cli.get(k)
        pass

    def publish(self, channel, msg):
        self._tick_ps.publish(channel, msg)
        pass

    def subscribe(self,channels):
        self._tick_ps.subscribe(channels)
        pass

    def expire(self, k, ttl):
        self._tick_cli.expire(k, ttl)
        pass

def on_open(self):
    #asubscribe okcoin.com spot ticker
    print('running on_open....')
    #self.send("{'event':'addChannel','channel':'ok_sub_futureusd_btc_kline_this_week_1min'}")

def on_message(self,evt):

    evt = json.loads(evt)
    flag = evt.get('action', None)
    if flag != 'update':
        return

    datas = evt.get('data', None)
    if datas == None:
        return
    data = datas[0]
    if data['symbol'] != 'XBTUSD':
        return    
    price = data.get('lastPrice',None)
    if not price:
        return
    data = json.dumps(data)
    print(type(data),data)
    redis = RedisStore()
    key = f'bitmex/tick/xbtusd'
    redis.set(key, data)

def on_error(self, evt):
    print('running on_error....')

    websocket.enableTrace(False)
    host = url
    ws = websocket.WebSocketApp(host,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(ping_interval=30, ping_timeout=15)

def on_close(self,evt):
    print ('DISCONNECT')

if __name__ == "__main__":
    websocket.enableTrace(False)
    host = url
    ws = websocket.WebSocketApp(host,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever(ping_interval=30,ping_timeout=15)

