"""Contains utility functions for calling the Official Kubernetes API
"""
import logging
import json
import copy
import random
import time
import collections
from kubernetes import client
from kubernetes.client.rest import ApiException
from google.cloud import filestore_v1
logger = logging.getLogger(__name__)


def get_api_sleep(attempt):
    temp = 4 * 2 ** attempt
    return int(temp / 2) + random.randrange(0, temp/2)


def api_request(api_func, *args, **kwargs):
    """Sends an API request by calling api_func(*args, **kwargs) and catches the ApiException, if any.

    Args:
        api_func: A function/method/callable object that uses functions from the Kubernetes API package
        *args: Arguments for calling api_func.
        **kwargs: Keyword arguments for calling api_func.

    Returns: The response of calling api_func, most likely a dictionary.
        If an error occurs, the response will be a dictionary containing the following keys:
            status, the status returned in the ApiException
            error, the reason of the error
            headers, the header of the ApiException

    """
    try:
        response = api_func(*args, **kwargs)
        # Convert the response to dictionary if possible
        if hasattr(response, "to_dict"):
            response = response.to_dict()
    except ApiException as e:
        logger.debug("Exception when calling %s: %s" % (api_func.__name__, e))
        response = {
            "status": e.status,
            "error": e.reason,
            "headers": stringify(e.headers),
        }
        response.update(json.loads(e.body))
    return response


def delete_filestore_instance(name):
    # Create a client
    client = filestore_v1.CloudFilestoreManagerClient()

    # Initialize request argument(s)
    request = filestore_v1.DeleteInstanceRequest(
        name=f"projects/davelab-gcloud/locations/us-east1-b/instances/{name}"
    )

    # Make the request
    op_timer = time.time()
    operation = client.delete_instance(request=request)

    logging.info("Waiting for filestore deletion operation to complete...")

    response = operation.result()
    diff = time.time() - op_timer

    logging.info(f"Filestore Instance deleted in {diff:.3f} secs")


def create_volume_claim(name, namespace, storage, core_api, storage_class="standard-fc", access_modes=['ReadWriteOnce'], volume_name=None):
    if not storage:
        storage = "10"
    pvc_meta = client.V1ObjectMeta(name=name, namespace=namespace)
    pvc_resources = client.V1ResourceRequirements(requests={'storage': str(storage)+'Gi'})
    pvc_spec = client.V1PersistentVolumeClaimSpec(access_modes=access_modes, resources=pvc_resources, storage_class_name=storage_class)
    if volume_name:
        pvc_spec.volume_name = volume_name
    volume_claim = client.V1PersistentVolumeClaim(metadata=pvc_meta, spec=pvc_spec)
    created = False

    for i in range(10):
        try:
            pvc_response = api_request(core_api.list_namespaced_persistent_volume_claim, namespace)
            pvc_list = [x["metadata"]["name"] for x in pvc_response["items"]] if pvc_response and "items" in pvc_response else []
            if name in pvc_list:
                logging.debug(f"({name}) Persistent Volume Claim already exists, continue.")
                created = True
                break
            pvc_response = api_request(core_api.create_namespaced_persistent_volume_claim, namespace, volume_claim)
        except Exception as e:
            raise RuntimeError(f"({name}) Failure to create the Persistent Volume Claim on the cluster. Reason: {str(e)}")

        pvc_status = pvc_response.get("status", None)
        if pvc_status and isinstance(pvc_status, dict):
            logging.debug(f"({name}) Persistent Volume Claim created.")
            created = True
            break
        else:
            if 'Connection aborted' in str(pvc_response) or 'Connection reset' in str(pvc_response):
                sleep_time = get_api_sleep(i+1)
                logging.debug(f"({name}) Connection issue when creating Persistent Volume Claim. Sleeping for: {sleep_time}")
                time.sleep(sleep_time)
                continue
            elif 'Conflict' in str(pvc_response):
                logging.debug(f"({name}) Persistent Volume Claim already exists, continue.")
                created = True
                break
            else:
                raise RuntimeError(f"({name}) Failure to create a Persistent Volume Claim on the cluster. Response: {str(pvc_response)}")
    return created


def create_volume(name, namespace, storage, core_api, storage_class="standard-fc", access_modes=['ReadWriteOnce'], ip_address=None, path=None):
    if not storage:
        storage = "10Gi"
    # storage = parse_storage_text(storage)
    pv_meta = client.V1ObjectMeta(name=name, namespace=namespace)
    nfs_config = {}
    if ip_address:
        nfs_config = client.V1NFSVolumeSource(path=path, server=ip_address)
    pv_spec = client.V1PersistentVolumeSpec(access_modes=access_modes, capacity={"storage": storage}, nfs=nfs_config, storage_class_name=storage_class)
    volume = client.V1PersistentVolume(metadata=pv_meta, spec=pv_spec)
    created = False

    for i in range(10):
        try:
            pv_response = api_request(core_api.list_persistent_volume)
            pv_list = [x["metadata"]["name"] for x in pv_response["items"]] if pv_response and "items" in pv_response else []
            if name in pv_list:
                logging.debug(f"({name}) Persistent Volume already exists, continue.")
                created = True
                break
            pv_response = api_request(core_api.create_persistent_volume, volume)
        except Exception as e:
            raise RuntimeError(f"({name}) Failure to create the Persistent Volume on the cluster. Reason: {str(e)}")

        pv_status = pv_response.get("status", None)
        if pv_status and isinstance(pv_status, dict):
            logging.debug(f"({name}) Persistent Volume Claim created.")
            created = True
            break
        else:
            if 'Connection aborted' in str(pv_response) or 'Connection reset' in str(pv_response):
                sleep_time = get_api_sleep(i+1)
                logging.debug(f"({name}) Connection issue when creating Persistent Volume. Sleeping for: {sleep_time}")
                time.sleep(sleep_time)
                continue
            elif 'Conflict' in str(pv_response):
                logging.debug(f"({name}) Persistent Volume already exists, continue.")
                created = True
                break
            else:
                raise RuntimeError(f"({name}) Failure to create a Persistent Volume on the cluster. Response: {str(pv_response)}")
    return created


def create_filestore_instance(name, capacity=1024, core_api=None, storage_class="filestore-hdd", namespace="default", vol_name=None, vol_capacity=1024, vol_claim_name=None):
    # Create a client
    client = filestore_v1.CloudFilestoreManagerClient()

    inst_request = filestore_v1.GetInstanceRequest(name=f"projects/davelab-gcloud/locations/us-east1-b/instances/{name}")
    response = None
    try:
        response = client.get_instance(inst_request)
    except BaseException as e:
        logging.info(f"Filestore Instance {name} does not exist. Creating now.")

    if not response:
        instance = filestore_v1.Instance(
            tier=filestore_v1.Instance.Tier.BASIC_HDD,
            file_shares=[filestore_v1.FileShareConfig(name=name.replace("-", "_"), capacity_gb=capacity)],
            networks=[filestore_v1.NetworkConfig(network="davelab-private")]
        )

        # Initialize request argument(s)
        request = filestore_v1.CreateInstanceRequest(
            parent="projects/davelab-gcloud/locations/us-east1-b",
            instance_id=name,
            instance=instance
        )

        # Make the request
        op_timer = time.time()
        operation = client.create_instance(request=request)

        logging.info("Waiting for filestore creation operation to complete...")

        response = operation.result()
        diff = time.time() - op_timer

        # Handle the response
        logging.info(f"Filestore Instance created in {diff:.3f} secs")

    if vol_name:
        logging.info(f"Creating persistent volume for new filestore instance")
        ip_address = response.networks[0].ip_addresses[0]
        fs_name = response.file_shares[0].name
        # create volume
        vol_created = create_volume(vol_name, namespace, f"{vol_capacity}Gi", core_api, storage_class, ['ReadWriteMany'], ip_address, f"/{fs_name}")
        vol_name = vol_name if vol_created else None
        if vol_created and vol_claim_name:
            vc_created = create_volume_claim(vol_claim_name, namespace, vol_capacity, core_api, storage_class, ['ReadWriteMany'], vol_name)
            vol_claim_name = vol_claim_name if vc_created else None

    return response, vol_name, vol_claim_name


# This function is from the Aries package.
def stringify(obj):
    """Convert object to string.
    If the object is a dictionary-like object or list,
    the objects in the dictionary or list will be converted to strings, recursively.

    Returns: If the input is dictionary or list, the return value will also be a list or dictionary.

    """
    if isinstance(obj, collections.Mapping):
        obj = copy.deepcopy(obj)
        obj_dict = {}
        for key, value in obj.items():
            obj_dict[key] = stringify(value)
        return obj_dict
    elif isinstance(obj, list):
        str_list = []
        for item in obj:
            str_list.append(stringify(item))
        return str_list
    else:
        try:
            json.dumps(obj)
            return obj
        except TypeError:
            return str(obj)


def get_dict_value(dictionary, *keys, default=None):
    d = dictionary
    for key in keys:
        if key not in d:
            return default
        d = d.get(key, dict())
    return d
