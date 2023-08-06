from trojsdk.core.experiment_tools import TrojExperimenter
from trojsdk.core.client_utils import TrojJobHandler

def test_gen():
    conf_handler = TrojExperimenter("./trojsdk/examples/auth_config_dev.json")
    proj = "test_proj"
    dataset = "credit_dataset"
    model = "logistic_model"
    conf_handler.create_experiment(proj, dataset, model, delete_existing=True)
    conf_handler.log_testing_data(path_to_dset_file="s3://trojai-test-file-storage/stars_validation.csv", label_column="Type")
    conf_handler.log_model(model = "s3://trojai-test-file-storage/StarKNNPipe.pkl", model_wrapper_file = "s3://trojai-test-file-storage/StarKNNWrapper.py")
    conf_handler.log_attacks("trojsdk/examples/nlp_phil/attacks.json")
    '''
    "docker_image_url": "trojai/troj-engine-base-tabular:tabular-dev-latest",
    "docker_secret_name": "trojaicreds",
    "image_pull_policy": "IfNotPresent"
    '''
    conf_handler.log_docker_metadata("trojai/troj-engine-base-tabular:tabular-dev-latest", "trojaicreds", "IfNotPresent")
    k8s_dict = {
            "container_port": 80,
            "resources": {
                "requests": {
                    "cpu": "250m",
                    "memory": "800M"
                },
                "limits": {
                    "cpu": "500m",
                    "memory": "2000M"
                }
            },
            "tolerations": [
                {
                    "effect": "NoSchedule",
                    "operator": "Equal",
                    "value": "robustness-evaluation",
                    "key": "dedicated"
                }
            ]
        }
    conf_handler.log_k8s_metadata(k8s_dict)

    conf_handler.construct_base_config(task_type="tabular")
    tjh = conf_handler.run_troj_evaluation(proj, dataset, model)
    assert type(tjh) is TrojJobHandler 


def test_gen_with_upload():
    conf_handler = TrojExperimenter("./trojsdk/examples/auth_config_dev.json")
    conf_handler.minio_url = "trojaiminioapi.troj.red"
    proj = "test_proj"
    dataset = "credit_dataset"
    model = "logistic_model"
    conf_handler.create_experiment(proj, dataset, model, delete_existing=True)
    conf_handler.log_testing_data(path_to_dset_file="trojsdk\examples\local_files\stars_validation.csv", classes_dictionary= {
    "red dwarf": 0,
    "brown dwarf": 1,
    "white dwarf":  2,
    "main sequence": 3,
    "super giants": 4,
    "hyper giants": 5
  },label_column="Type")
    conf_handler.log_model(model = "trojsdk/examples/local_files/StarKNNPipe.pkl", model_wrapper_file = "trojsdk/examples/local_files/StarKNNWrapper.py")
    conf_handler.log_attacks("trojsdk\examples\star_attacks.json")
    conf_handler.log_docker_metadata("trojai/troj-engine-base-tabular:tabular-dev-latest", "trojaicreds", "IfNotPresent")
    k8s_dict = {
        "container_port": 80,
        "resources": {
            "requests": {
                "cpu": "250m",
                "memory": "800M"
            },
            "limits": {
                "cpu": "500m",
                "memory": "2000M"
            }
        },
        "tolerations": [
            {
                "effect": "NoSchedule",
                "operator": "Equal",
                "value": "robustness-evaluation",
                "key": "dedicated"
            }
        ]
    }
    conf_handler.log_k8s_metadata(k8s_dict)

    conf_handler.construct_base_config(task_type="tabular")
    tjh = conf_handler.run_troj_evaluation(proj, dataset, model)
    assert type(tjh) is TrojJobHandler 



# if __name__ == "__main__":
#     test_gen_with_upload()