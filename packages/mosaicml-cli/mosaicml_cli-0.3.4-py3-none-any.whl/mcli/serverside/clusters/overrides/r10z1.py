""" R10Z1 Cluster Definition """
from typing import Dict, List, Optional, Set

from mcli.serverside.clusters.cluster import GenericK8sCluster
from mcli.serverside.clusters.cluster_instances import InstanceGPUConfiguration, Instances, LocalInstances
from mcli.serverside.clusters.gpu_type import GPUType
from mcli.serverside.clusters.instance_type import InstanceType
from mcli.utils.utils_kube_labels import label

NUM_NODES = 128

a100_config = InstanceGPUConfiguration(
    gpu_type=GPUType.A100_40GB,
    gpu_nums=[8 * n for n in range(1, NUM_NODES + 1)],
    gpu_selectors={},
    cpus=64,
    cpus_per_gpu=8,
    memory=2048,
    memory_per_gpu=256,
    storage=8000,
    storage_per_gpu=1000,
    multinode_rdma_roce=1,
)

cpu_config = InstanceGPUConfiguration(
    gpu_type=GPUType.NONE,
    gpu_nums=[0],
)

R10Z1_INSTANCES = LocalInstances(gpu_configurations=[a100_config, cpu_config])

PARTITION_SELECTOR_MAP = {
    '1': label.mosaic.instance_size_types.OCI_GB4_8,
    '2': label.mosaic.instance_size_types.OCI_GD4_8
}


class R10Z1Cluster(GenericK8sCluster):
    """ R10Z1 Cluster Overrides """

    allowed_instances: Instances = R10Z1_INSTANCES

    pod_group_scheduler: Optional[str] = 'scheduler-plugins-scheduler'
    privileged: bool = True
    interactive: bool = True
    partitions: Optional[Set[str]] = set(PARTITION_SELECTOR_MAP)

    def get_selectors(self,
                      instance_type: InstanceType,
                      partitions: Optional[List[str]] = None) -> Dict[str, List[str]]:

        selectors = super().get_selectors(instance_type, partitions)

        instance_selectors = []
        if partitions is not None:
            # Any invalid partitions should be flagged to user in call to `super`
            instance_selectors = [PARTITION_SELECTOR_MAP[pp] for pp in partitions if pp in PARTITION_SELECTOR_MAP]
        elif instance_type.gpu_type is not GPUType.NONE:
            # If no partitions provided, use any gpu selector as long as not requesting cpu instance
            instance_selectors = list(PARTITION_SELECTOR_MAP.values())

        if instance_selectors:
            selectors[label.mosaic.cloud.INSTANCE_SIZE] = instance_selectors

        return selectors
