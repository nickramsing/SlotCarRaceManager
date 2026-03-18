import csv
from pathlib import Path
from datetime import datetime
from log_writer.logger import get_logger
try:
    import yaml
except ImportError:
    raise ImportError("PyYAML is required for publishing race schedules. PyYAML can be instead with `pip' or uv: 'pyyaml'")
#instantiate module level logger
logger = get_logger(__name__)

def _load_config(config_path: Path) -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def get_export_schedule_config() -> dict:
    '''
    Purpose: grabs configuration file and parameters for export race schedules
    :return: dict with parameters for export schedule
        datetime format and file names
    '''
    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / "export_config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Schedule EXPORT config not found at {config_path}")

    try:
        config = _load_config(config_path)

        output_directory = "output_files/"   #default directory
        driver_file = config.get("driver_file", "DRIVERS")
        heats_file = config.get("heats_file", "HEATS")
        datetime_format = config.get("datetime_format", "%Y-%m-%d-%H:%M")
        return {"Directory": output_directory,
                "DriverFile": driver_file,
                "HeatFile": heats_file,
                "DateTimeFormat": datetime_format
                }
    except Exception as e:
        logger.error(f"EXCEPTION OCCURRED: could not obtain export file information: {e}")
        return None


def construct_filename(type_file: str, event_name: str) -> str:
    '''
    Purpose: construct filename by concatenating params
    :param event_name:
    :param type_file:
    :return: filename_with_path - event_name & type_file & datetime
    '''
    try:
        #get file parameters: datetime_format, directory, type_file
        file_params = get_export_schedule_config()
        if file_params:
            directory_path = file_params["Directory"]
            dt = datetime.now().strftime(file_params["DateTimeFormat"])
            event_name = event_name.replace(" ", "-")
            if type_file == "DRIVERS":
                type_of_file = file_params["DriverFile"]
            else:
                type_of_file = file_params["HeatFile"]
            filename_with_path = directory_path + event_name + "_" + type_of_file + "_" + dt + ".csv"
            return filename_with_path
        else:
            return None
    except Exception as e:
        logger.error(f"EXCEPTION OCCURRED: could not generate file name: {e}")
        return None


def export_schedule_csv_Heats(schedule,
                        CARS,
                        event_name: str) -> bool:
    '''
    Saves a schedule to CSV files: heats - full schedule of heats

    :param schedule: schedule for race tournament
    :param heats_filename: filename for heats file
    :param drivers_filename: filename for drivers file

    :return: Boolean:  True if able to save schedule; False otherwise
    '''
    # --- Heats View ---
    try:
        logger.info(f"Attempting to save full race schedule of Heats: generating... ")
        heats_filename = construct_filename(type_file="HEATS", event_name=event_name)
        if not heats_filename:
            heats_filename = "output_files/HEATS.csv"
        with open(heats_filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Heat"] + CARS)

            for i, heat in enumerate(schedule, 1):
                row = [f"Heat {i}"]
                car_to_driver = {car: d for d, car in heat}
                for car in CARS:
                    row.append(car_to_driver.get(car, ""))
                writer.writerow(row)
        logger.info(f"Full schedule of heats successfully exported to: {heats_filename}")
        return True

    except Exception as e:
        logger.error(f"EXCEPTION OCCURRED: generating full schedule: {e}")
        return False

def export_schedule_csv_Drivers(schedule,
                        CARS,
                        event_name: str) -> bool:
    '''
    Saves a schedule to CSV files: for each driver
    Provides each driver with a listing of their upcoming race heats
    where they will participate

    :param schedule: schedule for race tournament
    :param CARS: list of cars
    :param drivers_filename: filename for drivers file

    :return: Boolean:  True if able to save schedule; False otherwise
    '''
    try:
        logger.info(f"Attempting to save Drivers schedule: generating... ")
        drivers_filename = construct_filename(type_file="DRIVERS", event_name=event_name)
        if not drivers_filename:
            drivers_filename = "output_files/DRIVERS.csv"
        with open(drivers_filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Driver", "Heat", "Car"])

            for i, heat in enumerate(schedule, 1):
                for d, car in heat:
                    writer.writerow([d, f"Heat {i}", car])
        logger.info(f"Drivers schedule successfully exported to: {drivers_filename}")
        return True
    except Exception as e:
        logger.error(f"EXCEPTION OCCURRED: generating driver schedule: {e}")
        return False


def print_schedule_to_console(schedule) -> bool:
    '''
    Prints a schedule to the console
    :param schedule: schedule
    :return: Boolean:  True if able to save schedule; False otherwise
    '''
    try:
        logger.info(f"Printing schedule to console...")
        for i, heat in enumerate(schedule, 1):
            print(f"\nHeat {i} ({len(heat)} drivers)")
            for d, car in heat:
                print(f"  {car:7} → {d}")
        logger.info(f"Successfully printed schedule to console.")
        return True
    except Exception as e:
        logger.error(f"EXCEPTION OCCURRED: print schedule to console: {e}")
        return False