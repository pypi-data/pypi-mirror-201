from msb_cipher import Cipher
from msb_dataclasses import Singleton
from msb_dataclasses.search_parameter import SearchParameter
from msb_db.models import (MsbModel)
from msb_db import (DEFAULT_QUERY_LIMIT, DEFAULT_QUERY_OFFSET)
from msb_exceptions import CustomExceptionHandler
from ._exceptions import ApiServiceExceptions
from django.db.models.query import QuerySet


class ApiService(CustomExceptionHandler, metaclass=Singleton):
	db_model = MsbModel
	resource_name: str = None

	@property
	def resource_name_value(self) -> str | None:
		try:
			if not self.resource_name:
				import re
				class_name = re.split('(?<=.)(?=[A-Z])', self.__class__.__name__.replace("Service", ""))
				return " ".join(class_name)
			return self.resource_name
		except Exception:
			return None

	@property
	def cipher(self):
		return Cipher

	def __decrypt(self, data):
		return Cipher.decrypt(data=data)

	def __init__(self):
		if self.db_model is None:
			raise ApiServiceExceptions.InvalidDatabaseModel(resource=self.resource_name_value)

	def search(self, params: SearchParameter) -> QuerySet:
		try:
			model_query = params.get_query(self.db_model)
			return model_query.all()[params.offset:params.offset + params.limit]
		except Exception:
			return QuerySet()

	def create(self, *model_data_list) -> bool:
		try:
			create_status = False
			if len(model_data_list) == 0:
				raise ApiServiceExceptions.InvalidDataForCreateOperation(resource=self.resource_name_value)

			if len(model_data_list) == 1:
				model_data = model_data_list[0]
				_model = self.db_model(**model_data)
				_model.save()
				create_status = True
			else:
				create_status = self.db_model.objects.bulk_create(
					[self.db_model(**model_data) for model_data in model_data_list]
				)
				create_status = True
		except Exception:
			raise ApiServiceExceptions.CreateOperationFailed(resource=self.resource_name_value)
		return create_status

	def retrieve(self, pk=None, silent=True):
		try:
			if pk is None:
				raise ApiServiceExceptions.InvalidPk(resource=self.resource_name_value)
			return self.db_model.objects.get(pk=pk)
		except Exception:
			if not silent:
				raise ApiServiceExceptions.RetrieveOperationFailed(resource=self.resource_name_value)
			return None

	def list(self, limit: int = None, offset: int = None) -> QuerySet:
		try:
			offset = offset if isinstance(offset, int) else DEFAULT_QUERY_OFFSET
			limit = limit if isinstance(limit, int) else DEFAULT_QUERY_LIMIT

			fields = [
				i for i in self.db_model._list_field_names
				if (x := getattr(self.db_model, i, None)) and not isinstance(x, property)
			]
			data_set = self.db_model.objects.only(*fields).all()[offset:limit] if len(fields) > 0 else None
			return data_set
		except Exception as e:
			raise ApiServiceExceptions.ListOperationFailed(resource=self.resource_name_value)

	def update(self, pk=None, **model_data) -> bool:
		try:
			status = False
			if (pk := self.__decrypt(pk)) is None:
				raise ApiServiceExceptions.InvalidPk(resource=self.resource_name_value)
			model_object = self.db_model.objects.filter(pk=pk)
			if model_object and not (status := model_object.update(**model_data)):
				raise ApiServiceExceptions.UpdateOperationFailed(resource=self.resource_name_value)
			return bool(status)
		except Exception as e:
			raise ApiServiceExceptions.UpdateOperationFailed(resource=self.resource_name_value)

	def delete(self, pk=None) -> bool:
		try:
			status = False

			if (pk := self.__decrypt(pk)) is None:
				raise ApiServiceExceptions.InvalidPk(resource=self.resource_name_value)
			model_object = self.db_model.objects.get(pk=pk)

			if model_object and not (status := model_object.delete()):
				raise ApiServiceExceptions.DeleteOperationFailed(resource=self.resource_name_value)
			return bool(status)
		except Exception as e:
			raise ApiServiceExceptions.DeleteOperationFailed(resource=self.resource_name_value)
