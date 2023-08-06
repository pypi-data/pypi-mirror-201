import requests
import shutil
import json

from via_hub_logistc.model.zephry import TestFolder, TestCycle


class ReportManager():

    def __init__(self):
        self.product_token = None
        self.cycle_performer = None
        self.lst_scenarios = []
        self.branch_name = None
        self.cycle_execution_date = None
        self.product_url = None
        self.project_id = None
        self.cycle_folder_name = None
        self.cycle_description = None
        self.cycle_interation = None
        self.cycle_status = None
        self.plan_id = None
        self.project_key = None
        self.file_path = None
        self.send_result_path = None
        self.cycle_envireoment = None
        self.cycle_owner = None
        self.cycle_name = None
        self.cycle_id = None
        self.cycle_status_suit = None

    @property
    def cycle_status_suit(self):
        return self._cycle_status_suit

    @cycle_status_suit.setter
    def cycle_status_suit(self, value):
        self._cycle_status_suit = value

    @property
    def lst_scenarios(self):
        return self._lst_scenarios

    @lst_scenarios.setter
    def lst_scenarios(self, value):
        self._lst_scenarios = value

    @property
    def cycle_performer(self):
        return self._cycle_performer

    @cycle_performer.setter
    def cycle_performer(self, value):
        self._cycle_performer = value

    @property
    def branch_name(self):
        return self._branch_name

    @branch_name.setter
    def branch_name(self, value):
        self._branch_name = value

    @property
    def cycle_execution_date(self):
        return self._cycle_execution_date

    @cycle_execution_date.setter
    def cycle_execution_date(self, value):
        self._cycle_execution_date = value

    @property
    def product_url(self):
        return self._product_url

    @product_url.setter
    def product_url(self, value):
        self._product_url = value

    @property
    def project_id(self):
        return self._project_id

    @project_id.setter
    def project_id(self, value):
        self._project_id = value

    @property
    def cycle_folder_name(self):
        return self._cycle_folder_name

    @cycle_folder_name.setter
    def cycle_folder_name(self, value):
        self._cycle_folder_name = value

    @property
    def product_token(self):
        return self._product_token

    @product_token.setter
    def product_token(self, value):
        self._product_token = value

    @property
    def cycle_description(self):
        return self._cycle_description

    @cycle_description.setter
    def cycle_description(self, value):
        self._cycle_description = value

    @property
    def cycle_interation(self):
        return self._cycle_interation

    @cycle_interation.setter
    def cycle_interation(self, value):
        self._cycle_interation = value

    @property
    def cycle_status(self):
        return self._cycle_status

    @cycle_status.setter
    def cycle_status(self, value):
        self._cycle_status = value

    @property
    def plan_id(self):
        return self._plan_id

    @plan_id.setter
    def plan_id(self, value):
        self._plan_id = value

    @property
    def project_key(self):
        return self._project_key

    @project_key.setter
    def project_key(self, value):
        self._project_key = value

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        self._file_path = value

    @property
    def cycle_envireoment(self):
        return self._cycle_envireoment

    @cycle_envireoment.setter
    def cycle_envireoment(self, value):
        self._cycle_envireoment = value

    @property
    def cycle_owner(self):
        return self._cycle_owner

    @cycle_owner.setter
    def cycle_owner(self, value):
        self._cycle_owner = value

    @property
    def cycle_name(self):
        return self._cycle_name

    @cycle_name.setter
    def cycle_name(self, value):
        self._cycle_name = value

    @property
    def cycle_id(self):
        return self._cycle_id

    @cycle_id.setter
    def cycle_id(self, value):
        self._cycle_id = value

    @property
    def send_result_path(self):
        return self._send_result_path

    @send_result_path.setter
    def send_result_path(self, value):
        self._send_result_path = value

    ### Search id the of cycle in jira ###
    def get_cycle_id(self, cycle):

        uri = self.product_url + f'/testrun/{cycle}?fields=id'

        headers = {
            "Authorization": self.product_token
        }

        response = requests.request("GET", uri, headers=headers)

        return response.json()["id"]

    ### Add name the of cycle test in jira ###
    def create_cycle_name(self, project_id: int, release: str):
        release = release.title().replace("/", " ")

        uri = self.product_url + \
            f'/rest/tests/1.0/testrun/search?fields=id,key,name&query=testRun.projectId%20IN%20({project_id})'

        headers = {
            "Authorization": self.product_token
        }

        response = requests.request("GET", uri, headers=headers)

        cycles = response.json()['results']

        count_release = 0

        for cycle in cycles:
            if str(cycle['name']).find(release) > 0:
                count_release = count_release + 1

        return f'{release} | C{count_release + 1}'

    ###Create new folder for test regression ###
    def create_folder(self, folder_name: str, projectKey: str):
        uri = self.product_url + "/rest/atm/1.0/folder"

        headers = {
            "Authorization": self.product_token
        }

        payload = TestFolder(projectKey, folder_name, "TEST_RUN").__dict__

        requests.request("POST", uri, json=payload, headers=headers)

        return folder_name

    ###Create new cycle for test regression ###
    def create_cycle_test(self, folder_name: str, test_plan: str,  key: str, name_cycle: str, descripption: str, iteration: str, owner: str, cycle_date: str, status: str):
       
        payload = TestCycle(
            name_cycle,
            descripption,
            key,
            folder_name,
            iteration,
            owner,
            test_plan,
            cycle_date,
            status,
            []
        ).__dict__

        uri = self.product_url + "/rest/atm/1.0/testrun"

        headers = {
            "Authorization": self.product_token
        }

        response = requests.request("POST", uri, json=payload, headers=headers)

        return response.json()["key"]

    ### Add scenarios to an existing cycle ###
    def save_result_runner_tests(self, cycle: str, list_scenarios: dict):

        for scenario in list_scenarios:
            uri = self.product_url + \
                f'/rest/atm/1.0/testrun/{cycle}/testcase/{scenario["id"]}/testresult'

            headers = {
                "Authorization": self.product_token
            }

            requests.request('POST', uri, json=scenario["tc"], headers=headers)

    ### Add report the runner for existing cycle  ###
    def save_report_rennur(self, cycle, file_path, file_name):

        shutil.make_archive(file_name + "/result_test",
                            'zip', root_dir=file_path)

        f = open(file_name + '/result_test.zip', 'rb')

        files = {"file": f}

        uri = self.product_url + f"/rest/atm/1.0/testrun/{cycle}/attachments"

        headers = {
            "Authorization": self.product_token
        }

        requests.request("POST", uri, files=files, headers=headers)

    ### Get info the of created test case ###
    def get_owner_test_case(self, test_key):

        uri = self.product_url + f'/rest/atm/1.0/testcase/{test_key}'

        headers = {
            "Authorization": self.product_token
        }

        response = requests.request("GET", uri, headers=headers)

        return response.json()["owner"]

    ### Change status upadate cycle test ###
    def update_cycle_execution(self, project_id, cycle_id: str, status:str):
        url_status = self.product_url + \
            f'/rest/tests/1.0/project/{project_id}/testrunstatus'

        headers = {
            "Authorization": self.product_token
        }

        lst_status = requests.request("GET", url_status, headers=headers)

        for value in lst_status.json():
            status_jira = value['name']
            status_name = status

            if status_jira == status_name:
                status_id = value['id']

                url_cycle = self.product_url + \
                    f'/rest/tests/1.0/testrun/{cycle_id}?fields=id'

                jira_cycle_id = requests.request(
                    "GET", url_cycle, headers=headers).json()

                payload = {
                    "id": int(jira_cycle_id['id']),
                    "projectId": int(project_id),
                    "statusId": int(status_id)
                }

                url_change = self.product_url + \
                    f'/rest/tests/1.0/testrun/{jira_cycle_id["id"]}'

                requests.request("PUT", url_change,
                                 json=payload, headers=headers)
            
                break