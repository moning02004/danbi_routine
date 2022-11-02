from rest_framework.renderers import JSONRenderer

from api_routine.constants import (ROUTINE_RESULT_UPDATE_STATUS, ROUTINE_LIST_MESSAGE, ROUTINE_LIST_STATUS,
                                   ROUTINE_CREATE_MESSAGE, ROUTINE_DETAIL_MESSAGE, ROUTINE_DETAIL_STATUS,
                                   ROUTINE_UPDATE_MESSAGE, ROUTINE_UPDATE_STATUS, ROUTINE_DELETE_MESSAGE,
                                   ROUTINE_DELETE_STATUS, ROUTINE_RESULT_UPDATE_MESSAGE, ROUTINE_CREATE_STATUS)


class RoutineResponseModelMixin(JSONRenderer):
    message = None
    status = None
    response_data = None

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context["response"]
        if str(response.status_code).startswith("4"):
            return super().render(data, accepted_media_type=None, renderer_context=None)

        self.response_data = response.data
        data = {
            "data": self.get_response_data(),
            "message": {
                "msg": self.message,
                "status": self.status
            }
        }
        response.data = data
        return super().render(data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)

    def get_response_data(self):
        return self.response_data

    def get_response_data_of_id(self):
        return {
            "routine_id": self.response_data["routine_id"]
        }


class RoutineListResponseModel(RoutineResponseModelMixin):
    message = ROUTINE_LIST_MESSAGE
    status = ROUTINE_LIST_STATUS


class RoutineCreateResponseModel(RoutineResponseModelMixin):
    message = ROUTINE_CREATE_MESSAGE
    status = ROUTINE_CREATE_STATUS

    def get_response_data(self):
        return self.get_response_data_of_id()


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
