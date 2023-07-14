# MongoDB

初步探索 MongoDB

* [目錄](https://github.com/twtrubiks/mongodb-tutorial#mongodb-shell-crud) - [Youtube Tutorial - 初步探索 MongoDB Shell CRUD - Part 1](https://youtu.be/ik6vKTdmGEQ)

* [目錄](https://github.com/twtrubiks/mongodb-tutorial#mongodb-gui-tool) - [Youtube Tutorial - MongoDB Compass (GUI) 以及 PyMongo - Part 2](https://youtu.be/yzovQ8WXwiA)

## 教學

[docker-compose.yml](docker-compose.yml)

```yml
version: '3.8'

services:

    db:
        image: mongo
        restart: always
        container_name: mongodb
        ports:
            - "27017:27017"
        environment:
            MONGO_INITDB_ROOT_USERNAME: root
            MONGO_INITDB_ROOT_PASSWORD: password
        volumes:
            - mongo_data:/data/db

volumes:
  mongo_data:
```


進入容器

```cmd
docker exec -it mongodb bash
```

連接

```cmd
mongosh admin -u root -p password
```

顯示 databases

```cmd
show dbs
```

顯示 collections (類似 RMDBS 中的 table)

```cmd
show collections
```

顯示 databases version

```cmd
db.version()
```

建立新的不存在 database

```sql
use test
```

## MongoDB Shell CRUD

* [Youtube Tutorial - 初步探索 MongoDB Shell CRUD - Part 1](https://youtu.be/ik6vKTdmGEQ)

官方文件可參考 [mongodb-shell](https://www.mongodb.com/docs/mongodb-shell/)

* [Insert Documents](https://www.mongodb.com/docs/mongodb-shell/crud/insert/#std-label-mongosh-insert)

- Insert a Single Document

```sql
use test

db.movies.insertOne(
  {
    title: "The Favourite",
    genres: [ "Drama", "History" ],
    runtime: 121,
    rated: "R",
    year: 2018,
    directors: [ "Yorgos Lanthimos" ],
    cast: [ "Olivia Colman", "Emma Stone", "Rachel Weisz" ],
    type: "movie"
  }
)

```

`insertOne()`

```text
returns a document that includes the newly inserted document's _id field value.
```

取回資料

```sql
db.movies.find( { title: "The Favourite" } )
```

- Insert Multiple Documents

```sql
use test

db.movies.insertMany([
   {
      title: "Jurassic World: Fallen Kingdom",
      genres: [ "Action", "Sci-Fi" ],
      runtime: 130,
      rated: "PG-13",
      year: 2018,
      directors: [ "J. A. Bayona" ],
      cast: [ "Chris Pratt", "Bryce Dallas Howard", "Rafe Spall" ],
      type: "movie"
    },
    {
      title: "Tag",
      genres: [ "Comedy", "Action" ],
      runtime: 105,
      rated: "R",
      year: 2018,
      directors: [ "Jeff Tomsic" ],
      cast: [ "Annabelle Wallis", "Jeremy Renner", "Jon Hamm" ],
      type: "movie"
    }
])
```

`insertMany()`

```text
returns a document that includes the newly inserted documents' _id field values.
```

取回全部的資料

```sql
db.movies.find( {} )
```

* [Query Documents](https://www.mongodb.com/docs/mongodb-shell/crud/read/#query-documents)

說明語法

```sql
use test
db.movies.find()
```

類似 RMDBS 中的

```sql
SELECT * FROM movies
```

Specify Equality Condition

```sql
use test
db.movies.find( { title: "The Favourite" } )
```

類似 RMDBS 中的

```sql
SELECT * FROM movies WHERE title = "The Favourite"
```

Specify Conditions Using Query Operators

```sql
use test
db.movies.find( { genres: { $in: [ "Drama", "PG-13" ] } } )
```

類似 RMDBS 中的

```sql
SELECT * FROM movies WHERE genres in ("Drama", "PG-13")
```

Specify Logical Operators(AND)

```sql
use test
db.movies.find( { rated: "R", runtime: { $gte: 120 } } )
```

rated 必須是 R, 然後 runtime 必須大於等於 120

Specify Logical Operators(OR)

```sql
use test
db.movies.find( {
     year: 2018,
     $or: [ { runtime: { $gte: 100 } }, { title: "Tag" } ]
} )
```

year 必須是 2018, 然後 runtime 必須大於等於 100 或 title 等於 Tag.

* [Update Documents](https://www.mongodb.com/docs/mongodb-shell/crud/update/#update-documents)

- Update a Single Document

```sql
use test

db.movies.updateOne(
  { title: "Jurassic World: Fallen Kingdom" }, {
    $set: {runtime: 77}
  })

db.movies.find( { title: "Jurassic World: Fallen Kingdom" } )

db.movies.updateOne(
  { title: "Jurassic World: Fallen Kingdom" },{
    $set: {runtime: "77"},
    $currentDate: { lastUpdated: true }
})
```

如果沒有的欄位, 會自動建立.

有關 `$currentDate` 的說明可參考
[currentDate](https://www.mongodb.com/docs/manual/reference/operator/update/currentDate/#mongodb-update-up.-currentDate)

- Update Multiple Documents

```sql
use test
db.movies.updateMany(
  { runtime: { $lt: 100 } },
  {
    $set: { runtime: 5, nights: 1 }
  }
)

db.movies.find( { nights: 1 } )
```

- Replace a Document

```sql
db.movies.replaceOne(
  { _id: ObjectId("64741819dcd1cd7e37d54731") },
  { test123: 893421, limit: 5000, products: [ "Investment", "Brokerage" ] }
)

db.movies.findOne( { _id: ObjectId("64741819dcd1cd7e37d54731") } )
```

* [Delete Documents](https://www.mongodb.com/docs/mongodb-shell/crud/delete/#std-label-mongosh-delete)

- Delete All Documents

```sql
use test
db.movies.deleteMany({})
```

- Delete All Documents that Match a Condition

```sql
use test
db.movies.deleteMany( { title: "Tag" } )
```

- Delete Only One Document that Matches a Condition

```sql
use test
db.movies.deleteOne( { _id: ObjectId("64741819dcd1cd7e37d54731") } )

db.movies.findOne( { _id: ObjectId("64741819dcd1cd7e37d54731") } )
```

## MongoDB GUI TOOL

* [Youtube Tutorial - MongoDB Compass (GUI) 以及 PyMongo - Part 2](https://youtu.be/yzovQ8WXwiA)

請直接到這邊下載 [MongoDB Compass (GUI)](https://www.mongodb.com/try/download/compass)

設定 Authentication Method

![alt tag](https://i.imgur.com/ESatcxG.png)

如果順利登入的話, 會看到類似的介面

![alt tag](https://i.imgur.com/etaKtAn.png)

## PyMongo

透過 [PyMongo documentation](https://pymongo.readthedocs.io/en/stable/tutorial.html) 把玩 MongoDB

安裝 pymongo

```cmd
pip3 install pymongo
```

範例 code

```python

from pymongo import MongoClient

client = MongoClient('mongodb://root:password@localhost:27017/')

db = client['test']

movies = db['movies']

def insert_demo():
    # insert
    new_profile = {'user_id': 213, 'name': 'Alan'}
    movies.insert_one(new_profile)

    # read
    for move in movies.find():
        print(move)

def update_demo():
    movies.update_one({'user_id': 213}, {'$set': {'user_id': 30}})

    # read
    for move in movies.find():
        print(move)

insert_demo()
# update_demo()
```

## Reference

* [https://www.mongodb.com](https://www.mongodb.com)