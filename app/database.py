from motor.motor_asyncio import AsyncIOMotorClient
from .core.config import get_settings

settings = get_settings()
client = AsyncIOMotorClient(settings.MONGO_URL)
db = client["mathbattle"]
