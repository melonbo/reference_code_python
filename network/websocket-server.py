import asyncio
import websockets

# 定义WebSocket连接处理函数
async def handle_connection(websocket, path):
    # 接收WebSocket客户端发送的消息
    async for message in websocket:
        print(f"Received message: {message}")
        # 发送消息到WebSocket客户端
        await websocket.send(f"Received message: {message}")

# 启动WebSocket服务器
start_server = websockets.serve(handle_connection, "localhost", 8080)

# 运行事件循环
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
