from ortools.sat.python import cp_model


# AP usage of each level
AP_USAGE_LIST = [ 10, 10, 10, 10,   15, 15, 15, 15,   20, 20, 20, 20]

# List of resources given by each stage (with bonus)
# The rows are the resources and the columns are the stages
RESOURCE_LIST = [[21,  0,  0, 26,   32,  0,  0, 42,   45, 26, 26, 64],
                 [ 2, 13,  4,  0,    4, 20,  8,  0,    8, 28,  0,  0],
                 [ 3,  6, 20,  0,    6, 12, 30,  0,   12,  0, 42,  0],]

# Currency target
REQUIREMENT_LIST = [8588, 1920, 10225]

# The amount of AP used to clear initially
INITIAL_CLEAR_AP = 285

# The amount of currency received in the initial clear
INITIAL_CLEAR = [1335, 867, 867]



# Solver
model = cp_model.CpModel()
var_upper_bound = 1000000
qs = []
for i in range(1,len(AP_USAGE_LIST)+1):
    qs += [model.NewIntVar(0, var_upper_bound, "q" + str(i))]

for j, constraint in enumerate(RESOURCE_LIST):
    f_i = constraint[0] * qs[0]
    for i in range(1, len(constraint)):
        f_i = f_i + constraint[i] * qs[i]
    model.Add((REQUIREMENT_LIST[j] - INITIAL_CLEAR[j]) <= f_i)

f_0 =INITIAL_CLEAR_AP + AP_USAGE_LIST[0] * qs[0]
for j in range(1, len(AP_USAGE_LIST)):
    f_0 = f_0 + AP_USAGE_LIST[j] * qs[j]

model.Minimize(f_0)

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f"Minimum AP required: {solver.ObjectiveValue()}\n")
    for i in range(len(AP_USAGE_LIST)):
        print(f"q{i+1} = {solver.Value(qs[i])}")
else:
    print("No solution found.")
