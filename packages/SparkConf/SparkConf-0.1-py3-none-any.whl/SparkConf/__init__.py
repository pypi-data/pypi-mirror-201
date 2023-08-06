import boto3

def describe_instance(worker_instance_type: str):
    client = boto3.client('ec2', region_name = 'us-west-2')

    response = client.describe_instance_types(
        DryRun=False,
        InstanceTypes = [worker_instance_type]
    )


    #worker_node_virtual_core = response["InstanceTypes"][0]["VCpuInfo"]["DefaultVCpus"]
    worker_node_virtual_core = response["InstanceTypes"][0]["VCpuInfo"]["DefaultCores"]
    worker_node_memory = response["InstanceTypes"][0]["MemoryInfo"]["SizeInMiB"]

    return worker_node_virtual_core, worker_node_memory


def spark_conf(worker_instance_type: str):
    worker_node_virtual_core, worker_node_memory = describe_instance(worker_instance_type)

    if worker_node_virtual_core >= 8:
        spark_executor_cores = 5

        #number of executors per instance = (total number of virtual cores per instance - 1)/ spark.executors.cores
        no_of_executors_per_instance = round((worker_node_virtual_core - 1) / spark_executor_cores)

        #spark.executors.memory = total RAM per instance * 0.9 / number of executors per instance
        spark_executor_memory = str(round(((worker_node_memory * 0.9) / no_of_executors_per_instance)/1000)) + "g"
    else:
        spark_executor_cores = worker_node_virtual_core
        spark_executor_memory = str(worker_node_memory) + "m"

    spark_driver_cores = spark_executor_cores
    spark_driver_memory = spark_executor_memory
    spark_memory_fraction =0.8
    spark_memory_storageFraction = 0.2
    spark_memory_offHeap_enabled = False

    return spark_executor_cores, spark_driver_cores, spark_executor_memory, spark_driver_memory, spark_memory_fraction, spark_memory_storageFraction, spark_memory_offHeap_enabled