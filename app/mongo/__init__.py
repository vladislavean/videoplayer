from dataclasses import dataclass
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection


@dataclass
class MongoClient:
    mongo_db_client: AsyncIOMotorClient
    mongo_db_name: str
    mongo_collection_name: str

    def _get_collection(self) -> AsyncIOMotorCollection:
        return self.mongo_db_client[self.mongo_db_name][self.mongo_collection_name]

    # можно прям тут дописать async def find()/insert()/update()/delete()


db_client = MongoClient(
    mongo_db_client=AsyncIOMotorClient(
        "mongodb://localhost:27017", serverSelectTimeoutMS=5000
    ),
    mongo_db_name="test_db",
    mongo_collection_name="recordings",
)