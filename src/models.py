class ModelCreationFailure(Exception):
    """Raised when Model class verification failed due to incorrect keys inputs."""


class ModelValidationFailureKeys(Exception):
    """Raised when Model class verification failed due to incorrect keys inputs."""


class ModelValidationFailureValues(Exception):
    """Raised when Model class verification failed due to incorrect values inputs."""


class Model:
    """
    Model class is used for database models creation and validation of inputs.
    """
    def __init__(self, expected_keys):
        if not expected_keys:
            raise ModelCreationFailure
        if len([True for data_type in expected_keys.values() if isinstance(data_type, type)]) != \
                len(expected_keys.values()):
            raise ModelCreationFailure
        for key, value in expected_keys.items():
            setattr(self, key, value)

    def validate(self, input_dict):
        """
        validate function takes input dict that is checked if all keys are suitable for this model and values are
        correct data type
        :param input_dict: data dict
        :return: input_dict
        """
        if input_dict.keys() != vars(self).keys():
            raise ModelValidationFailureKeys
        for key, value in input_dict.items():
            if getattr(self, key) is not type(value):
                raise ModelValidationFailureValues
        return input_dict
