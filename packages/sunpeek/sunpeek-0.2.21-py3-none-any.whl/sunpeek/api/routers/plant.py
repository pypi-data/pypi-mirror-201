from fastapi import APIRouter, Depends, BackgroundTasks, Request
from typing import List, Union
from sqlalchemy.orm import Session
from sunpeek.common import config_parser
import sunpeek.exporter
import sunpeek.components as cmp
from sunpeek.api.dependencies import session, crud
import sunpeek.serializable_models as smodels
import sunpeek.demo.demo_plant as demo_plant_function

plants_router = APIRouter(
    prefix="/plants",
    tags=["plants"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

plant_router = APIRouter(
    prefix="/plants/{plant_id}",
    tags=["plant"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

any_plant_router = APIRouter(
    prefix="/plants/-",
    tags=["plant"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@plants_router.get("", response_model=List[smodels.Plant],
                   summary="List all plants")
def plants(name: str = None, session: Session = Depends(session), crud=Depends(crud)):
    plants = crud.get_plants(session, plant_name=name)
    if not isinstance(plants, list):
        plants = [plants]

    return plants


@plants_router.get("/summary", response_model=List[smodels.PlantSummary],
                   summary="Get a list of all plants, with only minimal information")
def plants(name: str = None, session: Session = Depends(session), crud=Depends(crud)):
    p = crud.get_plants(session, plant_name=name)
    return p


@plants_router.post("/new", response_model=smodels.Plant,
                    summary="create plants",
                    status_code=201,
                    responses={
                        409: {"description": "Conflict, most likely because the plant name or name of a child "
                                             "object already exists",
                              "model": smodels.Error}})
def create_plant(plant: smodels.NewPlant, session: Session = Depends(session), crud=Depends(crud)):
    """
    Create a new plant. `name`, `latitude`, `longitude` are required. sensors can be mapped by passing a list of sensor
    structures to `sensors`
    """
    plant = config_parser.make_full_plant(plant.dict(exclude_unset=True), session)
    # plant = crud.create_component(session, plant)
    # done at each plant update anyway
    # plant.config_virtuals()
    # plant = crud.update_component(session, plant)
    plant = crud.create_component(session, plant)
    return plant


@plants_router.get("/create_demo_plant", response_model=smodels.Plant,
                   summary="Create demo plant config, optionally including data, if data is to be included, "
                           "accept_license must also be set to true")
def demo_plant(name: str = None, include_data: bool = False, accept_license: bool = False,
               session: Session = Depends(session)):
    plant = demo_plant_function.create_demoplant(session, name)
    if include_data and accept_license:
        demo_plant_function.add_demo_data(plant, session)
    return plant


@plant_router.get("", response_model=smodels.Plant,
                  tags=["plants"],
                  summary="Get a single plant by id")
def plants(plant_id: int, session: Session = Depends(session), crud=Depends(crud)):
    p = crud.get_plants(session, plant_id)
    return p


@plant_router.get("/export_config",
                  response_model=smodels.ConfigExport,
                  tags=["plants", "export"],
                  summary="Export a plant configuration, optionally with data",
                  description="Export a plant with the sensor types, collector types, and fluid definitions it uses.")
def export_conf(plant_id: int, session: Session = Depends(session), crud=Depends(crud)):
    plant = crud.get_plants(session, plant_id=plant_id)
    return smodels.ConfigExport(**sunpeek.exporter.create_export_config(plant))


@plant_router.post("/export_complete", response_model=smodels.JobReference,
                   tags=["plants", "export"], summary="Export a plant with configuration and data",
                   description="""Create an export job for a compleate plant with sensor types, collector types, 
                   fluid definitions, and data. When the job completes a tar package containing a json file, 
                   and data 1 CSV file per calender year, is available for download""",
                   status_code=202)
def create_complete_export(request: Request, background_tasks: BackgroundTasks, plant_id: int,
                           include_virtuals: bool = True,
                           session: Session = Depends(session), crud=Depends(crud)):
    plant = crud.get_plants(session, plant_id=plant_id)
    job = cmp.Job(status=cmp.helpers.ResultStatus.pending, plant=plant)
    crud.create_component(session, job)
    background_tasks.add_task(sunpeek.exporter.create_export_package, plant, include_virtuals, job)
    return smodels.JobReference(job_id=job.id, href=str(request.url_for('jobs')) + str(job.id))


def update_obj(obj, update_model):
    update_dict = update_model.dict(exclude_unset=True)

    for key, val in update_dict.items():
        if val != getattr(obj, key):
            setattr(obj, key, val)

    return obj


@plant_router.post("", response_model=Union[smodels.Plant, List[smodels.Plant]],
                   summary="Update a plant",
                   responses={409: {"description": "Conflict, most likely because the plant name or name of a child "
                                                   "object already exists",
                                    "model": smodels.Error}})
def plants(plant_id: int, plant: smodels.UpdatePlant, session: Session = Depends(session), crud=Depends(crud)):
    plant_cmp = crud.get_plants(session, plant_id=plant_id)
    plant_cmp = update_obj(plant_cmp, plant)
    plant_cmp = crud.update_component(session, plant_cmp)
    return plant_cmp


@plant_router.post("/summary", response_model=Union[smodels.PlantSummary, List[smodels.PlantSummary]],
                   summary="Update a plant",
                   responses={409: {"description": "Conflict, most likely because the plant name or name of a child "
                                                   "object already exists",
                                    "model": smodels.Error}})
def plants(plant_id: int, plant: smodels.PlantSummaryBase, session: Session = Depends(session), crud=Depends(crud)):
    plant_cmp = crud.get_plants(session, plant_id=plant_id)
    plant_cmp = update_obj(plant_cmp, plant)
    plant_cmp = crud.update_component(session, plant_cmp)
    return plant_cmp


@plant_router.delete("", summary="Delete a plant by id")
def plants(plant_id: int, session: Session = Depends(session), crud=Depends(crud)):
    p = crud.get_plants(session, plant_id=plant_id)
    name = p.name
    session.delete(p)
    session.commit()

    return str(f'plant {name} was deleted')


@plant_router.get("/sensors", response_model=Union[List[smodels.Sensor], smodels.Sensor],
                  tags=["sensors"],
                  summary="Get a list of sensors, or select by id or raw name")
@any_plant_router.get("/sensors/{id}", response_model=smodels.Sensor, tags=["sensors"],
                      summary="Get a single sensor by id")
def sensors(id: int = None, raw_name: str = None, plant_id: int = None,
            session: Session = Depends(session), crud=Depends(crud)):
    sensors = crud.get_sensors(session, id, raw_name, plant_id)
    return sensors


@any_plant_router.post("/sensors", response_model=List[smodels.Sensor],
                  tags=["sensors"],
                  summary="Batch update a list of sensors, each passed sensor object must contain an id")
def update_sensors(sensors: List[smodels.BulkUpdateSensor], sess: Session = Depends(session), crd=Depends(crud)):
    for sensor in sensors:
        sensor_obj = crd.get_sensors(sess, sensor.id)
        crd.update_component(sess, update_obj(sensor_obj, sensor), commit=False)
    sess.commit()
    return sensors


@any_plant_router.post("/sensors/{id}", response_model=smodels.Sensor, tags=["sensors"],
                       summary="Update a single sensor by id")
def update_sensor(id: int, sensor_update: smodels.Sensor, sess: Session = Depends(session), crd=Depends(crud)):
    sensor_obj = crd.get_sensors(sess, id)
    sensor_obj = crd.update_component(sess, update_obj(sensor_obj, sensor_update))
    return sensor_obj


@plant_router.post("/sensors/new", response_model=List[smodels.Sensor],
                   summary="Create a new `Sensor` object or objects", tags=["sensors"], status_code=201,
                   responses={
                       409: {
                           "description": "Conflict, most likely because the sensor raw name already exists in this plant",
                           "model": smodels.Error}})
def create_sensors(plant_id: int, sensor: Union[smodels.NewSensor, List[smodels.NewSensor]],
                   session: Session = Depends(session), crud=Depends(crud)):
    """
    Create a new sensor or sensors. `raw_name` is required.
    To create multiple sensors at once, pass a list of sensor structures
    """
    if not isinstance(sensor, list):
        sensors = [sensor]
    else:
        sensors = sensor

    rets = []
    plant = crud.get_plants(session, plant_id=plant_id)
    for sensor in sensors:
        sensor = cmp.Sensor(**sensor.dict(), plant=plant)
        sensor = crud.create_component(session, sensor, commit=False)
        rets.append(sensor)

    session.commit()
    return rets


@any_plant_router.delete("/sensors/{id}", tags=["sensors"], summary="Delete a single sensor by id")
def delete_sensor(id: int, sess: Session = Depends(session), crd=Depends(crud)):
    sensor_obj = crd.get_sensors(sess, id)
    crd.delete_component(sess, sensor_obj)


@plant_router.get("/arrays", response_model=Union[List[smodels.Array], smodels.Array],
                  tags=["arrays"],
                  summary="Get a list of arrays, or select by id or name and plant")
@any_plant_router.get("/arrays/{id}", response_model=smodels.Array, tags=["arrays"],
                      summary="Get a single array by id")
def arrays(id: int = None, name: str = None, plant_id: int = None, plant_name: str = None,
           session: Session = Depends(session), crud=Depends(crud)):
    return crud.get_components(session, cmp.Array, id, name, plant_id, plant_name)


@any_plant_router.post("/arrays/{id}", response_model=smodels.Array,
                       tags=["arrays"],
                       summary="Update an array by id")
def update_array(id: int, array: smodels.Array, session: Session = Depends(session), crud=Depends(crud)):
    array_cmp = crud.get_components(session, component=cmp.Array, id=id)
    array = array.dict(exclude_unset=True)

    for key, val in array.items():
        setattr(array_cmp, key, val)

    array_cmp = crud.update_component(session, array_cmp)
    return array_cmp


@any_plant_router.delete("/arrays/{id}", tags=["arrays"],
                         summary="Delete an array by id")
def arrays(id: int, session: Session = Depends(session), crud=Depends(crud)):
    array = crud.get_components(session, component=cmp.Array, id=id)
    name = array.name
    session.delete(array)
    session.commit()


@plant_router.post("/arrays/new",
                   response_model=Union[List[smodels.Array], smodels.Array],
                   tags=["arrays"], status_code=201,
                   summary="Get a list of arrays, or select by id or name and plant",
                   responses={
                       409: {"description": "Conflict, most likely because the array name or a child object already "
                                            "exists in this plant", "model": smodels.Error}
                   })
def create_array(array: smodels.NewArray, plant_id: int, session: Session = Depends(session), crud=Depends(crud)):
    """
    Create a new array or arrays. `name` and `collector_type` are required.
    To create multiple arrays at once, pass a list of array structures.
    sensors can be mapped by passing a dict of sensor structures to `sensors` (**NOTE** not actually tested, may not work yet.
    """
    if not isinstance(array, list):
        arrays = [array]
    else:
        arrays = array

    rets = []
    for array in arrays:
        plant = crud.get_plants(session, plant_id)
        array_cmp = cmp.Array(**array.dict(exclude_unset=True), plant=plant)
        array_cmp = crud.create_component(session, array_cmp)
        rets.append(array_cmp)

    return rets


@plant_router.get("/fluids", response_model=Union[List[smodels.Fluid], smodels.Fluid],
                  tags=["fluids"],
                  summary="Get a list of fluids, or select by name")
def fluids(id: int = None, name: str = None, plant_id: int = None, plant_name: str = None,
           session: Session = Depends(session), crud=Depends(crud)):
    return crud.get_components(session, cmp.Fluid, id, name, plant_id, plant_name)


@plant_router.get("/fluids/{id}", response_model=smodels.Fluid,
                  tags=["fluids"],
                  summary="Get a single fluid by id")
def fluids(id: int, session: Session = Depends(session), crud=Depends(crud)):
    return crud.get_components(session, cmp.Fluid, id=id)
