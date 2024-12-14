from pydantic import BaseModel

class ChatMessage(BaseModel):
    video_path: str
    prompt: str 