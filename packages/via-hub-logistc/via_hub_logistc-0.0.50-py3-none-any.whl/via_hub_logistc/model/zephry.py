class TestCase():
    def __init__(self, status, envireoment, create_tester, runner_tester, time_runner, iteration, actualStartDate, actualEndDate):
        self.status = status
        self.environment = envireoment
        self.assignedTo = create_tester
        self.executedBy = runner_tester
        self.executionTime = time_runner
        self.iteration = iteration
        self.actualStartDate = actualStartDate
        self.actualEndDate = actualEndDate

class TestFolder():
    def __init__(self, projectKey, name, type):
        self.projectKey = projectKey
        self.name = name
        self.type = type

class TestCycle():
    def __init__(self, name, desc, project_Key, folder, iteration, owner, testPlan, cycle_date, status, items):
        self.name = name
        self.description = desc
        self.projectKey = project_Key
        self.folder = folder
        self.status = status
        self.owner = owner
        self.plannedEndDate = cycle_date
        self.testPlanKey = testPlan
        self.plannedStartDate = cycle_date
        self.iteration = iteration
        self.items = items
