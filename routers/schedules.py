from fileinput import filename

import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import FileResponse
from models.slotcar_models import race_input_model
from services.schedule_controller import controller
from pathlib import Path
from log_writer.logger import get_logger

#instantiate module level logger
logger = get_logger(__name__)

#MOVE TO CONFIG
DOWNLOADS_DIR = Path("./output_files/")

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
        logger.info(f"Receiving race input data to pass to the controller. ")
        logger.info(f"Race input file data: {race_inputs} ")

        response = controller(number_of_participants=race_inputs.number_of_participants,
                              cars=race_inputs.cars,
                              slots_per_heat=race_inputs.slots_per_heat,
                              max_idle_heats=race_inputs.max_idle_heats,
                              solution_time_limit=race_inputs.solution_time_limit,
                              idle_constraint_mode=race_inputs.idle_constraint_mode)

        return {"message": "Schedule parameters received", "response": response}
    except Exception as e:
        logger.error(f"EXCEPTION OCCURRED:  {e} ")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/retrieveschedule")
async def retrieveschedule(file_name: str):
    """
    Retrieve and download the CSV file containing the full race schedule .

    parameters: race_input_model - matches Pydantic schema for race input parameters
    outcome: CSV file containing the full schedule -

    """
    try:
        logger.info(f"Retrieving FULL race schedule. ")
        logger.info(f"File name to retrieve: {file_name} ")

        # Construct full path and validate it exists
        file_path = DOWNLOADS_DIR / file_name

        # Security check - prevent directory traversal attacks
        if not file_path.resolve().is_relative_to(DOWNLOADS_DIR.resolve()):
            logger.error(f"EXCEPTION OCCURRED: Invalid file path  {file_path} ")
            raise HTTPException(status_code=400, detail="Invalid file path")

        if not file_path.exists():
            logger.error(f"EXCEPTION OCCURRED: File not found  {file_name} ")
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(
                path=file_path,
                media_type="text/csv",
                filename=file_name
            )
    except Exception as e:
        logger.error(f"EXCEPTION OCCURRED:  {e} ")
        raise HTTPException(status_code=400, detail=str(e))