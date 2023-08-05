from setuptools.config.setupcfg import read_configuration as c;

__name__ = (c("setup.cfg")["metadata"]["name"])
__version__ = (c("setup.cfg")["metadata"]["version"])


def get_provider_info():
    return {
        "package-name": __name__,  # Required
        "name": "Huawei Cloud Apache Airflow Provider",
        "description": "Huawei Cloud Apache Airflow Provider",
        "connection-types": [
            {
                "connection-type": "huaweicloud",
                "hook-class-name": "huawei_cloud_provider.hooks.base_huawei_cloud.HuaweiBaseHook",
            }
        ],
        "versions": [__version__],
    }
