from fastapi import FastAPI
import configparser
import json

from utils import get_most_similar_title
from data_io import DataIO


def get_data():
    dataio=DataIO()
    df = dataio.get_data()
    return df


data = get_data()
app = FastAPI()


@app.get("/")
def ping():
    return {"Hello": "World", "Health":"Good", "api":"bas_url/api?query=something"}


@app.get("/api")
async def get_result(query:str = "", top_n:int = 5):
    global data
    if query=="":
        return {'msg':'Query Param Empty, use api?query=something is something'}
    return get_most_similar_title(query, data, top_n)
