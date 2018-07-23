from collections import OrderedDict

from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from rest_framework import serializers, status

from .search import is_search_view

TYPE_TO_FIELDMAPPING = {
    openapi.TYPE_INTEGER: serializers.IntegerField,
    openapi.TYPE_NUMBER: serializers.FloatField,
    openapi.TYPE_STRING: serializers.CharField,
    openapi.TYPE_BOOLEAN: serializers.BooleanField,
}


class AutoSchema(SwaggerAutoSchema):

    @property
    def model(self):
        qs = self.view.get_queryset()
        return qs.model

    @property
    def _is_search_view(self):
        return is_search_view(self.view)

    def get_operation_id(self, operation_keys):
        """
        Simply return the model name as lowercase string, postfixed with the operation name.
        """
        action = operation_keys[-1]
        model_name = self.model._meta.model_name
        return f"{model_name}_{action}"

    def should_page(self):
        if self._is_search_view:
            return hasattr(self.view, 'paginator')
        return super().should_page()

    def get_request_serializer(self):
        if not self._is_search_view:
            return super().get_request_serializer()

        Base = self.view.get_search_input_serializer_class()

        filter_fields = []
        for filter_backend in self.view.filter_backends:
            filter_fields += self.probe_inspectors(
                self.filter_inspectors,
                'get_filter_parameters', filter_backend()
            ) or []

        filters = {}
        for filter_field in filter_fields:
            FieldClass = TYPE_TO_FIELDMAPPING[filter_field.type]
            filters[filter_field.name] = FieldClass(
                help_text=filter_field.description,
                required=filter_field.required
            )

        SearchSerializer = type(Base.__name__, (Base,), filters)
        return SearchSerializer()

    def get_default_responses(self):
        if self._is_search_view:
            response_status = status.HTTP_200_OK
            response_schema = self.serializer_to_schema(self.get_view_serializer())
            schema = openapi.Schema(type=openapi.TYPE_ARRAY, items=response_schema)
            if self.should_page():
                schema = self.get_paginated_response(schema) or schema
            return OrderedDict({str(response_status): schema})
        return super().get_default_responses()
