import asyncio
import websockets
import json
import ssl

class JsonRpcClient:
    def __init__(self, uri):
        self.uri = uri
        self.request_id = 0
        self.ssl_context = ssl.create_default_context()

    async def call(self, method, params):
        async with websockets.connect(self.uri, ssl=self.ssl_context) as ws:
            self.request_id += 1

            request = {
                "jsonrpc": "2.0",
                "method": method,
                "params": params,
                "id": self.request_id
            }

            await ws.send(json.dumps(request))
            response = json.loads(await ws.recv())

            if "error" in response:
                raise Exception(response["error"])

            return response["result"]

async def main():
    client = JsonRpcClient("wss://localhost:8765")
    result = await client.call("add", [10, 5])
    print("Result:", result)

asyncio.run(main())
