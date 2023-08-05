import websocket

def connect_progress_ws(address):
    ws = websocket.WebSocket()
    ws.connect(address)
    return ws

def wrap_ws_progress(ws):
    prev = 0
    while ws.connected:
        try:
            current = int(ws.recv())
            yield current - prev
            prev = current
        except websocket.WebSocketConnectionClosedException:
            return

class PyntProgress():
    def __init__(self, what_to_track, total, description) -> None:
        self.running = False
        self.trackable = what_to_track
        self.total = total
        self.description = description

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.running = False


