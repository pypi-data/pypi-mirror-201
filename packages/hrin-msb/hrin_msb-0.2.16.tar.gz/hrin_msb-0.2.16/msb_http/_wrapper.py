from json import dump as json_dump
from typing import (List, Dict)

from ._client import ApiRequestClient
from ._dataclasses import (ApiRequestData, MsbApiResponse, RestRequest)


class ApiRouter(ApiRequestData):

	def _get_payload(self, request: RestRequest):
		if self.method.lower() in ['get']:
			return None

		return json_dump((request.data if type(request.data) in [list, dict] else {}))

	def __init__(self, request: RestRequest):
		super(ApiRouter, self).__init__(request=request)
		self.set_request_method(request.method)
		self.set_data(self._get_payload(request))


class MsbIntraServiceRequest:
	service_host: str = ''
	__api_request: ApiRequestClient

	def __init__(self, request: RestRequest = None, version: int = 1):
		self.__api_request = ApiRequestClient(api_host=self.service_host, request=request)

	def __execute(self):
		api_response = self.__api_request.get_result()
		return api_response.as_msb_api_response()

	@property
	def request(self) -> ApiRequestClient:
		return self.__api_request

	def retrieve(self, endpoint: str, pk: str) -> MsbApiResponse:
		self.__api_request.set_endpoint(endpoint=endpoint).GET(query_params=[pk])
		return self.__execute()

	def list(self, endpoint: str, limit: int = -1, offset: int = 0) -> MsbApiResponse:
		self.__api_request.set_endpoint(endpoint=endpoint).GET(query_params=dict(limit=limit, offset=offset))
		return self.__execute()

	def create(self, endpoint: str, data: [List | Dict] = None) -> MsbApiResponse:
		self.__api_request.set_endpoint(endpoint=endpoint).POST(data=data)
		return self.__execute()

	def search(self, endpoint: str, params: dict) -> MsbApiResponse:
		endpoint = f"{endpoint.strip('/')}/search"
		data = params.__dict__
		self.__api_request.set_endpoint(endpoint=endpoint).POST(data=data)
		return self.__execute()

	def update(self, endpoint: str, pk: str, data: Dict = None) -> MsbApiResponse:
		self.__api_request.set_endpoint(endpoint=endpoint).PUT(data=data, query_params=[pk])
		return self.__execute()

	def bulk_update(self, endpoint: str, data: List[Dict] = None) -> MsbApiResponse:
		self.__api_request.set_endpoint(endpoint=endpoint).PUT(data=data)
		return self.__execute()

	def delete(self, endpoint: str, pk: str) -> MsbApiResponse:
		self.__api_request.set_endpoint(endpoint=endpoint).POST(query_params=[pk])
		return self.__execute()

	def bulk_delete(self, endpoint: str, data: List[Dict]) -> MsbApiResponse:
		self.__api_request.set_endpoint(endpoint=endpoint).POST(data=data)
		return self.__execute()
