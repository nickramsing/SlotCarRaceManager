from typing import List

import services.create_race_schedule as cs
import services.publish_schedule as ps
from log_writer.logger import get_logger

#instantiate module level logger
logger = get_logger(__name__)

##Switch to Environmental - YAML configuration
CSV_FILENAME_HEATS = "tournament_heats.csv"
CSV_FILENAME_DRIVERS = "tournament_drivers.csv"

def controller(number_of_participants: int,
               cars: List[str],
               slots_per_heat: int,
               max_idle_heats: int,
               solution_time_limit: int,
               idle_constraint_mode: str):

    logger.info(f"Initiating controller to generate schedule... ")
    try:
        schedule = cs.solve_tournament(num_drivers=number_of_participants,
                                       time_limit=solution_time_limit,
                                       CARS=cars,
                                       SLOTS_PER_HEAT=slots_per_heat,
                                       max_idle_heats=max_idle_heats,
                                       idle_constraint_mode=idle_constraint_mode)
        #Prints schedule to system console
        #outcome_console = ps.print_schedule_to_console(schedule=schedule)

        if schedule:
            '''
            If successfully create and return the schedule, then publish schedule in CSV files
            '''
            outcome_heat = ps.export_schedule_csv_Heats(schedule,
                                   CARS=cars,
                                   heats_filename=CSV_FILENAME_HEATS)

            outcome_drivers = ps.export_schedule_csv_Drivers(schedule,
                                   CARS=cars,
                                   drivers_filename=CSV_FILENAME_DRIVERS)
            #determine workflow based on function calls
            if outcome_heat == True and outcome_drivers == True:
                outcome = True
                message = f"FULL Schedule exported successfully. You can retrieve the race schedule in the file {CSV_FILENAME_HEATS}.  "
                message = message + f"Driver schedule exported successfully. You can retrieve the race schedule in the file {CSV_FILENAME_DRIVERS} "
            elif outcome_heat == True and outcome_drivers == False:
                outcome = False
                message = f"FULL Schedule exported successfully. You can retrieve the race schedule in the file {CSV_FILENAME_HEATS}.  "
                message = message + f"Driver schedule was NOT exported or created. You will need to remediate the issue - check the log file. "
            elif outcome_heat == False and outcome_drivers == True:
                outcome = False
                message = f"FULL Schedule was NOT exported or created. You will need to remediate the issue - check the log file.  "
                message = message + f"Driver schedule exported successfully. You can retrieve the race schedule in the file {CSV_FILENAME_DRIVERS}  "
            elif outcome_heat == False and outcome_drivers == False:
                outcome = False
                message = f"Neither FULL schedule or Driver schedule was exported or created. You will need to remediate the issue - check the log file. "

        return {"result": outcome, "message": message}
    except Exception as e:
        logger.error(f"EXCEPTION OCCURRED: running controller: {e}")
        return {"result": False, "message": f"EXCEPTION OCCURRED in controller: {e}"}