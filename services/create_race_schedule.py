from ortools.sat.python import cp_model
import itertools
#from main import CARS, SLOTS_PER_HEAT


def solve_tournament(num_drivers, time_limit, CARS, SLOTS_PER_HEAT, max_idle_heats=3,
                     idle_constraint_mode='soft', idle_penalty_weight=500):
    """
    Solve the tournament scheduling problem using CP-SAT.

    Args:
        num_drivers: Number of drivers in the tournament
        time_limit: Maximum solver time in seconds
        CARS: List of car names/colors
        SLOTS_PER_HEAT: Maximum drivers racing per heat
        max_idle_heats: Target maximum consecutive heats a driver can sit out (default 3)
        idle_constraint_mode: 'hard' (must satisfy), 'soft' (penalize violations), or 'off'
        idle_penalty_weight: Penalty per idle violation in soft mode (default 500).
            Higher values prioritize engagement over fewer heats.
            Reference: each heat costs 1000, each wasted slot costs 1.

    Returns:
        List of heats, where each heat is a list of (driver, car) tuples
    """
    drivers = list(range(num_drivers))
    cars = list(range(len(CARS)))

    total_slots = num_drivers * len(CARS)
    min_heats = (total_slots + SLOTS_PER_HEAT - 1) // SLOTS_PER_HEAT
    max_heats = min_heats + 8   # buffer for feasibility with idle constraints

    model = cp_model.CpModel()

    # x[d,c,h] = 1 if driver d uses car c in heat h
    x = {}
    for d in drivers:
        for c in cars:
            for h in range(max_heats):
                x[d, c, h] = model.NewBoolVar(f"x_d{d}_c{c}_h{h}")

    # y[h] = 1 if heat h is used
    y = {h: model.NewBoolVar(f"y_h{h}") for h in range(max_heats)}

    # p[d1,d2,h] = 1 if both drivers are in heat h
    p = {}
    for d1, d2 in itertools.combinations(drivers, 2):
        for h in range(max_heats):
            p[d1, d2, h] = model.NewBoolVar(f"p_{d1}_{d2}_h{h}")

    # --- Constraints ---

    # Each driver uses each car exactly once
    for d in drivers:
        for c in cars:
            model.Add(sum(x[d, c, h] for h in range(max_heats)) == 1)

    # Driver can only be in one car per heat
    for d in drivers:
        for h in range(max_heats):
            model.Add(sum(x[d, c, h] for c in cars) <= 1)

    # Each car used at most once per heat
    for c in cars:
        for h in range(max_heats):
            model.Add(sum(x[d, c, h] for d in drivers) <= 1)

    # Heat capacity
    for h in range(max_heats):
        model.Add(sum(x[d, c, h] for d in drivers for c in cars) <= SLOTS_PER_HEAT * y[h])

    # Link y[h] to usage
    for h in range(max_heats):
        model.Add(sum(x[d, c, h] for d in drivers for c in cars) >= y[h])

    # Pairing constraints
    for d1, d2 in itertools.combinations(drivers, 2):
        for h in range(max_heats):
            model.Add(p[d1, d2, h] <= sum(x[d1, c, h] for c in cars))
            model.Add(p[d1, d2, h] <= sum(x[d2, c, h] for c in cars))
            model.Add(p[d1, d2, h] >= sum(x[d1, c, h] for c in cars) +
                      sum(x[d2, c, h] for c in cars) - 1)

        # Each pair meets at least once, at most twice
        model.Add(sum(p[d1, d2, h] for h in range(max_heats)) >= 1)
        model.Add(sum(p[d1, d2, h] for h in range(max_heats)) <= 2)

    # Symmetry breaking: heats must be used in order (heat h+1 can only be used if heat h is used)
    for h in range(max_heats - 1):
        model.AddImplication(y[h + 1], y[h])

    # Idle time constraint: no driver sits out more than max_idle_heats consecutive heats
    # For each window of (max_idle_heats + 1) consecutive heats, driver must race at least once
    window_size = max_idle_heats + 1
    idle_violations = []

    if idle_constraint_mode in ('hard', 'soft'):
        for d in drivers:
            for h_start in range(max_heats - window_size + 1):
                window_heats = range(h_start, h_start + window_size)
                races_in_window = sum(x[d, c, h] for c in cars for h in window_heats)

                if idle_constraint_mode == 'hard':
                    # Hard constraint: must race at least once in window (if window is active)
                    model.Add(races_in_window >= 1).OnlyEnforceIf(y[h_start + window_size - 1])
                else:
                    # Soft constraint: penalize violations
                    # violation = 1 iff (window is active AND driver doesn't race in window)
                    last_heat = h_start + window_size - 1

                    # no_race = 1 iff driver doesn't race in this window
                    no_race = model.NewBoolVar(f"no_race_d{d}_h{h_start}")
                    model.Add(races_in_window == 0).OnlyEnforceIf(no_race)
                    model.Add(races_in_window >= 1).OnlyEnforceIf(no_race.Not())

                    # violation = y[last_heat] AND no_race
                    violation = model.NewBoolVar(f"idle_violation_d{d}_h{h_start}")
                    # violation => y[last_heat] and violation => no_race
                    model.AddImplication(violation, y[last_heat])
                    model.AddImplication(violation, no_race)
                    # (y[last_heat] AND no_race) => violation
                    model.AddBoolOr([y[last_heat].Not(), no_race.Not(), violation])

                    idle_violations.append(violation)

    # --- Objective ---
    # Minimize: heats (weight 1000) + wasted slots (weight 1) + idle violations (configurable)
    wasted = []
    for h in range(max_heats):
        used = sum(x[d, c, h] for d in drivers for c in cars)
        wasted.append(SLOTS_PER_HEAT * y[h] - used)

    objective = 1000 * sum(y[h] for h in range(max_heats)) + sum(wasted)
    if idle_violations:
        objective += idle_penalty_weight * sum(idle_violations)
    model.Minimize(objective)

    # --- Solve ---
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 8

    status = solver.Solve(model)

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("No feasible solution found.")
        return None

    # --- Extract schedule ---
    schedule = []
    for h in range(max_heats):
        if solver.Value(y[h]) == 1:
            heat = []
            for d in drivers:
                for c in cars:
                    if solver.Value(x[d, c, h]):
                        heat.append((f"D{d+1}", CARS[c]))
            schedule.append(heat)

    return schedule

