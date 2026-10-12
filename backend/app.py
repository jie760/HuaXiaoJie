from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI(title="华小牛AI助手", version="1.0.0")

# 允许跨域，方便前端本地开发
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载路由模块
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    print("🚀 启动华小牛后端服务...")
    uvicorn.run(app, host="0.0.0.0", port=8000)