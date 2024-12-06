from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.routes import router as v1_router

# Инициализация приложения
app = FastAPI(title="REST API для регистрации горных перевалов")

# Регистрация маршрутов
app.include_router(v1_router, prefix="/api/v1")

# Настройка CORS (Cross-Origin Resource Sharing)
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)