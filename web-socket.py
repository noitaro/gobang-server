import json
from websocket_server import WebsocketServer

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

def new_client(client, server):
  logger.debug('New client {}:{} has joined.'.format(client['address'][0], client['address'][1]))
 
def client_left(client, server):
  logger.debug('Client {}:{} has left.'.format(client['address'][0], client['address'][1]))
 
def message_received(client, server, message):
  logger.debug('Message "{}" has been received from {}:{}'.format(message, client['address'][0], client['address'][1]))

  playData = json.loads(message)
  playData["x"] = playData.get("x") + 1

  reply_message = json.dumps(playData)
  server.send_message(client, reply_message)
  logger.debug('Message "{}" has been sent to {}:{}'.format(reply_message, client['address'][0], client['address'][1]))
 
# Main
if __name__ == "__main__":
  server = WebsocketServer(port=8000, host='localhost')
  server.set_fn_new_client(new_client)
  server.set_fn_client_left(client_left)
  server.set_fn_message_received(message_received)
  server.run_forever()