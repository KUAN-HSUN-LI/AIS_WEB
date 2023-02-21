from functools import lru_cache
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import Settings
from server_gpu_parser import load_gpu_info_from_files
from fastapi.staticfiles import StaticFiles
from fastapi import WebSocket
import asyncio

@lru_cache()
def get_settings():
    return Settings()

class ConnectionManager:
    def __init__(self, settings: Settings):
        self.active_connections: List[WebSocket] = []
        self.gpu_data = None
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self._get_gpu_data())
        self.settings = settings

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await manager.send_personal_message(None, websocket)
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(self.gpu_data)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def _get_gpu_data(self):
        while True:
            self.gpu_data = load_gpu_info_from_files(self.settings.GPU_INFO_DIR)
            await asyncio.sleep(5)



settings = Settings()
manager = ConnectionManager(settings)
app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    while True:
        try:
            await manager.send_personal_message(None, websocket)
            await asyncio.sleep(5)
        except Exception as e:
            print(e)
            break
        
if settings.ENV == 'prod':
    app.mount("/", StaticFiles(directory="./dist", html=True))