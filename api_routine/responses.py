from rest_framework.response import Response


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
    message = "Routine lookup was successful."
    status = "ROUTINE_LIST_OK"


class RoutineCreateResponseModel(RoutineResponseModelMixin):
    message = "You have successfully created the routine."
    status = "ROUTINE_CREATE_OK"

    def get_response_data(self):
        return {
            "id": self.response.data["routine_id"]
        }


class RoutineRetrieveResponseModel(RoutineResponseModelMixin):
    message = "Routine lookup was successful."
    status = "ROUTINE_DETAIL_OK"


class RoutineUpdateResponseModel(RoutineResponseModelMixin):
    message = "The routine has been modified."
    status = "ROUTINE_UPDATE_OK"

    def get_response_data(self):
        return self.get_response_data_of_id()


class RoutineDeleteResponseModel(RoutineResponseModelMixin):
    message = "The routine has been deleted."
    status = "ROUTINE_DELETE_OK"

    def get_response_data(self):
        return self.get_response_data_of_id()


class RoutineResultResponseModel(RoutineResponseModelMixin):
    message = "The routine's result has been updated."
    status = "ROUTINE_RESULT_UPDATE_OK"

    def get_response_data(self):
        return self.get_response_data_of_id()
