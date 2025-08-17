import asyncio
from pymongo import AsyncMongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# 全域變數
client = None
db = None
movies = None

async def connect():
    """建立非同步連接並處理錯誤"""
    global client, db, movies
    try:
        client = AsyncMongoClient('mongodb://root:password@localhost:27017/', 
                                serverSelectionTimeoutMS=5000)
        # 測試連接
        await client.admin.command('ping')
        print("成功連接到 MongoDB")
        
        db = client['test']
        movies = db['movies']
        return True
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"無法連接到 MongoDB: {e}")
        return False

async def insert_demo():
    """非同步插入示範"""
    # insert
    new_profile = {'user_id': 213, 'name': 'Alan'}
    result = await movies.insert_one(new_profile)
    print(f"插入文檔 ID: {result.inserted_id}")
    
    # read
    print("\n所有文檔:")
    async for movie in movies.find():
        print(movie)

async def update_demo():
    """非同步更新示範"""
    result = await movies.update_one({'user_id': 213}, {'$set': {'user_id': 30}})
    print(f"更新了 {result.modified_count} 個文檔")
    
    # read
    print("\n更新後的文檔:")
    async for movie in movies.find():
        print(movie)

async def cleanup():
    """清理測試資料"""
    result = await movies.delete_many({'user_id': {'$in': [213, 30]}})
    print(f"\n清理了 {result.deleted_count} 個文檔")

async def main():
    """主程式"""
    # 建立連接
    if not await connect():
        return
    
    try:
        await insert_demo()
        # await update_demo()
        # await cleanup()  # 取消註解以清理測試資料
    finally:
        if client:
            await client.close()
            print("\n已關閉連接")

if __name__ == "__main__":
    # 執行非同步主程式
    asyncio.run(main())