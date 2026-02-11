# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SlotCarRaceManager is a tournament scheduling system for slot car races. It uses Google OR-Tools constraint programming to generate fair race schedules where:
- Configurable number of drivers (default 18) use configurable cars (default 6, identified by color)
- Each driver must use each car exactly once
- Every pair of drivers races together 1-2 times
- Drivers stay engaged (configurable max idle heats between races)
- Minimizes total heats, idle violations, and wasted lane slots

## Commands

```bash
# Install dependencies (requires Python 3.14+)
uv sync

# Run the scheduler to generate tournament CSV files
python main.py

# Validate generated schedule
jupyter notebook Validate_RaceSchedule.ipynb
```

## Architecture

**Entry Point**: `main.py` - Contains global configuration (CARS, SLOTS_PER_HEAT, NUMBER_OF_PARTICIPANTS) and orchestrates the workflow via `controller()`.

**Solver**: `services/create_race_schedule.py` - OR-Tools CP-SAT solver with binary decision variables:
- `x[d,c,h]`: driver d uses car c in heat h
- `y[h]`: heat h is used
- `p[d1,d2,h]`: drivers meet in heat h
- Idle constraint: `max_idle_heats` (default 3), modes: 'hard', 'soft', 'off'
- Objective: minimize `1000 * heats + idle_penalty * violations + wasted_slots`

**Output**: `services/publish_schedule.py` - Exports to two CSV views:
- `tournament_heats.csv`: Heat-centric (columns are car colors)
- `tournament_drivers.csv`: Driver-centric (Driver, Heat, Car)

**Logging**: `log_writer/logger.py` - JSON-formatted logs to `logs/app.log`. Uses factory pattern via `get_logger(__name__)`. Config in `log_writer/log_config.yaml`.

## Dependencies

- `ortools`: Constraint programming solver
- `polars`: DataFrame operations (used in validation notebook)
- `pyyaml`: Logger configuration
- `notebook`: Jupyter for validation

## Specialized Agent

For optimization work on `create_race_schedule.py`, see `OPTIMIZER_AGENT.md` which provides:
- Detailed constraint model documentation
- Feasibility analysis for different configurations
- OR-Tools patterns and best practices

## Planned Features

- RESTful API with FastAPI
- Dynamic configuration via API inputs (replacing global variables)
