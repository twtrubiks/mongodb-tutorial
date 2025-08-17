from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# 建立連接並處理錯誤
try:
    client = MongoClient('mongodb://root:password@localhost:27017/', 
                        serverSelectionTimeoutMS=5000)
    # 測試連接
    client.admin.command('ping')
    print("成功連接到 MongoDB")
except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    print(f"無法連接到 MongoDB: {e}")
    exit(1)

db = client['test']
movies = db['movies']

def insert_demo():
    # insert
    new_profile = {'user_id': 213, 'name': 'Alan'}
    result = movies.insert_one(new_profile)
    print(f"插入文檔 ID: {result.inserted_id}")
    
    # read
    print("\n所有文檔:")
    for movie in movies.find():
        print(movie)

def update_demo():
    result = movies.update_one({'user_id': 213}, {'$set': {'user_id': 30}})
    print(f"更新了 {result.modified_count} 個文檔")
    
    # read
    print("\n更新後的文檔:")
    for movie in movies.find():
        print(movie)

def cleanup():
    # 清理測試資料
    result = movies.delete_many({'user_id': {'$in': [213, 30]}})
    print(f"\n清理了 {result.deleted_count} 個文檔")

if __name__ == "__main__":
    try:
        insert_demo()
        # update_demo()
        # cleanup()  # 取消註解以清理測試資料
    finally:
        client.close()
        print("\n已關閉連接")