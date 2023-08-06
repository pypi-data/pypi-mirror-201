from trojsdk.core import data_utils
from trojsdk.core import client_utils
from trojsdk.core.client_utils import TrojJobHandler


def test_sdk_fail():

    troj_job_handler = TrojJobHandler()
    try:
        troj_job_handler.check_job_status()
        assert False
    except:
        assert True


def test_sdk_pass_tabular():

    troj_job_handler = client_utils.submit_evaluation(
        path_to_config="./trojsdk/examples/tabular_medical_insurance_config.json", nossl=True
    )

    import time

    time.sleep(2)
    try:
        troj_job_handler.check_job_status()
        print(troj_job_handler.status_response["data"])
        assert True
    except Exception as e:
        print(e)
        assert False
