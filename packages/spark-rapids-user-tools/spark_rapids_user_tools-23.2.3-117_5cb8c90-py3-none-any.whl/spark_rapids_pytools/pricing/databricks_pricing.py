# Copyright (c) 2023, NVIDIA CORPORATION.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""providing absolute costs of resources in Databricks"""

from dataclasses import dataclass, field

from spark_rapids_pytools.common.prop_manager import JSONPropertiesContainer
from spark_rapids_pytools.common.sys_storage import FSUtil
from spark_rapids_pytools.common.utilities import Utils
from spark_rapids_pytools.pricing.emr_pricing import EMREc2PriceProvider


@dataclass
class DatabricksCatalogContainer(JSONPropertiesContainer):
    def _init_fields(self) -> None:
        pass


@dataclass
class DatabricksPriceProvider(EMREc2PriceProvider):
    """
    Provide costs of Databricks instances
    """
    name = 'Databricks'
    plan: str = field(default='databricks-premium', init=False)  # standard, premium (default), or enterprise
    # TODO: current default to 'premium' plan and 'Jobs Compute' compute type,
    # need to figure out how to find these values from cluster properties

    def _generate_cache_files(self):
        src_file_path = Utils.resource_path(f'{self.plan}-catalog.json')
        FSUtil.cache_resource(src_file_path, self.cache_files[self.plan])
        super()._generate_cache_files()

    def _process_resource_configs(self):
        online_entries = self.pricing_configs['databricks'].get_value('catalog', 'onlineResources')
        for online_entry in online_entries:
            file_name = online_entry.get('localFile')
            file_key = online_entry.get('resourceKey').split('-catalog')[0]
            if file_key == self.plan or 'databricks' not in file_key:
                self.cache_files[file_key] = FSUtil.build_path(self.cache_directory, file_name)
            if 'databricks' not in file_key:
                self.resource_urls[file_key] = online_entry.get('onlineURL')

    def _create_catalogs(self):
        super()._create_catalogs()
        for file_key, cache_file in self.cache_files.items():
            if 'ec2' not in file_key:
                self.catalogs[file_key] = DatabricksCatalogContainer(prop_arg=cache_file)

    def get_ssd_price(self, machine_type: str) -> float:
        pass

    def get_ram_price(self, machine_type: str) -> float:
        pass

    def get_gpu_price(self, gpu_device: str) -> float:
        pass

    def get_cpu_price(self, machine_type: str) -> float:
        pass

    def get_container_cost(self) -> float:
        pass

    def get_cores_count_for_vm(self, machine_type: str) -> str:
        pass

    def get_ram_size_for_vm(self, machine_type: str) -> str:
        pass

    def get_instance_price(self, instance, compute_type: str = 'Jobs Compute') -> float:
        # the cost of an instance is amount of DBU * JOB_type-rate-per-hour
        job_type_conf = self.catalogs[self.plan].get_value(compute_type)
        rate_per_hour = job_type_conf.get('RatePerHour')
        instance_conf = job_type_conf.get('Instances').get(instance)
        instance_dbu = instance_conf.get('DBU')
        return instance_dbu * rate_per_hour
