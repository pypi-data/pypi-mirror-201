from trojsdk.core.ExperimentTools import TrojExperimenter
from trojsdk.core.client_utils import TrojJobHandler

def test_gen():
    conf_handler = TrojExperimenter("./trojsdk/examples/auth_config_dev.json")
    proj = "test_proj"
    dataset = "credit_dataset"
    model = "logistic_model"
    conf_handler.create_experiment(proj, dataset, model, delete_existing=True)
    # conf_handler.log_training_data()
    conf_handler.log_testing_data("train_set.json", path_to_dset_file="s3://trojai-test-file-storage/stars_validation.csv", label_column="Type")
    conf_handler.log_model(model = "s3://trojai-test-file-storage/StarKNNPipe.pkl", model_wrapper_file = "s3://trojai-test-file-storage/StarKNNWrapper.py")
    conf_handler.log_attacks("trojsdk/examples/tabular_test/all_pipe_transform_config.json")
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
            ],
            "node_selector": {
                "dedicated": "robustness-evaluation"
            }
        }
    conf_handler.log_k8s_metadata(k8s_dict)

    conf_handler.construct_base_config()
    tjh = conf_handler.run_troj_evaluation(proj, dataset, model)
    assert type(tjh) is TrojJobHandler 

def test_gen_w_minio_upload():
    pass
