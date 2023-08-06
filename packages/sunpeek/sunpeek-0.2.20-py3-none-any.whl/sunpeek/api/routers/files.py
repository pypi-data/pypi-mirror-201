from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.datastructures import UploadFile
from sqlalchemy.orm import Session

from sunpeek.common.utils import sp_logger
from sunpeek.common.data_uploader import DataUploader_db
from sunpeek.serializable_models import DataUploadResponse
from sunpeek.api.dependencies import session, crud
from sunpeek.api.routers.plant import plant_router
from sunpeek.common.data_uploader import DatetimeTemplates


files_router = APIRouter(
    prefix="/data",
    tags=["data"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@files_router.post("/div-zero")
def zero_div():
    """This method server as a usage example only for the log class and the HTTP exception raising. It must be deleted for release"""

    try:
        x = 1 / 0
    except (Exception) as err:

        # how to use the logger to report an exception
        sp_logger.exception(err)
        # how to manually report using the INFO level
        sp_logger.info("This won't print in file because of loggers level")
        # str(err) gives the message related to the exception
        error_dict = {"message": "UPS something went wrong", "error": str(err)}
        # raise HTTPException so the API returns an error code instead of freezing
        raise HTTPException(status_code=500, detail=error_dict)


@plant_router.post("/data", tags=["data"], response_model=DataUploadResponse)
def upload_measure_data(
        plant_id: int,
        files: List[UploadFile],
        datetime_template: DatetimeTemplates = None,
        datetime_format: str = None,
        timezone: str = None,
        csv_separator: str = ';',
        csv_decimal: str = '.',
        csv_encoding: str = 'utf-8',
        index_col: int = 0,
        sess: Session = Depends(session),
        crd: crud = Depends(crud)) -> DataUploadResponse:
    """Ingests csv files to database. For details, see docstring of the `data_uploader` module.

    Parameters
    ----------
    plant_id : A pre-configured plant with this name must exist in the database.
    files : list
        List of csv files that are batch ingested.
    datetime_template : DatetimeTemplates
        Templates to simplify the definition of a datetime format. Overridden by datetime_format (if not None).
    datetime_format : str
        Used to parse datetimes from csv file. Leave to None infers the format.
    timezone : str or pytz.timezone.
        Optional. To be provided if timestamps in the data have no time zone information.
    csv_separator : str
        Used in pd.read_csv as 'sep' kwarg
    csv_decimal : str
        Used in pd.read_csv as 'decimal' kwarg
    csv_encoding : str
        Used in pd.read_csv as 'encoding' kwarg
    index_col : int
        DataUploader will try to parse timestamps from this column.
    sess : sqlalchemy.orm.Session
    crd : api.dependencies.crud

    Returns
    -------
    upload_response : DataUploadResponse

    Raises
    ------
    ConnectionError
    HTTPException
    """

    up = DataUploader_db(plant=crd.get_plants(sess, plant_id),
                         files=files,
                         datetime_template=datetime_template,
                         datetime_format=datetime_format,
                         timezone=timezone,
                         csv_separator=csv_separator,
                         csv_decimal=csv_decimal,
                         csv_encoding=csv_encoding,
                         index_col=index_col,
                         session=sess)
    response = up.do_upload()
    return response  # DataUploadResponse
