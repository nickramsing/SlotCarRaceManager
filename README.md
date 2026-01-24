#PROBLEM
You are an applied mathematician familiar with optimization problems. You are also a skilled hobbyist that races complex slot cars (such as scalextric slot cars) in fun, but highly competitive races. You are interested in ensuring races you host are fair and equitable. That is already challenging given that drivers possess different skills and levels of experiences and the slot cars do not perform exactly the same. You are hosting a race competition as the race director. The race competition is composed of a series of race events where You need to generate You want participants to all have fair chances per the following specifications: 1. You are constrained by having 6 cars: you can identify cars by their colors [Red, Green, Blue, Yellow, Orange, White]. 2. You have 18 drivers: you can label drivers D1 - D18 3. The race course can accommodate all 6 cars. So, each race event on the race course may have 6 drivers maximum. 4. Each driver must use each car (color) exactly once. This ensures equity with cars: everyone will have used each car. 5. Every driver must race other driver at least once but no more than twice. You must minimize the number of times drivers race against each other but you must ensure that everyone races each other. Can you construct a race schedule that ensures equity, but does not require endless race events? I want participants to be competitive, have fun, but not be board!
- Objective:
  - Minimize heats
  - Minimize wasted slots


#Technical Solution: true optimization / constraint-satisfaction model. 
- 6 cars / slots per heat
- Drivers must use each car once
- Some heats may be partially filled
- We want minimum number of heats and minimum wasted slots
- Every pair must meet ≥ 1 and ≤ 2 times
-Below is a true optimizer-style solver using backtracking + pruning. It will:
  - Work for 6, 12, 15, 18, … drivers
  - Minimizes number of heats
  - Minimizes wasted slots
  - Allows partially-filled heats (not full 6 lanes)
  - Enforces:
    - each driver uses each car exactly once
    - max 6 drivers per heat
    - pair constraints: no pair meets more than twice
    - every pair meets at least once
 


##Logger
###Features
* Single module: log_writer/logger.py
* Uses standard logging with get_logger(__name__)
* JSON-formatted logs (great for Polars ingestion)
* One file, append-only
* Includes:
  * timestamp
  * level
  * message
  * module
  * function
  * line number
* All levels → same file
* DEBUG can be disabled via config
* Raises if log file can’t be written
* Minimal + portable

###Directory layout
the_app/
├── log_writer/
│   ├── logger.py
│   └── log_config.yaml
├── main.py


#To Dos:
##Add logging:
1. create a logging module to handle logs
```python
import logging

# Configure logging to a file named 'app.log'
# Set the level to DEBUG to capture all messages
logging.basicConfig(filename='app.log', level=logging.DEBUG, filemode='w')

logging.debug("This message should go to a file")
logging.info("As should this one")
logging.warning("And this one too")

```

2. define a custom log message format 
3. send log message to log_writer
```python
import logging

# Define a custom log message format
log_format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'

logging.basicConfig(level=logging.INFO, format=log_format)

logger = logging.getLogger(__name__)

logger.info("This is a formatted log message")


```
4. Maintain logging levels
- DEBUG: Detailed information for diagnosing problems.
- INFO: Confirmation that things are working as expected.
- WARNING: An indication that something unexpected happened or might happen in the near future (the default level).
- ERROR: Due to a more serious problem, the software has not been able to perform some function.
- CRITICAL: A serious error, indicating that the program itself may be unable to continue running

###video to review:
https://www.youtube.com/watch?v=pxuXaaT1u3k