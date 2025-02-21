from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from prometheus_fastapi_instrumentator import Instrumentator
from app.websockets import manager
from app.gitlab import router as gitlab_router
from app.kubernetes import inject_code_into_pod
import json

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

# Instrument the app with Prometheus
Instrumentator().instrument(app).expose(app)