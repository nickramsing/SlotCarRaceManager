import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from models.slotcar_models import race_input_model
from services.schedule_controller import controller

router = APIRouter()     #change to router next step



@router.post("/createschedule")
async def create_schedule(race_inputs: race_input_model):
    """
    Create a new schedule with the provided data.

    parameters: race_input_model - matches Pydantic schema for race input parameters
    outcome: schedule -
        question: result as a strream of schedule items?
            or as a CSV file
    """
    try:
        print("Checking received parameters")
        print(race_inputs)

        response = controller(number_of_participants=race_inputs.number_of_participants,
                              cars=race_inputs.cars,
                              slots_per_heat=race_inputs.slots_per_heat,
                              max_idle_heats=race_inputs.max_idle_heats,
                              solution_time_limit=race_inputs.solution_time_limit,
                              idle_constraint_mode=race_inputs.idle_constraint_mode)

        return {"message": "Schedule parameters received", "response": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))