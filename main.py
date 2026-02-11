from os import supports_dir_fd
import services.create_race_schedule as cs
import services.publish_schedule as ps
from log_writer.logger import get_logger
#instantiate module level logger
logger = get_logger(__name__)

#Global variables
CARS = ["Red", "Green", "Blue", "Yellow", "Orange", "White"]
SLOTS_PER_HEAT = 6
NUMBER_OF_PARTICIPANTS = 18
MAX_IDLE_HEATS = 3  # Target maximum consecutive heats a driver can sit out
IDLE_CONSTRAINT_MODE = 'soft'  # 'hard', 'soft', or 'off'
SOLUTION_TIME_LIMIT = 60
CSV_FILENAME_HEATS = "tournament_heats.csv"
CSV_FILENAME_DRIVERS = "tournament_drivers.csv"

'''
IMPROVEMENTS
todo: check on out each function SHOULD return
todo: How might include RESTful API with FASTAPI to support request?
todo: if receive inputs via RESTful API, then need to redo the global variables! How store with default/received values?
'''

def controller():
    logger.info(f"Initiating controller to generate schedule... ")
    try:
        schedule = cs.solve_tournament(num_drivers=NUMBER_OF_PARTICIPANTS,
                                       time_limit=SOLUTION_TIME_LIMIT,
                                       CARS=CARS,
                                       SLOTS_PER_HEAT=SLOTS_PER_HEAT,
                                       max_idle_heats=MAX_IDLE_HEATS,
                                       idle_constraint_mode=IDLE_CONSTRAINT_MODE)
        #Prints schedule to system console
        #outcome_console = ps.print_schedule_to_console(schedule=schedule)

        if schedule:
            '''
            If successfully create and return the schedule, then publish schedule in CSV files
            '''
            outcome_heat = ps.export_schedule_csv_Heats(schedule,
                                   CARS=CARS,
                                   heats_filename=CSV_FILENAME_HEATS)

            outcome_drivers = ps.export_schedule_csv_Drivers(schedule,
                                   CARS=CARS,
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

if __name__ == "__main__":
    result = controller()
    print(result)


