import datetime

from fastapi import APIRouter, Depends, HTTPException
from typing import Union
from sunpeek.api.dependencies import session, crud
from sunpeek.api.routers.plant import plant_router
from sunpeek.api.routers.config import config_router
from sunpeek.core_methods.pc_method import PCMethod
import enum
import sunpeek.serializable_models as smodels

evaluations_router = APIRouter(
    prefix=plant_router.prefix + "/evaluations",
    tags=["methods", "evaluations"]
)

stored_evaluations_router = APIRouter(
    prefix=config_router.prefix + "/stored_evaluations/{stored_eval_id}",
    tags=["methods", "evaluations"]
)


@evaluations_router.get("/run")
@stored_evaluations_router.get("/run", tags=["methods", "evaluations"])
def run(plant_id: int, stored_eval_id: int, method: str = None,
        eval_start: str = "1900-01-01 00:00:00", eval_end: str = "2021-01-01 00:00:00",
        sess=Depends(session), crd=Depends(crud)):
    plant = crd.get_plants(sess, plant_id=plant_id)
    raise HTTPException(status_code=501,
                        detail="Stored evaluations are not yet implemented in HarvesIT", headers=
                        {"Retry-After": "Wed, 30 Nov 2022 23:59 GMT", "Cache-Control": "no-cache"})


class available_pc_equations(enum.IntEnum):
    one = 1
    two = 2


class available_pc_methods(enum.Enum):
    iso = 'iso'
    extended = 'extended'


@evaluations_router.get("/pc_method", summary="Run the PC method", response_model=smodels.PCMethodOutput)
def quick_run_pc_method(plant_id: int, method: available_pc_methods,
                        equation: Union[available_pc_equations, None],
                        eval_start: Union[datetime.datetime, None] = None,
                        eval_end: Union[datetime.datetime, None] = None,
                        sess=Depends(session), crd=Depends(crud)):
    """Runs the PC Method for the specified dates range"""
    plant = crd.get_plants(sess, plant_id=plant_id)
    plant.context.set_eval_interval(eval_start=eval_start, eval_end=eval_end)
    pc_obj = PCMethod.create(method=method.name, plant=plant, equation_id=equation)
    return pc_obj.run()

# @methods_router.get("/get-dcat-method-results")
# async def get_dcat_method_results(plant_id: str, start_date: str = "2021-05-20 13:00:00", end_date: str = "2021-05-21 13:00:00"):
#     """Retrieves the results of the DCAT method for the specified dates range"""
#     results_dict = {"plant_id": plant_id,"start_date":start_date, "end_date":end_date, "results_array": [1,1,2,1.5] }
#     return results_dict


# @methods_router.get("/run-pc-method")
# async def run_pc_method(plant_id: str, start_date: str = "2021-05-20 13:00:00", end_date: str = "2021-05-21 13:00:00"):
#     """Runs the PC method on the clean data stored between the specified dates range"""
#
#     results_dict = {"plant_id": plant_id,"start_date":start_date, "end_date":end_date, "results_array": [.35,.39,1.69,4.86,6.23,.51,5.25] }
#
#     return results_dict


# @methods_router.get("/run-dcat-method")
# async def run_dcat_method(plant_id: str, start_date: str = "2021-05-20 13:00:00", end_date: str = "2021-05-21 13:00:00"):
#     """Runs the DCAT method on the clean data stored between the specified dates range"""
#
#     results_dict = {"plant_id": plant_id,"start_date":start_date, "end_date":end_date, "results_array": [.35,.39,1.69,4.86,6.23,.51,5.25] }
#
#     return results_dict
