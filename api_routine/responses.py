class RoutineResponseModelMixin:
    response = None

    def get_response_data_of_id(self):
        return {
            "id": self.response.data["routine_id"]
        }


class RoutineListResponseModel(RoutineResponseModelMixin):
    def get_response_model_for_list(self):
        self.response.data = {
            "data": self.response.data,
            "message": {
                "msg": "Routine lookup was successful.",
                "status": "ROUTINE_LIST_OK"
            }
        }
        return self.response

    def get_response_model_for_create(self):
        self.response.data = {
            "data": self.get_response_data_of_id(),
            "message": {
                "msg": "You have successfully created the routine.",
                "status": "ROUTINE_CREATE_OK"
            }
        }
        return self.response


class RoutineDetailResponseModel(RoutineResponseModelMixin):
    def get_response_model_for_retrieve(self):
        self.response.data = {
            "data": self.response.data,
            "message": {
                "msg": "Routine lookup was successful.",
                "status": "ROUTINE_LIST_OK"
            }
        }
        return self.response

    def get_response_model_for_update(self):
        self.response.data = {
            "data": self.response.data,
            "message": {
                "msg": "The routine has been modified.",
                "status": "ROUTINE_UPDATE_OK"
            }
        }
        return self.response

    def get_response_model_for_delete(self):
        self.response.data = {
            "data": self.get_response_data_of_id(),
            "message": {
                "msg": "The routine has been deleted.",
                "status": "ROUTINE_DELETE_OK"
            }
        }
        return self.response

    def get_response_model_for_result(self):
        self.response.data = {
            "data": self.get_response_data_of_id(),
            "message": {
                "msg": "The routine's result has been updated.",
                "status": "ROUTINE_RESULT_UPDATE_OK"
            }
        }
        return self.response
