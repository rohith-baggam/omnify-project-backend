from django.db.models.query import QuerySet
from rest_framework.request import Request
from typing import Dict


class SerializerUtils:
    request: Request
    payload: Dict
    queryset: QuerySet

    def __init__(self, request: Request, payload: Dict):
        self.request = request

    def validate(self, data):
        data["is_valid"] = True
        data["error_message"] = {}
        return self.payload

    def create(self, validated_data):
        return validated_data
