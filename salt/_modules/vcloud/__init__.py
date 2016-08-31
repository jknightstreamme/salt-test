import time
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery

_instance_list = []


def _get_instance_list(service, project):
    """Caching interface for instance list"""
    global _instance_list
    if not _instance_list:
        _instance_list = _gcloud_list_instances(service=service,
                                                project=project)
    return _instance_list


def _gcloud_start_instance(service, project, instance_name):
    instances = _get_instance_list(service, project)
    for i in instances:
        if i['name'] == instance_name:
            zone_name = i['zone'][str(i['zone']).rfind('/')+1:]
            request = service.instances().start(project=project,
                                                zone=zone_name,
                                                instance=instance_name)
            resp = request.execute()
            return _wait_for_operation(service, project, zone_name,
                                       operation=resp['name'])


def _gcloud_stop_instance(service, project, instance_name):
    instances = _get_instance_list(service, project)
    for i in instances:
        if i['name'] == instance_name:
            zone_name = i['zone'][str(i['zone']).rfind('/')+1:]
            request = service.instances().stop(project=project,
                                               zone=zone_name,
                                               instance=instance_name)
            resp = request.execute()
            return _wait_for_operation(service, project, zone_name,
                                       operation=resp['name'])


def _gcloud_list_instances(service, project):
    instance_list = []
    instances = service.instances()
    request = instances.aggregatedList(project=project)
    while request is not None:
        response = request.execute()

        for zone, instances_scoped_list in response['items'].items():
            for instance in instances_scoped_list.get('instances', []):
                instance_data = {'name': instance['name'],
                                 'status': instance['status'],
                                 'zone': instance['zone']}
                instance_list.append(instance_data)

        request = instances.aggregatedList_next(previous_request=request,
                                                previous_response=response)

    return instance_list


def _gcloue_list_zones(service, project):
    zone_list = []
    zones = service.zones()
    zone_req = zones.list(project=project)

    while zone_req is not None:
        resp = zone_req.execute()

        for zone in resp['items']:
            zone_list.append(zone)

        zone_req = zones.list_next(previous_request=zone_req,
                                   previous_response=resp)

    return zone_list


def _wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result

        time.sleep(1)


def start(instance, project):
    credentials = GoogleCredentials.get_application_default()
    compute = discovery.build('compute', 'v1', credentials=credentials)
    _gcloud_start_instance(compute, project, instance)


def stop(instance, project):
    credentials = GoogleCredentials.get_application_default()
    compute = discovery.build('compute', 'v1', credentials=credentials)
    _gcloud_stop_instance(compute, project, instance)
