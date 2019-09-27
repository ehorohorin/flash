from ticket import Ticket
import qrcode
import json

t = Ticket()

data = json.dumps(t.__dict__, indent=4, sort_keys=True, default=str)


img = qrcode.make(data)
img.save("json.png", format='PNG')