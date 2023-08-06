from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Float, Integer, Identity, ForeignKey, DateTime, Enum, Interval, Boolean, ARRAY
from sunpeek.components.helpers import ORMBase, ComponentParam, AttrSetterMixin
from sunpeek.components import Plant, Fluid


class PCMethodOutput(ORMBase, AttrSetterMixin):
    __tablename__ = 'pc_method_outputs'

    id = Column(Integer, Identity(0), primary_key=True)

    plant_id = Column(Integer, ForeignKey('plant.id'))
    plant = relationship("Plant")

    datetime_eval_start = Column(DateTime(timezone=True))
    datetime_eval_end = Column(DateTime(timezone=True))

    # TODO Move these to the calling job, once we have a job system for PC calls
    # datetime_job_start = Column(DateTime(timezone=True), primary_key=True)
    # datetime_job_done = Column(DateTime(timezone=True), primary_key=True)

    # Algorithm settings
    pc_method_name = Column(String)  # The version of the PC method used to reflect the plant hydraulic layout
    evaluation_mode = Column(Enum('ISO', 'extended', name='pc_evaluation_modes'))
    equation = Column(Integer)
    check_accuracy_level = Column(Integer)

    interval_length = Column(Interval)
    safety_combined = Column(Float)
    wind_used = Column(Boolean)

    max_nan_density = Column(Float)
    min_data_in_interval = Column(Integer)
    max_gap_in_interval = Column(Interval)

    # Results
    n_intervals = Column(Integer)

    datetime_intervals_start = Column(ARRAY(DateTime(timezone=True)))
    datetime_intervals_end = Column(ARRAY(DateTime(timezone=True)))

    # Plant results
    tp_measured = ComponentParam('W', type='array')
    tp_sp_measured = ComponentParam('W m**-2', type='array')
    tp_sp_expected = ComponentParam('W m**-2', type='array')
    tp_sp_expected_safety = ComponentParam('W m**-2', type='array')

    target_actual_slope = ComponentParam('')
    target_actual_slope_safety = ComponentParam('')

    # Array results
    array_results = relationship("PCMethodOutputArray")

    fluid_solar_id = Column(ForeignKey(Fluid.id))
    fluid_solar = relationship("Fluid")
    mean_temperature = ComponentParam('K')
    mean_fluid_density = ComponentParam('kg m**-3')
    mean_fluid_heat_capacity = ComponentParam('J kg**-1 K**-1')


class PCMethodOutputArray(ORMBase, AttrSetterMixin):
    __tablename__ = 'pc_results_arrays'

    id = Column(Integer, Identity(0), primary_key=True)
    parent_result_id = Column(Integer, ForeignKey('pc_method_outputs.id', ondelete="CASCADE"))
    # parent_result = relationship("PCMethodOutput", back_populates="array_results")

    array_id = Column(ForeignKey('arrays.id'))
    array = relationship("Array")

    tp_sp_measured = ComponentParam('W m**-2', type='array')
    tp_sp_expected = ComponentParam('W m**-2', type='array')
    tp_sp_expected_safety = ComponentParam('W m**-2', type='array')
