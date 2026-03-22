import asyncio
import websockets
import json
import ssl

async def add(params):
    return params[0] + params[1]

async def subtract(params):
    return params[0] - params[1]

methods = {"add": add, "subtract": subtract}

async def handle_rpc(websocket):
    async for message in websocket:
        request = json.loads(message)

        response = {"jsonrpc": "2.0", "id": request.get("id")}

        try:
            method = request.get("method")
            params = request.get("params", [])

            if method in methods:
                result = await methods[method](params)
                response["result"] = result
            else:
                response["error"] = {"code": -32601, "message": "Method not found"}

        except Exception as e:
            response["error"] = {"code": -32603, "message": str(e)}

        await websocket.send(json.dumps(response))

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain("cert.pem", "key.pem")

start_server = websockets.serve(handle_rpc, "localhost", 8765, ssl=ssl_context)

print("Server running on wss://localhost:8765")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
