# import sched, time
# resubber = sched.scheduler(time.time, time.sleep)
# def resubscribe(sc): 
#     print("Resubscribe")
#     # do your stuff
#     print(sc)
#     resubber.enter(1, 1, resubscribe, (sc,))
# resubber.enter(1, 1, resubscribe, ("asda",))
# resubber.run()


import threading
import socket
from api import subscribe_to_messages

OPAQUE = 0
def resub(sock, token):
    msg = subscribe_to_messages(token, OPAQUE)
    print(msg)
    sock.sendall(bytes(msg, 'utf-8'))
    t = threading.Timer(1, resub, [sock, token])
    t.start()

token = "e18fd2e9cfa91559a9658bfe31e95160da755368f8e281b52945c6be48f3fdd7"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("api.seraphim.online", 20013))




t = threading.Timer(1, resub, [sock, token])
t.start()