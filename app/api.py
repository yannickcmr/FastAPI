""" Controller API for communication throughout the application """

from concurrent.futures import ThreadPoolExecutor

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.logging_config import create_logger
from app.validation.messages import FilterDatasetRequest
from app.validation.messages import MessageResponse, DataResponse
from app.dataset.dataset import DatasetReader


""" Logging Function """

Logger = create_logger()
Logger.info("=> Logging initialized.")

""" Multithreading Option """

executor = ThreadPoolExecutor(1)
Logger.info("=> Thread Pool established.")


""" Dataset Class """

Dataset = DatasetReader("app/dataset/business_sales.csv")
Logger.info("=> Dataset ready.")


""" API """

app = FastAPI(
    title="FastAPI",
    version="0.6.9",
    contact={
        "name": "Yannick Ciomer",
        "email": ""
    },
    summary="FastAPI example to start from :)",
    description=""
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"]
)


@app.get("/")
def root() -> MessageResponse:
    return {
        "msg": "Welcome to the FastAPI. Please visit http://localhost:8000/docs for more details.",
        "code": 200,
        "data": None
    }

@app.get("/ping")
def pong(log_lvl = "info") -> str:
    Logger.setLevel(log_lvl.upper())
    Logger.debug("pong")
    return "pong"

@app.get("/versions")
def get_versions(log_lvl = "info") -> MessageResponse:
    """ Endpoint to get the current versions.

    Returns:
        dict: Dict containing all current versions.
    """
    Logger.setLevel(log_lvl.upper())
    Logger.info(f"App Version [{app.version}]")

    return {
        "msg": "/version success.",
        "code": 200,
        "data": None
    }


@app.get("/get_data")
async def get_data(log_lvl = "info") -> DataResponse:
    Logger.setLevel(log_lvl.upper())
    Logger.info(f"==> Get Data Request")

    data = Dataset.find()
    Logger.debug(f"==> Get Data Response: {data=}")

    if data['code'] != 200:
        Logger.warning(f"Something is wrong.")

    return {
        'msg': "/get_data success.",
        'code': 200,
        'data': data['data']
    }

@app.post("/filter_data")
async def filter_data(data: FilterDatasetRequest, log_lvl = "info") -> DataResponse:
    Logger.setLevel(log_lvl.upper())
    Logger.info(f"==> Filter Data Request")

    data = Dataset.find(data.query)
    Logger.debug(f"==> Filter Data Response: {data=}")

    if data['code'] != 200:
        Logger.warning(f"Something is wrong.")

    return {
        'msg': "/filter_data success.",
        'code': 200,
        'data': data['data']
    }


""" Testing """

if __name__ == "__main__":
    # Terminal: uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
    print("=> Running FastAPI.")
    uvicorn.run("api:app", reload=True, port=8000)
