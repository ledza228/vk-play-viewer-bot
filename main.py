import json
from time import sleep
import requests
import websocket
import threading
import sys
import socks

channel_name = ""
viewers_amount = 10

#urls
wss_url = "wss://pubsub.boosty.to/connection/websocket"
api_url = "https://api.vkplay.live/v1/blog/"
vkplay_url = "https://vkplay.live/"

#for wss messages
chanel_id = ""
bloger_with_id = ""


proxy_arg = None

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



def _createViewer(proxy=None):
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(wss_url,
        on_open=_on_open,
        on_message=_on_message,
        on_error=_on_error)

    if proxy is None:
        ws.run_forever()
    else:
        ip_proxy, port_proxy = proxy.split(":")
        ws.run_forever(http_proxy_host=ip_proxy, http_proxy_port=port_proxy, proxy_type=proxy_arg['type'])


def parse_proxy(file_name):
    f = open(file_name, "r")
    res = list(map(lambda x: x.replace('\n',''), f.readlines()))
    f.close()

    return res


def main():
    proxy_list = None
    if proxy_arg is not None:
        proxy_list = parse_proxy(proxy_arg['filename'])
    
    setIdParams()

    for i in range(viewers_amount):
        if proxy_list is not None:
            proxy = proxy_list[i % len(proxy_list)]
            thread = threading.Thread(target=_createViewer, args=[proxy])
        else:
            thread = threading.Thread(target=_createViewer,)

        thread.start()
        sleep(1)


def print_usage():
    print("Usage example: python3 main.py channel_name [viewers_amount] [additional_args]")
    print("additional args: ")
    print("--socks5 <filename>  using socks5 proxy from file")
    print("--http <filename>  using http/https proxy from file")



def parse_args():
    proxy_params = ["socks5", "http"]
    for i in range(len(sys.argv)):
        if sys.argv[i].startswith("--"):
            if len(sys.argv) == i + 1:
                print("incorrect proxy param!")
                print("example:")
                print("--socks5 proxy.txt")
                print("--http proxy_file.txt")
                exit(1)
            global proxy_arg
            name = sys.argv[i][2:]
            if name in proxy_params:
                proxy_arg = {'type': name, 'filename': sys.argv[i+1]}
            else:
                print("incorrect argument: " + sys.argv[i])

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Error: There is no username")
        print_usage()
        exit(0)
    channel_name = sys.argv[1]
    
    if (len(sys.argv) > 2):
        if ("--" not in sys.argv[2]):
            viewers_amount = int(sys.argv[2])

    parse_args()
    if proxy_arg:
        print("using proxy:")
        print(proxy_arg)
    else:
        print("not using proxy!")

    main()
