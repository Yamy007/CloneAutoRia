class UserCreateMessageValidateDefaultFields:
    ACTIVE_MESSAGE = ", must be ACTIVE"
    STAFF_MESSAGE = ", must be STAFF"
    BLOCK_MESSAGE = ", cannot be BLOCKED"
    SUPERUSER_MESSAGE = ", the field SUPERUSER must be "

    def __error_message_active(self):
        return str(self.name) + self.ACTIVE_MESSAGE

    def __error_message_staff(self):
        return str(self.name) + self.STAFF_MESSAGE

    def __error_message_block(self):
        return str(self.name) + self.BLOCK_MESSAGE

    def error_message_superuser(self, status):
        return str(self.name) + self.SUPERUSER_MESSAGE + str(status).upper()

    def validate_base_fields(self):
        self.kwargs.setdefault("is_active", True)
        self.kwargs.setdefault("is_block", False)
        self.kwargs.setdefault("is_staff", True)
        if not self.kwargs.get("is_active"):
            raise ValueError(self.__error_message_active())
        if self.kwargs.get("is_block"):
            raise ValueError(self.__error_message_block())
        if not self.kwargs.get("is_staff"):
            raise ValueError(self.__error_message_staff())
        return self.kwargs

    def __init__(self, name, **kwargs):
        self.name = name
        self.kwargs = kwargs


class ValidationModelMessage:
    PASSWORD = "The password must be from 4 to 128 characters including Latin characters of any case, numbers and special characters, !@#$_-+"
    NAME_SURNAME = "This fields must have only letters from 3 to25"
