# API 路由层
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from services.yolo_service import YOLOService
from services.llm_service import LLMService

router = APIRouter()
yolo_service = YOLOService()
llm_service = LLMService()

class ChatRequest(BaseModel):
    query: str
    image: str = None

@router.post("/api/detect")
async def detect_image(file: UploadFile = File(...)):
    """接口：接收图片并调用视觉服务"""
    contents = await file.read()
    return yolo_service.detect(contents)

@router.post("/api/chat")
async def chat(request: ChatRequest):
    """接口：接收文本和图片并调用大模型服务"""
    try:
        answer = llm_service.chat(request.query, request.image)
        return {"answer": answer}
    except Exception as e:
        print(f"LLM服务出错: {e}")
        return {"answer": f"系统内部错误: {str(e)}"}