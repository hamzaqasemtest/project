from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.chatbot_streaming import Chatbot

router = APIRouter()


@router.get("/stream_chat/")
async def stream_chat(content: str):
    chatbot = Chatbot("")
    response = chatbot.chat_streaming(content)
    return StreamingResponse(response, media_type="text/event-stream")
