
from formant.sdk.cloud.v2.src.resources.resources import Resources
from formant.sdk.cloud.v2.formant_query_api_client.api.count import count_controller_history, count_controller_active_devices
from formant.sdk.cloud.v2.formant_query_api_client.models.count_history_query import CountHistoryQuery
from formant.sdk.cloud.v2.formant_query_api_client.models.active_devices_query import ActiveDevicesQuery

class Count(Resources):

    def history(self, count_history_query: CountHistoryQuery):
        'Gets all the objects(of given type) during the timestamp'
        client = self._get_client()
        response = count_controller_history.sync_detailed(client=client, json_body=count_history_query)
        return response

    async def history_async(self, count_history_query: CountHistoryQuery):
        'Gets all the objects(of given type) during the timestamp'
        client = self._get_client()
        response = (await count_controller_history.asyncio_detailed(client=client, json_body=count_history_query))
        return response

    def active_devices(self, active_devices_query: ActiveDevicesQuery):
        'Gets all the active devices during the timestamp'
        client = self._get_client()
        response = count_controller_active_devices.sync_detailed(client=client, json_body=active_devices_query)
        return response

    async def active_devices_async(self, active_devices_query: ActiveDevicesQuery):
        'Gets all the active devices during the timestamp'
        client = self._get_client()
        response = (await count_controller_active_devices.asyncio_detailed(client=client, json_body=active_devices_query))
        return response
