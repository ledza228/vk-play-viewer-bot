import json
from time import sleep
import requests
import websocket
import threading
import sys

channel_name = ""
viewers_amount = 10

#urls
wss_url = "wss://pubsub.boosty.to/connection/websocket"
api_url = "https://api.vkplay.live/v1/blog/"
vkplay_url = "https://vkplay.live/"

#for wss messages
chanel_id = ""
bloger_with_id = ""


def getWebSocketJWT():
    html = requests.get(vkplay_url + channel_name).text
    token = html[html.find("eyJhbGciOiJIUzI1NiJ9"):]
    token = token[:token.find("\"")]
    return token


    
def setIdParams():
    def getUserIdFromAPI():
        res = requests.get(api_url + channel_name).json()
        return res["publicWebSocketChannel"]

    global bloger_with_id
    global chanel_id
    
    bloger_with_id = getUserIdFromAPI()
    chanel_id = bloger_with_id.split(":")[1]



def do_auth_with_wss(wss, jwt, id):
    auth = {"params":{"token":jwt,"name":"js"},"id":id}
    auth = json.dumps(auth)
    wss.send(auth)


def reg_on_chanell_with_wss(wss, id):
    reg = {"method":1,"params":{"channel":bloger_with_id},"id":id}
    reg = json.dumps(reg)
    wss.send(reg)


def reg_on_publ_stream_with_wss(wss, id):
    reg = {"method":1,"params":{"channel":"public-stream:"+chanel_id},"id":id}
    reg = json.dumps(reg)
    wss.send(reg)


def do_ping_with_wss(wss, id):
    ping_send = {"method":7,"id":id}
    ping_send = json.dumps(ping_send)
    wss.send(ping_send)

def _on_open(wss):
    print("Creating viewer!")
    do_auth_with_wss(wss, getWebSocketJWT(), 1)

    reg_on_chanell_with_wss(wss, 2)

    reg_on_publ_stream_with_wss(wss, 3)

    do_ping_with_wss(wss, 4)



def _on_message(wss, msg):
    print(msg)



def _on_error(wss, err):
    print(err)



def _createViewer():
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(wss_url,
        on_open=_on_open,
        on_message=_on_message,
        on_error=_on_error)

    ws.run_forever()



def main():
    setIdParams()

    for i in range(viewers_amount):
        thread = threading.Thread(target=_createViewer, )
        thread.start()
        sleep(1)


def print_usage():
    print("Usage example: python3 main.py channel_name [viewers_amount]")

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Error: There is no username")
        print_usage()
        exit(0)
    channel_name = sys.argv[1]
    
    if (len(sys.argv) > 2):
        viewers_amount = int(sys.argv[2])

    main()