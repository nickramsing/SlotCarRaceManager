from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import List

class idle_modes(str, Enum):
    hard = 'hard'
    soft = 'soft'
    off = 'off'


class race_input_model(BaseModel):
    number_of_participants: int     # total number of drivers
    cars: List[str]                 # list of cars - in COLORS of the car
    slots_per_heat: int             # number of slots per heat == number of cars that be in a heat
    max_idle_heats: int             # target maximum consecutive heats a driver must sit out
    solution_time_limit: int        # time in seconds to produce a solution
    idle_constraint_mode: idle_modes    #model constraint modes

    model_config = ConfigDict(json_schema_extra={
        'examples': [
            {
                "number_of_participants": 18,
                "cars": ["Red", "Green", "Blue", "Yellow", "Orange", "White"],
                "slots_per_heat": 6,
                "max_idle_heats": 3,
                "solution_time_limit": 60,
                "idle_constraint_mode": "soft"
            },
            {
                "number_of_participants": 12,
                "cars": ["Red", "Green", "Blue", "Yellow", "Orange", "White"],
                "slots_per_heat": 6,
                "max_idle_heats": 3,
                "solution_time_limit": 60,
                "idle_constraint_mode": "off"
            }
        ]
    })

