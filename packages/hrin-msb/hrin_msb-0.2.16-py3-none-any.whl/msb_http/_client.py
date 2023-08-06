from typing import (List, Dict, Self)

from requests.models import Response

from ._dataclasses import (ApiRequestData, ApiResponseWrapper)
from ._utils import make_api_request


class ApiRequestClient(ApiRequestData):

	@property
	def request_is_json(self) -> bool:
		return True

	def GET(self, query_params: [List | Dict] = None, ) -> Self:
		return self.set_query_params(params=query_params).set_request_method("GET")

	def POST(self, data: [List | Dict] = None, query_params: [List | Dict] = None) -> Self:
		return self.set_data(data=data).set_query_params(params=query_params).set_request_method("POST")

	def PUT(self, data: [List | Dict] = None, query_params: [List | Dict] = None) -> Self:
		return self.set_data(data=data).set_query_params(params=query_params).set_request_method("PUT")

	def DELETE(self, data: [List | Dict] = None, query_params: [List | Dict] = None) -> Self:
		return self.set_data(data=data).set_query_params(params=query_params).set_request_method("DELETE")

	def get_result(self) -> ApiResponseWrapper:
		try:
			_response = make_api_request(self)
		except Exception as e:
			_response = Response()
		return ApiResponseWrapper(_response)
