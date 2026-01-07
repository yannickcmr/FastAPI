""" Endpoints for CSV Reader """

from fastapi import APIRouter

from app.config.logging_config import create_logger
from app.validation.messages import FilterDatasetRequest
from app.validation.messages import DataResponse
from app.dataset.dataset import DatasetReader


""" Logging Function """

Logger = create_logger()
Logger.info("=> Logging initialized.")


""" Dataset Class """

Dataset = DatasetReader("app/dataset/business_sales.csv")
Logger.info("=> Dataset ready.")


""" API """

router = APIRouter(tags=['database'])

@router.get("/get_data")
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

@router.post("/filter_data")
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
