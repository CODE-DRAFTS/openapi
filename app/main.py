from fastapi import FastAPI,Response,status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from  psycopg2.extras  import RealDictCursor
from time import sleep  
from app import utils,schemas, env
from app.routers import users, posts


app = FastAPI()



while True:
    try:
        conn = psycopg2.connect( host=env.database_host_name,port=env.database_port  ,database=env.database_name , user=env.database_user_name, password=env.database_password , cursor_factory=RealDictCursor)
        cursor= conn.cursor()
        print("db connection successful")
        break
    except Exception as error:
        print(f"db connection failed:{error}"  ) 
        sleep(2)
 
app.include_router(users.router)
app.include_router(posts.router)

@app.get("/")
async def root():
    return {"message": "hello world"}











