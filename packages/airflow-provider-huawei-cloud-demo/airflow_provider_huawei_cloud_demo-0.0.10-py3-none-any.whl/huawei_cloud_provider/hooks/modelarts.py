#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from __future__ import annotations

from typing import Any

from airflow.exceptions import AirflowException
from huawei_cloud_provider.hooks.base_huawei_cloud import HuaweiBaseHook


class ModelArtsHook(HuaweiBaseHook):

    def create_dataset(
        self,
        data_sources: list[dict],
        work_path: str,
        work_path_type: int,
        data_format: str | None = None,
        dataset_name: str | None = None,
        dataset_type: int | None = None,
        description: str | None = None,
        import_annotations: bool | None = None,
        import_data: bool | None = None,
        label_format: dict | None = None,
        labels: list[dict] | None = None,
        managed: bool | None = None,
        schema: list[dict] | None = None,
        workforce_information: dict | None = None,
        workspace_id: str | None = None,
    ):
        try:
            return self.post_request(
                url="https://modelarts.$REGION.myhuaweicloud.com/v2/$PROJECT_ID/datasets",
                body={
                    "data_sources": data_sources,
                    "work_path": work_path,
                    "work_path_type": work_path_type,
                    "data_format": data_format,
                    "dataset_name": dataset_name,
                    "dataset_type": dataset_type,
                    "description": description,
                    "import_annotations": import_annotations,
                    "import_data": import_data,
                    "label_format": label_format,
                    "labels": labels,
                    "managed": managed,
                    "schema": schema,
                    "workforce_information": workforce_information,
                    "workspace_id": workspace_id
                }
            ).json()
        except Exception as e:
            raise AirflowException(f"Errors when creating dataset {e}")

    def create_dataset_version(
        self,
        dataset_id: str,
        clear_hard_property: bool | None,
        description: str | None,
        export_images: bool | None,
        remove_sample_usage: bool | None,
        train_evaluate_sample_ratio: str | None,
        version_format: str | None,
        version_name: str | None,
        with_column_header: bool | None,
    ):
        try:
            return self.post_request(
                url=f"https://modelarts.$REGION.myhuaweicloud.com/v2/$PROJECT_ID/datasets/{dataset_id}/versions",
                body={
                    "clear_hard_property": clear_hard_property,
                    "description": description,
                    "export_images": export_images,
                    "remove_sample_usage": remove_sample_usage,
                    "train_evaluate_sample_ratio": train_evaluate_sample_ratio,
                    "version_format": version_format,
                    "version_name": version_name,
                    "with_column_header": with_column_header
                }
            ).json()
        except Exception as e:
            raise AirflowException(f"Errors when creating dataset version {e}")

    def update_dataset(
        self,
        dataset_id: str,
        add_labels: list[dict] | None = None,
        current_version_id: str | None = None,
        dataset_name: str | None = None,
        delete_labels: list[dict] | None = None,
        description: str | None = None,
        update_labels: list[dict] | None = None
    ):
        try:
            return self.put_request(
                url=f"https://modelarts.$REGION.myhuaweicloud.com/v2/$PROJECT_ID/datasets/{dataset_id}",
                body={
                    "add_labels": add_labels,
                    "current_version_id": current_version_id,
                    "dataset_name": dataset_name,
                    "delete_labels": delete_labels,
                    "description": description,
                    "update_labels": update_labels
                }).json()
        except Exception as e:
            raise AirflowException(f"Errors when updating dataset {e}")

    def delete_dataset_version(self, dataset_id: str, version_id: str):
        try:
            self.delete_request(
                url=f"https://modelarts.$REGION.myhuaweicloud.com/v2/$PROJECT_ID/datasets/{dataset_id}/versions/{version_id}")
            return {}
        except Exception as e:
            raise AirflowException(f"Errors when deleting dataset {e}")

    def delete_dataset(self, dataset_id: str):
        try:
            self.delete_request(
                url=f"https://modelarts.$REGION.myhuaweicloud.com/v2/$PROJECT_ID/datasets/{dataset_id}")
            return {}
        except Exception as e:
            raise AirflowException(f"Errors when deleting dataset {e}")

    def create_algorithm(
        self,
        metadata: dict | None = None,
        job_config: dict | None = None,
        resource_requirements: list[dict] | None = None,
        advanced_config: dict | None = None
    ):
        try:
            return self.post_request(
                url="https://modelarts.$REGION.myhuaweicloud.com/v2/$PROJECT_ID/algorithms",
                body={
                    "metadata": metadata,
                    "job_config": job_config,
                    "resource_requirements": resource_requirements,
                    "advanced_config": advanced_config
                }).json()
        except Exception as e:
            raise AirflowException(f"Errors when creating algorithm {e}")

    def change_algorithm(
            self,
            algorithm_id: str,
            metadata: dict | None = None,
            job_config: dict | None = None,
            resource_requirements: list[dict] | None = None,
            advanced_config: dict | None = None):
        try:
            return self.put_request(
                url=f"https://modelarts.$REGION.myhuaweicloud.com/v2/$PROJECT_ID/algorithms/{algorithm_id}",
                body={
                    "metadata": metadata,
                    "job_config": job_config,
                    "resource_requirements": resource_requirements,
                    "advanced_config": advanced_config
                }).json()
        except Exception as e:
            raise AirflowException(f"Errors when changing algorithm {e}")

    def delete_algorithm(self, algorithm_id: str):
        try:
            self.delete_request(
                url=f"https://modelarts.$REGION.myhuaweicloud.com/v2/$PROJECT_ID/algorithms/{algorithm_id}")
            return {}
        except Exception as e:
            raise AirflowException(f"Errors when deleting algorithm {e}")

    def create_training_job(
        self,
        kind: str,
        metadata: dict,
        algorithm: dict | None = None,
        tasks: list[dict] | None = None,
        spec: dict | None = None
    ):
        try:
            return self.post_request(
                url=f"https://modelarts.$REGION.myhuaweicloud.com/v2/$PROJECT_ID/training-jobs",
                body={
                    "kind": kind,
                    "metadata": metadata,
                    "algorithm": algorithm,
                    "tasks": tasks,
                    "spec": spec
                }).json()
        except Exception as e:
            raise AirflowException(f"Errors when creating training job {e}")

    def delete_training_job(
        self,
        training_job_id: str
    ):
        try:
            return self.delete_request(
                url=f"https://modelarts.$REGION.myhuaweicloud.com/v2/$PROJECT_ID/training-jobs/{training_job_id}")
        except Exception as e:
            raise AirflowException(f"Errors when deleting training job {e}")

    def stop_training_job(
        self,
        training_job_id: str,
        action_type: str | None = None
    ):
        try:
            return self.post_request(
                url=f"https://modelarts.$REGION.myhuaweicloud.com/v2/$PROJECT_ID/training-jobs/{training_job_id}/actions",
                body={
                    "action_type": action_type
                }).json()
        except Exception as e:
            raise AirflowException(f"Errors when stopping training job {e}")

    def create_service(
        self,
        infer_type: str,
        service_name: str,
        workspace_id: str | None = None,
        schedule: list[dict] | None = None,
        cluster_id: str | None = None,
        pool_name: str | None = None,
        vpc_id: str | None = None,
        description: str | None = None,
        security_group_id: str | None = None,
        subnet_network_id: str | None = None,
        config: list[dict] | None = None,
        additional_properties: dict | None = None
    ):
        try:
            return self.post_request(
                url=f"https://modelarts.$REGION.myhuaweicloud.com/v1/$PROJECT_ID/services",
                body={
                    "infer_type": infer_type,
                    "service_name": service_name,
                    "workspace_id": workspace_id,
                    "schedule": schedule,
                    "cluster_id": cluster_id,
                    "pool_name": pool_name,
                    "vpc_id": vpc_id,
                    "description": description,
                    "security_group_id": security_group_id,
                    "subnet_network_id": subnet_network_id,
                    "config": config,
                    "additional_properties": additional_properties
                }).json()
        except Exception as e:
            raise AirflowException(f"Errors when creating service {e}")

    def delete_service(
        self,
        service_id: str
    ):
        try:
            return self.delete_request(
                url=f"https://modelarts.$REGION.myhuaweicloud.com/v1/$PROJECT_ID/services/{service_id}")
        except Exception as e:
            raise AirflowException(f"Errors when deleting service {e}")

    def update_service(
        self,
        service_id: str,
        schedule: list[dict] | None = None,
        description: str | None = None,
        config: list[dict] | None = None,
        status: str | None = None,
        additional_properties: dict | None = None
    ):
        try:
            return self.put_request(
                url=f"https://modelarts.$REGION.myhuaweicloud.com/v1/$PROJECT_ID/services/{service_id}",
                body={
                    "schedule": schedule,
                    "description": description,
                    "config": config,
                    "status": status,
                    "additional_properties": additional_properties
                }).json()
        except Exception as e:
            raise AirflowException(f"Errors when updating service {e}")

    def create_model(
        self,
        model_version: str,
        source_location: str,
        model_type: str,
        model_name: str,
        model_docs: list[dict] | None = None,
        template: dict | None = None,
        source_job_version: str | None = None,
        source_copy: str | None = None,
        initial_config: str | None = None,
        execution_code: str | None = None,
        source_job_id: str | None = None,
        output_params: list[dict] | None = None,
        description: str | None = None,
        runtime: str | None = None,
        model_metrics: str | None = None,
        source_type: str | None = None,
        dependencies: list[dict] | None = None,
        workspace_id: str | None = None,
        model_algorithm: str | None = None,
        apis: list[dict] | None = None,
        install_type: list[str] | None = None,
        input_params: list[dict] | None = None
    ):
        try:
            return self.post_request(
                url=f"https://modelarts.$REGION.myhuaweicloud.com/v1/$PROJECT_ID/models",
                body={
                    "model_version": model_version,
                    "source_location": source_location,
                    "model_type": model_type,
                    "model_name": model_name,
                    "model_docs": model_docs,
                    "template": template,
                    "source_job_version": source_job_version,
                    "source_copy": source_copy,
                    "initial_config": initial_config,
                    "execution_code": execution_code,
                    "source_job_id": source_job_id,
                    "output_params": output_params,
                    "description": description,
                    "runtime": runtime,
                    "model_metrics": model_metrics,
                    "source_type": source_type,
                    "dependencies": dependencies,
                    "workspace_id": workspace_id,
                    "model_algorithm": model_algorithm,
                    "apis": apis,
                    "install_type": install_type,
                    "input_params": input_params
                }).json()
        except Exception as e:
            raise AirflowException(f"Errors when creating model {e}")

    def delete_model(
        self,
        model_id: str
    ):
        try:
            return self.delete_request(
                url=f"https://modelarts.$REGION.myhuaweicloud.com/v1/$PROJECT_ID/models/{model_id}")
        except Exception as e:
            raise AirflowException(f"Errors when deleting model {e}")

    def list_dataset(self):
        try:
            return self.get_request(
                url=f"https://modelarts.$REGION.myhuaweicloud.com/v2/$PROJECT_ID/datasets").json()
        except Exception as e:
            raise AirflowException(f"Errors when listing dataset {e}")

    def list_dataset_version(self, dataset_id: str):
        try:
            return self.get_request(
                url=f"https://modelarts.$REGION.myhuaweicloud.com/v2/$PROJECT_ID/datasets/{dataset_id}/versions").json()
        except Exception as e:
            raise AirflowException(f"Errors when listing dataset version {e}")

    def list_training_job(self, training_job_id: str):
        try:
            return self.get_request(
                url=f"https://modelarts.$REGION.myhuaweicloud.com/v2/$PROJECT_ID/training-jobs/{training_job_id}").json()
        except Exception as e:
            raise AirflowException(f"Errors when listing training job {e}")

    def show_service(self, service_id: str):
        try:
            return self.get_request(
                url=f"https://modelarts.$REGION.myhuaweicloud.com/v1/$PROJECT_ID/services/{service_id}").json()
        except Exception as e:
            raise AirflowException(f"Errors when showing service {e}")
