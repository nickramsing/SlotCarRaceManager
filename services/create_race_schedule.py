from ortools.sat.python import cp_model
import itertools
#from main import CARS, SLOTS_PER_HEAT


def solve_tournament(num_drivers, time_limit, CARS, SLOTS_PER_HEAT):
    drivers = list(range(num_drivers))
    cars = list(range(len(CARS)))

    total_slots = num_drivers * len(CARS)
    min_heats = (total_slots + SLOTS_PER_HEAT - 1) // SLOTS_PER_HEAT
    max_heats = min_heats + 5   # small buffer for feasibility

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

    # --- Objective ---
    # Minimize number of heats + wasted slots
    wasted = []
    for h in range(max_heats):
        used = sum(x[d, c, h] for d in drivers for c in cars)
        wasted.append(SLOTS_PER_HEAT * y[h] - used)

    model.Minimize(1000 * sum(y[h] for h in range(max_heats)) + sum(wasted))

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

