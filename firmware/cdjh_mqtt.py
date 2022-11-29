import gc
import json
import time

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio


from mqtt_as import MQTTClient, config

gc.collect()


SERVER = "a26wt0x5359obq-ats.iot.eu-west-1.amazonaws.com"

state = {"state": {"reported": { "animation": "fire"}}}

class CDJHVlamtMQTTClient:
    
    def __init__(self, thingName, wifi_ssid, wifi_pass, animationMgr):
        self.thingName = thingName
        self.shadowTopicPrefix = '$aws/things/' + thingName + '/shadow'
        self.wifi_ssid = wifi_ssid
        self.wifi_pass = wifi_pass
        self.animationMgr = animationMgr

         
    def getConfig(self):
        with open('private.key') as f:
            key_data = f.read()
        with open('cert.pem') as f:
            cert_data = f.read()
#         with open('aws-root-ca.pem') as f:
#             rootca = f.read()
        config['subs_cb'] = self.callback
        config['connect_coro'] = self.conn_han
        config['server'] = SERVER
        config['client_id'] = self.thingName
        config['ssl'] = True
        config['ssl_params']=  {"cert": cert_data, "key": key_data, "server_side": False}
        config['ssid'] = self.wifi_ssid
        config['wifi_pw'] = self.wifi_pass
        return config
        
    def callback(self, topic, msg, retained):
        print((topic, msg, retained))
        if (topic.decode('utf8').endswith('update/accepted')):
            #decode msg (comes in as a bytearray)
            decoded_msg = msg.decode('utf8')
            msg_as_json = json.loads(decoded_msg)
            s = json.dumps(msg_as_json)
            print(s)
            animation_name = msg_as_json["state"]["reported"]["animation"]
            print("new animation should be " + animation_name)
            self.animationMgr.stop_annimation_and_run_new_one(animation_name)

    async def conn_han(self, client):
        await client.subscribe(self.shadowTopicPrefix + '/#' , 1)

    async def _run(self, client):
        await client.connect()
        # publish our initial state, running the fire animation
        await client.publish(self.shadowTopicPrefix + '/update', json.dumps(state), qos = 1)
        
        while True:
            #just keep the mqtt connection running and listen for incoming messages
            await asyncio.sleep(5)
            gc.collect()
            
    def run(self):
        MQTTClient.DEBUG = True  # Optional: print diagnostic messages
        client = MQTTClient(self.getConfig())
        try:
            asyncio.run(self._run(client))
        finally:
            client.close()  # Prevent LmacRxBlk:1 errors
        
    



