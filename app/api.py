""" Controller API for communication throughout the application """

from concurrent.futures import ThreadPoolExecutor

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.documentation import DESCRIPTION
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
    description=DESCRIPTION
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"]
)


@app.get("/")
def root() -> MessageResponse:
    """ Default Endpoint.

    Returns:
        MessageResponse: Dict containing welcome msg, code and data.
    """
    return {
        "msg": "Welcome to the FastAPI. Please visit http://localhost:8000/docs for more details.",
        "code": 200,
        "data": None
    }

@app.get("/ping")
def pong(log_lvl = "info") -> str:
    """ Endpoint for pinging.

    Args:
        log_lvl (str, optional): Logger level. Defaults to "info".

    Returns:
        str: pong
    """
    Logger.setLevel(log_lvl.upper())
    Logger.debug("pong")
    return "pong"

@app.get("/versions")
def get_versions(log_lvl = "info") -> MessageResponse:
    """ Endpoint to get the current versions.

    Returns:
        dict: Dict containing code, msg and all current versions.
    """
    Logger.setLevel(log_lvl.upper())
    Logger.info(f"App Version [{app.version}]")

    return {
        'msg': "/version success.",
        'code': 200,
        'data': {
            'version': app.version
        }
    }


@app.get("/get_data")
async def get_data(log_lvl = "info") -> DataResponse:
    """ Endpoint for getting all the data from the .csv file.

    Args:
        log_lvl (str, optional): Logger level. Defaults to "info".

    Returns:
        DataResponse: Dict containing code, msg and .csv data.
    """
    Logger.setLevel(log_lvl.upper())
    Logger.info("==> Get Data Request")

    data = Dataset.find()
    Logger.debug(f"{data=}")

    if data['code'] != 200:
        Logger.warning("Something is wrong.")

    return {
        'msg': "/get_data success.",
        'code': 200,
        'data': data['data']
    }

@app.post("/filter_data")
async def filter_data(data: FilterDatasetRequest, log_lvl = "info") -> DataResponse:
    """ Endpoint for gathering filtered .csv data.

    Args:
        data (FilterDatasetRequest): Body containing query.
        log_lvl (str, optional): Logger level. Defaults to "info".

    Returns:
        DataResponse: Dict containing code, msg and filtered .csv data.
    """
    Logger.setLevel(log_lvl.upper())
    Logger.info("==> Filter Data Request")

    data = Dataset.find(data.query)
    Logger.debug(f"{data=}")

    if data['code'] != 200:
        Logger.warning("Something is wrong.")

    return {
        'msg': "/filter_data success.",
        'code': 200,
        'data': data['data']
    }


""" Testing """

if __name__ == "__main__":
    # Terminal: uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
    Logger.info("=> Running FastAPI.")
    uvicorn.run("api:app", reload=True, port=8000)
