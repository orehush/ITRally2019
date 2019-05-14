from sanic import Sanic
from sanic.response import file

app = Sanic(__name__)


@app.route('/')
async def index(request):
    return await file('ws.html')


@app.websocket('/feed')
async def feed(request, ws):
    while True:
        data = 'hello!'
        print('Server sending: ' + data)
        await ws.send(data)
        data = await ws.recv()
        print('Server received: ' + data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)

