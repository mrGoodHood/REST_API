from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

from app.db_manager import DatabaseManager

# Инициализируем экземпляр FastAPI
app = FastAPI()

# Инициализируем экземпляр DatabaseManager
db_manager = DatabaseManager()
db_manager.connect()

# Схема для валидации данных пользователя
class User(BaseModel):
    email: str = Field(..., example="example@example.com")
    fam: str = Field(None, example="Иванов")
    name: str = Field(None, example="Иван")
    otc: str = Field(None, example="Иванович")
    phone: str = Field(None, example="+7 123 456 7890")

# Схема для валидации координат
class Coords(BaseModel):
    latitude: float = Field(..., example=45.3842)
    longitude: float = Field(..., example=7.1525)
    height: int = Field(..., example=1200)

# Схема для валидации уровня сложности
class Level(BaseModel):
    winter: str = Field("", example="")
    summer: str = Field("1А", example="1А")
    autumn: str = Field("1А", example="1А")
    spring: str = Field("", example="")

# Схема для валидации изображений
class Image(BaseModel):
    data: str = Field(..., example="<base64_encoded_image>")
    title: str = Field(..., example="Седловина")

# Основная схема для валидации данных о перевале
class PerevalAdded(BaseModel):
    beauty_title: str = Field("", example="Пер. ")
    title: str = Field(..., example="Пхия")
    other_titles: str = Field("", example="Триев")
    connect: str = Field("", example="")
    add_time: datetime = Field(datetime.now(), example="2021-09-22T13:18:13")
    user: User
    coords: Coords
    level: Level
    images: List[Image]

# Метод POST /submitData
@app.post("/submitData", status_code=status.HTTP_201_CREATED)
async def submit_data(request: Request, pereval_added: PerevalAdded):
    try:
        # Извлекаем данные из запроса
        user_data = pereval_added.user.dict()
        coords_data = pereval_added.coords.dict()
        level_data = pereval_added.level.dict()
        images_data = pereval_added.images

        # Вставляем пользователя в базу данных
        user_id = db_manager.insert_user(**user_data)

        # Вставляем координаты в базу данных
        coord_id = db_manager.insert_coords(**coords_data)

        # Вставляем данные о перевале в базу данных
        pereval_id = db_manager.insert_pereval_added(
            beauty_title=pereval_added.beauty_title,
            title=pereval_added.title,
            other_titles=pereval_added.other_titles,
            connect=pereval_added.connect,
            add_time=pereval_added.add_time,
            user_id=user_id,
            coord_id=coord_id,
            winter_level=level_data["winter"],
            summer_level=level_data["summer"],
            autumn_level=level_data["autumn"],
            spring_level=level_data["spring"]
        )

        # Вставляем изображения в базу данных
        for image in images_data:
            db_manager.insert_image(pereval_id, image.data, image.title)

        return JSONResponse(content={
            "status": status.HTTP_201_CREATED,
            "message": "Данные успешно сохранены.",
            "id": pereval_id
        })

    except Exception as e:
        return JSONResponse(content={
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e),
            "id": None
        })

# Завершаем соединение с базой данных при завершении работы приложения
@app.on_event("shutdown")
def shutdown_event():
    db_manager.close_connection()