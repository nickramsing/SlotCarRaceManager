import csv
from log_writer.logger import get_logger
#instantiate module level logger
logger = get_logger(__name__)

def export_schedule_csv_Heats(schedule,
                        CARS,
                        heats_filename) -> bool:
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
                        drivers_filename) -> bool:
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