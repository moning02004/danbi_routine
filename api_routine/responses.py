from rest_framework.response import Response

from api_routine.constants import (ROUTINE_RESULT_UPDATE_STATUS, ROUTINE_LIST_MESSAGE, ROUTINE_LIST_STATUS,
                                   ROUTINE_CREATE_MESSAGE, ROUTINE_DETAIL_MESSAGE, ROUTINE_DETAIL_STATUS,
                                   ROUTINE_UPDATE_MESSAGE, ROUTINE_UPDATE_STATUS, ROUTINE_DELETE_MESSAGE,
                                   ROUTINE_DELETE_STATUS, ROUTINE_RESULT_UPDATE_MESSAGE, ROUTINE_CREATE_STATUS)


class RoutineResponseModelMixin:
    message = None
    status = None

    def __init__(self, response: Response = None):
        self.response = response

    def get_response_data(self):
        return self.response.data

    def get_response_data_of_id(self):
        return {
            "id": self.response.data["routine_id"]
        }

    def get_response(self):
        self.response.data = {
            "data": self.get_response_data(),
            "message": {
                "msg": self.message,
                "status": self.status
            }
        }
        return self.response


class RoutineListResponseModel(RoutineResponseModelMixin):
    message = ROUTINE_LIST_MESSAGE
    status = ROUTINE_LIST_STATUS


class RoutineCreateResponseModel(RoutineResponseModelMixin):
    message = ROUTINE_CREATE_MESSAGE
    status = ROUTINE_CREATE_STATUS

    def get_response_data(self):
        return {
            "id": self.response.data["routine_id"]
        }


class RoutineRetrieveResponseModel(RoutineResponseModelMixin):
    message = ROUTINE_DETAIL_MESSAGE
    status = ROUTINE_DETAIL_STATUS


class RoutineUpdateResponseModel(RoutineResponseModelMixin):
    message = ROUTINE_UPDATE_MESSAGE
    status = ROUTINE_UPDATE_STATUS

    def get_response_data(self):
        return self.get_response_data_of_id()


class RoutineDeleteResponseModel(RoutineResponseModelMixin):
    message = ROUTINE_DELETE_MESSAGE
    status = ROUTINE_DELETE_STATUS

    def get_response_data(self):
        return self.get_response_data_of_id()


class RoutineResultResponseModel(RoutineResponseModelMixin):
    message = ROUTINE_RESULT_UPDATE_MESSAGE
    status = ROUTINE_RESULT_UPDATE_STATUS

    def get_response_data(self):
        return self.get_response_data_of_id()
