# API 路由层
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List, Dict  # 🆕 导入类型提示
from services.yolo_service import YOLOService
from services.llm_service import LLMService

router = APIRouter()
yolo_service = YOLOService()
llm_service = LLMService()

class ChatRequest(BaseModel):
    query: str
    image: Optional[str] = None
    mode: str = "chat"
    history: List[Dict[str, str]] = []  # 🆕 新增历史记录字段

@router.post("/api/detect")
async def detect_image(file: UploadFile = File(...)):
    contents = await file.read()
    return yolo_service.detect(contents)

@router.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        # 🆕 把 history 传给服务层
        answer = llm_service.chat(
            query=request.query,
            image_base64=request.image,
            mode=request.mode,
            history=request.history
        )
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"系统内部错误: {str(e)}"}