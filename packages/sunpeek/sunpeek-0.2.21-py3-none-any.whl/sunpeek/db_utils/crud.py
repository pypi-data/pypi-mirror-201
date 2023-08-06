from sqlalchemy.orm import Session
import sunpeek.components as cmp
from typing import Union


def get_plants(session: Session, plant_id: int=None, plant_name: str=None):
    """
    Gets a plant by name from the database, or all plants if no `plant_name` or `plant_id` parameter is supplied
    Parameters
    ----------
    session
    plant_id
    plant_name

    Returns
    -------
    common.components.Plant object, if `plant_name` or `plant_id` param is supplied, otherwise list of all
    common.components.Plant objects in the DB.
    """

    if plant_id is not None:
        return session.query(cmp.Plant).filter(cmp.Plant.id == plant_id).one()
    elif plant_name is not None:
        return session.query(cmp.Plant).filter(cmp.Plant.name == plant_name).one()
    else:
        return session.query(cmp.Plant).all()


def get_components(session: Session, component: Union[cmp.Component, str], id: int = None, name:str = None, plant_id: int=None, plant_name: str=None):
    """
    Get a component, or list of components from the database.

    Parameters
    ----------
    session
    component: An instance of a subclass of cmp.Component
    id
    name
    plant_id
    plant_name

    Returns
    -------
    Comonent object, or list of Component objects
    """

    if isinstance(component, str):
        component = cmp.__dict__[component]

    qry = session.query(component)
    if id is not None:
        return qry.filter(component.id == id).one()
    if plant_id is not None:
        qry = qry.join(cmp.Plant).filter(cmp.Plant.id == plant_id)
    if name is not None and component != cmp.Sensor:
        return qry.filter(component.name == name).one()
    elif name is not None and component == cmp.Sensor:
        return qry.filter(component.raw_name == name).one()
    if plant_name is not None:
        qry = qry.join(cmp.Plant).filter(cmp.Plant.name == plant_name)
    return qry.all()


def get_sensors(session: Session, id: int = None, raw_name: str = None, plant_id: int=None, plant_name: str=None):
    """
    Get all sensors, all sensors of a given plant, or a specific sensor. Note, parameters have the following precedence:
    id, name, plant_id, plant_name. So if a component name is given, all further parameters are ignored

    Parameters
    ----------
    session
    component: An instance of a subclass of cmp.Component
    id
    raw_name
    plant_id
    plant_name

    Returns
    -------
    Sensor object, or list of Sensor objects
    """

    return get_components(session, cmp.Sensor, id, raw_name, plant_id, plant_name)


def create_component(session: Session, component: cmp.Component, commit=True):
    """
    Add a new component to the database

    Parameters
    ----------
    session
    component: An instance of a subclass of cmp.Component
    commit: whether to commit the new components, if set to false, session.commit() must be called later.

    Returns
    -------
    The updated object after commit to the database (this may have had modifications made by database side logic
    """
    session.add(component)
    if commit:
        session.commit()
    return component


def update_component(session: Session, component: cmp.helpers.ORMBase, commit=True):
    """
    Updates a component to the database

    Parameters
    ----------
    session
    component: An instance of a subclass of cmp.Component

    Returns
    -------
    The updated object after commit to the database (this may have had modifications made by database side logic
    commit: whether to commit the new components, if set to false, session.commit() must be called later.
    """
    session.add(component)
    if commit:
        session.commit()
    return component


def delete_component(session: Session, component: cmp.Component):
    """
    Removes a component from the database

    Parameters
    ----------
    session
    component: An instance of a subclass of cmp.Component

    Returns
    -------
    The updated object after commit to the database (this may have had modifications made by database side logic
    """

    session.delete(component)
    session.commit()
