from fastapi import FastAPI, WebSocket
from app.websockets import manager
from app.gitlab import router as gitlab_router

app = FastAPI()

# Include routers
app.include_router(gitlab_router)

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            # Handle incoming messages (e.g., trigger deployments)
            await manager.send_message({"status": "received", "message": message}, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)