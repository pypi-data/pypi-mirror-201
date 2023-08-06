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
"""This module contains Huawei Cloud ModelArts operators."""
from __future__ import annotations

import json
from typing import TYPE_CHECKING, Sequence

from airflow.models import BaseOperator
from huawei_cloud_provider.hooks.modelarts import ModelArtsHook

if TYPE_CHECKING:
    from airflow.utils.context import Context


class ModelArtsCreateDatasetOperator(BaseOperator):
    """
    This operator is used to create a dataset.

    :param data_sources: Input dataset path, which is used to synchronize source data
        (such as images, text files, and audio files) in the directory and its subdirectories to the dataset.
        For a table dataset, this parameter indicates the import directory.
        The work directory of a table dataset cannot be an OBS path in a KMS-encrypted bucket.
        Only one data source can be imported at a time.
    :param work_path: Output dataset path, which is used to store output files such as label files.
        The format is /Bucket name/File path, for example, /obs-bucket/flower/rose/. (The directory is used as the path.)
        A bucket cannot be directly used as a path.
        The output dataset path is different from the input dataset path or its subdirectory.
        The value contains 3 to 700 characters.
    :param work_path_type: Type of the dataset output path. Options:
        0: OBS bucket (default value)
    :param data_format: Data format. Options:
        Default: default format
        CarbonData: CarbonData
    :param dataset_name: Dataset name.
    :param dataset_type: Dataset type. Options:
        0: image classification
        1: object detection
        3: image segmentation
        100: text classification
        101: named entity recognition
        102: text triplet
        200: sound classification
        201: speech content
        202: speech paragraph labeling
        400: table dataset
        600: video labeling
        900: custom format
    :param description: Dataset description.
    :param import_annotations: Whether to automatically import the labeling information in the input directory,
    supporting detection, image classification, and text classification. Options:
    true: Import labeling information in the input directory. (Default value)
    false: Do not import labeling information in the input directory.
    :param import_data: Whether to import data. This parameter is used only for table datasets. Options:
    true: Import data when creating a database.
    false: Do not import data when creating a database. (Default value)
    :param label_format: Label format information. This parameter is used only for text datasets.
    :param labels: Label format information. This parameter is used only for text datasets.
    :param managed: Whether to host a dataset. Options:
    true: Host a dataset.
    false: Do not host a dataset. (Default value)
    :param schema: Schema list.
    :param workforce_information: Team labeling information.
    :param workspace_id: Workspace ID.
    :param project_id: Specifies the project ID.
    :param region: Regions where the API is available.
    :param huaweicloud_conn_id: The Airflow connection used for ModelArts credentials.
    """

    def __init__(
        self,
        data_sources: list[dict],
        work_path: str,
        work_path_type: int,
        dataset_name: str,
        data_format: str | None = None,
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
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.region = region
        self.project_id = project_id
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.data_sources = data_sources
        self.work_path = work_path
        self.work_path_type = work_path_type
        self.data_format = data_format
        self.dataset_name = dataset_name
        self.dataset_type = dataset_type
        self.description = description
        self.import_annotations = import_annotations
        self.import_data = import_data
        self.label_format = label_format
        self.labels = labels
        self.managed = managed
        self.schema = schema
        self.workforce_information = workforce_information
        self.workspace_id = workspace_id

    def execute(self, context: Context):

        model_arts_hook = ModelArtsHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, region=self.region, project_id=self.project_id
        )

        return model_arts_hook.create_dataset(

            data_sources=self.data_sources,
            work_path=self.work_path,
            work_path_type=self.work_path_type,
            data_format=self.data_format,
            dataset_name=self.dataset_name,
            dataset_type=self.dataset_type,
            description=self.description,
            import_annotations=self.import_annotations,
            import_data=self.import_data,
            label_format=self.label_format,
            labels=self.labels,
            managed=self.managed,
            schema=self.schema,
            workforce_information=self.workforce_information,
            workspace_id=self.workspace_id
        )


class ModelArtsCreateDatasetVersionOperator(BaseOperator):
    """
    This operator is used to create a dataset.

    """
    template_fields = ("dataset_id",)

    def __init__(
        self,
        dataset_id: str,
        clear_hard_property: bool | None = None,
        description: str | None = None,
        export_images: bool | None = None,
        remove_sample_usage: bool | None = None,
        train_evaluate_sample_ratio: str | None = None,
        version_format: str | None = None,
        version_name: str | None = None,
        with_column_header: bool | None = None,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.dataset_id = dataset_id
        self.clear_hard_property = clear_hard_property
        self.description = description
        self.export_images = export_images
        self.remove_sample_usage = remove_sample_usage
        self.train_evaluate_sample_ratio = train_evaluate_sample_ratio
        self.version_format = version_format
        self.version_name = version_name
        self.with_column_header = with_column_header
        self.region = region
        self.project_id = project_id
        self.huaweicloud_conn_id = huaweicloud_conn_id

    def execute(self, context: Context):

        model_arts_hook = ModelArtsHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, region=self.region, project_id=self.project_id
        )

        return model_arts_hook.create_dataset_version(
            dataset_id=self.dataset_id,
            clear_hard_property=self.clear_hard_property,
            description=self.description,
            export_images=self.export_images,
            remove_sample_usage=self.remove_sample_usage,
            train_evaluate_sample_ratio=self.train_evaluate_sample_ratio,
            version_format=self.version_format,
            version_name=self.version_name,
            with_column_header=self.with_column_header,
        )


class ModelArtsUpdateDatasetOperator(BaseOperator):
    """
    This operator used to modify basic information about a dataset,
    such as the dataset name, description, current version, and labels.

    :param dataset_id: Dataset ID.
    :param add_labels: List of added labels.
    :param current_version_id: ID of current dataset version.
    :param dataset_name: Dataset name.
    :param delete_labels: List of deleted labels.
    :param description: Dataset description. The value contains 0 to 256 characters and does not support
    the following special characters: ^!<>=&"'
    :param update_labels: List of updated labels.
    :param project_id: Specifies the project ID.
    :param region: Regions where the API is available.
    :param huaweicloud_conn_id: The Airflow connection used for ModelArts credentials.
    """

    template_fields: Sequence[str] = ("dataset_id",)
    def __init__(
        self,
        dataset_id: str,
        add_labels: list[dict] | None = None,
        current_version_id: str | None = None,
        dataset_name: str | None = None,
        delete_labels: list[dict] | None = None,
        description: str | None = None,
        update_labels: list[dict] | None = None,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.region = region
        self.project_id = project_id
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.dataset_id = dataset_id
        self.dataset_name = dataset_name
        self.description = description
        self.add_labels = add_labels
        self.delete_labels = delete_labels
        self.update_labels = update_labels
        self.current_version_id = current_version_id

    def execute(self, context: Context):

        model_arts_hook = ModelArtsHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, region=self.region, project_id=self.project_id)

        return model_arts_hook.update_dataset(
            dataset_id=self.dataset_id,
            dataset_name=self.dataset_name,
            description=self.description,
            add_labels=self.add_labels,
            delete_labels=self.delete_labels,
            update_labels=self.update_labels,
            current_version_id=self.current_version_id
        )


class ModelArtsDeleteDatasetVersionOperator(BaseOperator):
    """
    This operator used to delete a dataset labeling version.

    :param dataset_id: Dataset ID.
    :param version_id: Dataset version ID.
    :param project_id: Specifies the project ID.
    :param region: Regions where the API is available.
    :param huaweicloud_conn_id: The Airflow connection used for ModelArts credentials.
    """

    template_fields: Sequence[str] = ("dataset_id", "version_id")
    def __init__(
        self,
        dataset_id: str,
        version_id: str,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.region = region
        self.project_id = project_id
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.dataset_id = dataset_id
        self.version_id = version_id

    def execute(self, context: Context):

        model_arts_hook = ModelArtsHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, region=self.region, project_id=self.project_id
        )

        return model_arts_hook.delete_dataset_version(
            dataset_id=self.dataset_id, version_id=self.version_id
        )


class ModelArtsDeleteDatasetOperator(BaseOperator):
    """
    This operator used to delete a dataset without deleting the source data of the dataset.

    :param dataset_id: Dataset ID.
    :param project_id: Specifies the project ID.
    :param region: Regions where the API is available.
    :param huaweicloud_conn_id: The Airflow connection used for ModelArts credentials.
    """
    template_fields: Sequence[str] = ("dataset_id",)

    def __init__(
        self,
        dataset_id: str,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.region = region
        self.project_id = project_id
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.dataset_id = dataset_id

    def execute(self, context: Context):

        model_arts_hook = ModelArtsHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, region=self.region, project_id=self.project_id
        )

        return model_arts_hook.delete_dataset(
            dataset_id=self.dataset_id
        )

class ModelArtsCreateAlgorithmOperator(BaseOperator):
    """
    This operator used to create an algorithm.

    :param metadata: Algorithm metadata, which describes basic algorithm information.
    :param job_config: Algorithm configuration, such as the boot file.
    :param resource_requirements: Algorithm resource constraint. You can disable this function by not setting this parameter.
    :param advanced_config: Advanced algorithm configuration. Currently, autosearch is supported.
    :param project_id: Specifies the project ID.
    :param region: Regions where the API is available.
    :param huaweicloud_conn_id: The Airflow connection used for ModelArts credentials.
    """

    def __init__(
        self,
        metadata: dict | None = None,
        job_config: dict | None = None,
        resource_requirements: list[dict] | None = None,
        advanced_config: dict | None = None,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.region = region
        self.project_id = project_id
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.metadata = metadata
        self.job_config = job_config
        self.resource_requirements = resource_requirements
        self.advanced_config = advanced_config

    def execute(self, context: Context):

        model_arts_hook = ModelArtsHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, region=self.region, project_id=self.project_id
        )

        return model_arts_hook.create_algorithm(
            metadata=self.metadata,
            job_config=self.job_config,
            resource_requirements=self.resource_requirements,
            advanced_config=self.advanced_config
        )


class ModelArtsDeleteAlgorithmOperator(BaseOperator):
    """
    This operator used to delete an algorithm.

    :param algorithm_id: Algorithm ID.
    :param project_id: Specifies the project ID.
    :param region: Regions where the API is available.
    :param huaweicloud_conn_id: The Airflow connection used for ModelArts credentials.
    """
    template_fields: Sequence[str] = ("algorithm_id",)

    def __init__(
        self,
        algorithm_id: str,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.region = region
        self.project_id = project_id
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.algorithm_id = algorithm_id

    def execute(self, context: Context):

        model_arts_hook = ModelArtsHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, region=self.region, project_id=self.project_id
        )

        return model_arts_hook.delete_algorithm(algorithm_id=self.algorithm_id)


class ModelArtsChangeAlgorithmOperator(BaseOperator):
    """
    This operator used to modify an algorithm.

    :param algorithm_id: Algorithm ID.
    :param metadata: Algorithm metadata, which describes basic algorithm information.
    :param job_config: Algorithm configuration, such as the boot file.
    :param resource_requirements: Algorithm resource constraint. You can disable this function by not setting this parameter.
    :param advanced_config: Advanced algorithm configuration. Currently, autosearch is supported.
    :param project_id: Specifies the project ID.
    :param region: Regions where the API is available.
    :param huaweicloud_conn_id: The Airflow connection used for ModelArts credentials.
    """
    template_fields: Sequence[str] = ("algorithm_id",)

    def __init__(
        self,
        algorithm_id: str,
        metadata: dict | None = None,
        job_config: dict | None = None,
        resource_requirements: list[dict] | None = None,
        advanced_config: dict | None = None,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.region = region
        self.project_id = project_id
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.algorithm_id = algorithm_id
        self.metadata = metadata
        self.job_config = job_config
        self.resource_requirements = resource_requirements
        self.advanced_config = advanced_config

    def execute(self, context: Context):

        model_arts_hook = ModelArtsHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, region=self.region, project_id=self.project_id
        )

        return model_arts_hook.change_algorithm(
            algorithm_id=self.algorithm_id,
            metadata=self.metadata,
            job_config=self.job_config,
            resource_requirements=self.resource_requirements,
            advanced_config=self.advanced_config
        )


class ModelArtsCreateTrainingJobOperator(BaseOperator):
    """
    This operator used to create a training job.

    :param kind: Training job type, which is job by default. Options:
        job: training job
        hetero_job: heterogeneous job
        autosearch_job: auto search job
        mrs_job: MRS job
        edge_job: edge job
    :param metadata: Metadata of a training job.
    :param algorithm: Algorithm used by a training job. Options:
        id: Only the algorithm ID is used.
        subscription_id+item_version_id: The subscription ID and version ID of the algorithm are used.
        code_dir+boot_file: The code directory and boot file of the training job are used.
    :param tasks: List of tasks in heterogeneous training jobs. If this parameter is specified, leave the spec parameter blank.
    :param spec: Specifications of a training job. If this parameter is specified, leave the tasks parameter blank.
    :param project_id: Specifies the project ID.
    :param region: Regions where the API is available.
    :param huaweicloud_conn_id: The Airflow connection used for ModelArts credentials.
    """

    template_fields = ("algorithm")
    template_fields_renderers = {"algorithm": "json"}

    def __init__(
        self,
        kind: str,
        metadata: dict,
        algorithm: dict | None = None,
        tasks: list[dict] | None = None,
        spec: dict | None = None,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.region = region
        self.project_id = project_id
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.kind = kind
        self.metadata = metadata
        self.algorithm = algorithm
        self.tasks = tasks
        self.spec = spec

    def execute(self, context: Context):

        model_arts_hook = ModelArtsHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, region=self.region, project_id=self.project_id
        )

        return model_arts_hook.create_training_job(
            kind=self.kind,
            metadata=self.metadata,
            algorithm=self.algorithm,
            tasks=self.tasks,
            spec=self.spec
        )


class ModelArtsDeleteTrainingJobOperator(BaseOperator):
    """
    This operator used to delete a training job.

    :param training_job_id: ID of a training job.
    :param project_id: Specifies the project ID.
    :param region: Regions where the API is available.
    :param huaweicloud_conn_id: The Airflow connection used for ModelArts credentials.
    """
    template_fields: Sequence[str] = ("training_job_id",)

    def __init__(
        self,
        training_job_id: str,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.region = region
        self.project_id = project_id
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.training_job_id = training_job_id

    def execute(self, context: Context):

        model_arts_hook = ModelArtsHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, region=self.region, project_id=self.project_id
        )

        return model_arts_hook.delete_training_job(training_job_id=self.training_job_id)


class ModelArtsStopTrainingJobOperator(BaseOperator):
    """
    This operator used to terminate a training job. Only jobs in the Creating, Waiting, or Running state can be terminated.

    :param training_job_id: ID of a training job.
    :param project_id: Specifies the project ID.
    :param region: Regions where the API is available.
    :param huaweicloud_conn_id: The Airflow connection used for ModelArts credentials.
    """
    template_fields: Sequence[str] = ("training_job_id",)

    def __init__(
        self,
        training_job_id: str,
        action_type: str | None = None,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.region = region
        self.project_id = project_id
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.training_job_id = training_job_id
        self.action_type = action_type

    def execute(self, context: Context):

        model_arts_hook = ModelArtsHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, region=self.region, project_id=self.project_id
        )

        return model_arts_hook.stop_training_job(training_job_id=self.training_job_id, action_type=self.action_type)


class ModelArtsCreateServiceOperator(BaseOperator):
    """
    This operator used to deploy a model as a service.

    :param infer_type: Inference mode, which can be real-time, batch, or edge. real-time indicates a real-time service.
        A model is deployed as a web service and provides real-time test UI and monitoring. The service keeps running.
        batch indicates a batch service, which can perform inference on batch data and automatically stops after data is processed.
        edge indicates an edge service, which uses Intelligent EdgeFabric (IEF) to deploy a model as a web service on an edge node created on IEF.
    :param service_name: Service name, which consists of 1 to 64 characters.
    :param workspace_id: ID of the workspace to which a service belongs. The default value is 0, indicating the default workspace.
    :param schedule: Service scheduling configuration, which can be configured only for real-time services.
        By default, this parameter is not used. Services run for a long time.
    :param cluster_id: Dedicated resource pool ID. By default, this parameter is left blank, indicating that dedicated resource pools are not used.
        When using a dedicated resource pool to deploy services, ensure that the cluster is running properly.
        After this parameter is configured, the network configuration of the cluster is used,
        and the vpc_id parameter does not take effect. If both this parameter and cluster_id in real-time config are configured,
        cluster_id in real-time config is preferentially used.
    :param pool_name: Specifies the ID of the new dedicated resource pool. By default, this parameter is left blank, indicating that the dedicated resource pool is not used.
        This parameter corresponds to the ID of the new resource pool. When using dedicated resource pool to deploy services,
        ensure that the cluster status is normal. If both pool_name in real-time config and pool_name in real-time config are configured,
        pool_name in real-time config is preferred.
    :param vpc_id: ID of the VPC to which a real-time service instance is deployed. By default, this parameter is left blank.
        In this case, ModelArts allocates a dedicated VPC to each user, and users are isolated from each other.
        To access other service components in the VPC of the service instance, set this parameter to the ID of the corresponding VPC.
        Once a VPC is configured, it cannot be modified. If both vpc_id and cluster_id are configured, only the dedicated resource pool takes effect.
    :param description: Service description, which contains a maximum of 100 characters. By default, this parameter is left blank.
    :param security_group_id: Security group. By default, this parameter is left blank.
        This parameter is mandatory if vpc_id is configured. A security group is a virtual firewall that provides secure network
        access control policies for service instances. A security group must contain at least one inbound rule to permit the requests
        whose protocol is TCP, source address is 0.0.0.0/0, and port number is 8080.
    :param subnet_network_id: ID of a subnet. By default, this parameter is left blank. This parameter is mandatory
        if vpc_id is configured. Enter the network ID displayed in the subnet details on the VPC management console.
        A subnet provides dedicated network resources that are isolated from other networks.
    :param config: Model running configurations. If infer_type is batch or edge, you can configure only one model.
        If infer_type is real-time, you can configure multiple models and assign weights based on service requirements.
        However, the versions of multiple models must be unique.
    :param additional_properties: Additional service attribute, which facilitates service management.
    :param project_id: Specifies the project ID.
    :param region: Regions where the API is available.
    :param huaweicloud_conn_id: The Airflow connection used for ModelArts credentials.
    """
    template_fields: Sequence[str] = ("cluster_id",)

    def __init__(
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
        additional_properties: dict | None = None,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.region = region
        self.project_id = project_id
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.infer_type = infer_type
        self.service_name = service_name
        self.workspace_id = workspace_id
        self.schedule = schedule
        self.cluster_id = cluster_id
        self.pool_name = pool_name
        self.vpc_id = vpc_id
        self.description = description
        self.security_group_id = security_group_id
        self.subnet_network_id = subnet_network_id
        self.config = config
        self.additional_properties = additional_properties

    def execute(self, context: Context):

        model_arts_hook = ModelArtsHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, region=self.region, project_id=self.project_id
        )

        return model_arts_hook.create_service(
            infer_type=self.infer_type,
            service_name=self.service_name,
            workspace_id=self.workspace_id,
            schedule=self.schedule,
            cluster_id=self.cluster_id,
            pool_name=self.pool_name,
            vpc_id=self.vpc_id,
            description=self.description,
            security_group_id=self.security_group_id,
            subnet_network_id=self.subnet_network_id,
            config=self.config,
            additional_properties=self.additional_properties
        )


class ModelArtsDeleteServiceOperator(BaseOperator):
    """
    This operator used to delete a model service. You can delete your own services only.

    :param service_id: Service ID. To delete multiple services in a batch, use commas (,) to separate multiple service_id values.
    :param project_id: Specifies the project ID.
    :param region: Regions where the API is available.
    :param huaweicloud_conn_id: The Airflow connection used for ModelArts credentials.
    """

    def __init__(
        self,
        service_id: str,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.region = region
        self.project_id = project_id
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.service_id = service_id

    def execute(self, context: Context):

        model_arts_hook = ModelArtsHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, region=self.region, project_id=self.project_id
        )

        return model_arts_hook.delete_service(service_id=self.service_id)


class ModelArtsUpdateServiceOperator(BaseOperator):
    """
    This operator used to update configurations of a model service. It can also be used to start or stop a service.

    :param service_id: Service ID.
    :param description: Service description, which contains a maximum of 100 characters.
        If this parameter is not configured, the service description is not updated.
    :param schedule: Service scheduling configuration, which can be configured only for real-time services.
        By default, this parameter is not used. Services run for a long time.
    :param config: Service configuration. If this parameter is not configured, the service is not updated.
    :param status: Service status, which can be running or stopped. If this parameter is not configured, the service status is not changed.
        Either status or config can be modified. If both of them are used, modify status only.
    :param additional_properties: Additional service attribute, which facilitates service management.
    :param project_id: Specifies the project ID.
    :param region: Regions where the API is available.
    :param huaweicloud_conn_id: The Airflow connection used for ModelArts credentials.
    """
    template_fields: Sequence[str] = ("service_id",)

    def __init__(
        self,
        service_id: str,
        schedule: list[dict] | None = None,
        description: str | None = None,
        config: list[dict] | None = None,
        status: str | None = None,
        additional_properties: dict | None = None,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.region = region
        self.project_id = project_id
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.service_id = service_id
        self.schedule = schedule
        self.description = description
        self.config = config
        self.status = status
        self.additional_properties = additional_properties

    def execute(self, context: Context):

        model_arts_hook = ModelArtsHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, region=self.region, project_id=self.project_id
        )

        return model_arts_hook.update_service(
            service_id=self.service_id,
            schedule=self.schedule,
            description=self.description,
            config=self.config,
            status=self.status,
            additional_properties=self.additional_properties
        )


class ModelArtsCreateModelOperator(BaseOperator):
    """
    This operator used to import a model. The execution code and model must be uploaded to OBS first.
    By default, the model generated by a training job is stored in OBS.

    :param model_version: Model version in the format of Digit.Digit.Digit.
    Each digit is a one-digit or two-digit positive integer, but cannot start with 0. For example, 01.01.01 is not allowed. Common parameter
    :param source_location: OBS path where the model is located or the SWR image location.
    :param model_type: Model type, which can be TensorFlow, MXNet, Caffe, Spark_MLlib, Scikit_Learn, XGBoost, Image, PyTorch,
    or Template read from the configuration file. Common parameter
    :param model_name: Model name, which consists of 1 to 64 characters. Only letters, digits, hyphens (-), and underscores (_) are allowed. Common parameter.
    :param model_docs: List of model description documents. A maximum of three documents are supported. Common parameter
    :param template: Configuration items in a template. This parameter is mandatory when model_type is set to Template. Template parameter
    :param source_job_version: Version of the source training job. If the model is generated from a training job,
    input this parameter for source tracing. If the model is imported from a third-party meta model,
    leave this parameter blank. This parameter is left blank by default. Non-template parameter
    :param source_copy: Whether to enable image replication. This parameter is valid only when model_type is set to Image. Options:
        true: Default value, indicating that image replication is enabled. After this function is enabled,
        AI applications cannot be rapidly created, and modifying or deleting an image in the SWR source directory will not affect service deployment.
        false: Image replication is not enabled. After this function is disabled, AI applications can be rapidly created,
        but modifying or deleting an image in the SWR source directory will affect service deployment.
    :param initial_config: Character string converted from the model configuration file. Obtain fields such as apis,
        dependencies, input_params, and output_params in the initial_config configuration file. Non-template parameter
    :param execution_code: OBS path for storing the execution code. By default, this parameter is left blank.
        The name of the execution code file is consistently to be customize_service.py. The inference code file must be stored
        in the model directory. This parameter can be left blank.
        Then, the system will automatically identify the inference code in the model directory. Common parameter
    :param source_job_id: ID of the source training job. If the model is generated from a training job,
        input this parameter for source tracing. If the model is imported from a third-party meta model, leave this parameter blank.
        This parameter is left blank by default. Non-template parameter
    :param output_params: Collection of output parameters of a model. By default, this parameter is left blank.
        If the parameters are read from apis in the configuration file, provide only the initial_config field, and this field can be left blank. Non-template parameter
    :param description: Model description that consists of 1 to 100 characters. The following special characters cannot be contained: &!'"<>= Common parameter
    :param runtime: Model runtime environment. Its possible values are determined based on model_type.
    :param model_metrics: Model precision. If the value is read from the configuration file, this parameter can be left blank. Non-template parameter.
    :param source_type: Model source type, which can only be auto, indicating an ExeML model (model download is not allowed).
        If the model is obtained from a training job, leave this parameter blank. This parameter is left blank by default. Non-template parameter
    :param dependencies: Package required for inference code and model. By default, this parameter is left blank. If the package is read from the configuration file, this parameter can be left blank. Non-template parameter.
    :param workspace_id: Workspace ID, which defaults to 0. Common parameter.
    :param model_algorithm: Model algorithm. If the algorithm is read from the configuration file, this parameter can be left blank.
        The value can be predict_analysis, object_detection, or image_classification. Non-template parameter.
    :param apis: All API input and output parameters of the model. If the parameters are parsed from the configuration file,
        this parameter can be left blank. Non-template parameter.
    :param install_type: Deployment type. Only lowercase letters are supported. The value can be real-time, edge, or batch. Default value: [real-time, edge, batch].
    :param input_params: Collection of input parameters of a model. By default, this parameter is left blank.
        If the parameters are read from apis in the configuration file, provide only the initial_config field, and this field can be left blank. Non-template parameter.
    :param project_id: Specifies the project ID.
    :param region: Regions where the API is available.
    :param huaweicloud_conn_id: The Airflow connection used for ModelArts credentials.
    """

    def __init__(
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
        input_params: list[dict] | None = None,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.model_version = model_version
        self.source_location = source_location
        self.model_type = model_type
        self.model_name = model_name
        self.model_docs = model_docs
        self.template = template
        self.source_job_version = source_job_version
        self.source_copy = source_copy
        self.initial_config = initial_config
        self.execution_code = execution_code
        self.source_job_id = source_job_id
        self.output_params = output_params
        self.description = description
        self.runtime = runtime
        self.model_metrics = model_metrics
        self.source_type = source_type
        self.dependencies = dependencies
        self.workspace_id = workspace_id
        self.model_algorithm = model_algorithm
        self.apis = apis
        self.install_type = install_type
        self.input_params = input_params
        self.region = region
        self.project_id = project_id
        self.huaweicloud_conn_id = huaweicloud_conn_id

    def execute(self, context: Context):

        model_arts_hook = ModelArtsHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, region=self.region, project_id=self.project_id
        )

        return model_arts_hook.create_model(
            model_version=self.model_version,
            source_location=self.source_location,
            model_type=self.model_type,
            model_name=self.model_name,
            model_docs=self.model_docs,
            template=self.template,
            source_job_version=self.source_job_version,
            source_copy=self.source_copy,
            initial_config=self.initial_config,
            execution_code=self.execution_code,
            source_job_id=self.source_job_id,
            output_params=self.output_params,
            description=self.description,
            runtime=self.runtime,
            model_metrics=self.model_metrics,
            source_type=self.source_type,
            dependencies=self.dependencies,
            workspace_id=self.workspace_id,
            model_algorithm=self.model_algorithm,
            apis=self.apis,
            install_type=self.install_type,
            input_params=self.input_params
        )


class ModelArtsDeleteModelOperator(BaseOperator):
    """
    This operator used to delete a model based on the model ID

    :param model_id: Specifies the model ID.
    :param project_id: Specifies the project ID.
    :param region: Regions where the API is available.
    :param huaweicloud_conn_id: The Airflow connection used for ModelArts credentials.
    """
    template_fields: Sequence[str] = ("model_id",)

    def __init__(
        self,
        model_id: str,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.region = region
        self.project_id = project_id
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.model_id = model_id

    def execute(self, context: Context):

        model_arts_hook = ModelArtsHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, region=self.region, project_id=self.project_id
        )

        return model_arts_hook.delete_model(model_id=self.model_id)
