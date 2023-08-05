# coding: utf-8

"""
    Curia Platform API

    These are the docs for the curia platform API. To test, generate an authorization token first.  # noqa: E501

    OpenAPI spec version: 3.6.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class CreateTaskExecutionStatusDto(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'execution_id': 'str',
        'message': 'str',
        'type': 'str',
        'metadata': 'object'
    }

    attribute_map = {
        'execution_id': 'executionId',
        'message': 'message',
        'type': 'type',
        'metadata': 'metadata'
    }

    def __init__(self, execution_id=None, message=None, type=None, metadata=None):  # noqa: E501
        """CreateTaskExecutionStatusDto - a model defined in Swagger"""  # noqa: E501
        self._execution_id = None
        self._message = None
        self._type = None
        self._metadata = None
        self.discriminator = None
        self.execution_id = execution_id
        self.message = message
        self.type = type
        if metadata is not None:
            self.metadata = metadata

    @property
    def execution_id(self):
        """Gets the execution_id of this CreateTaskExecutionStatusDto.  # noqa: E501


        :return: The execution_id of this CreateTaskExecutionStatusDto.  # noqa: E501
        :rtype: str
        """
        return self._execution_id

    @execution_id.setter
    def execution_id(self, execution_id):
        """Sets the execution_id of this CreateTaskExecutionStatusDto.


        :param execution_id: The execution_id of this CreateTaskExecutionStatusDto.  # noqa: E501
        :type: str
        """
        if execution_id is None:
            raise ValueError("Invalid value for `execution_id`, must not be `None`")  # noqa: E501

        self._execution_id = execution_id

    @property
    def message(self):
        """Gets the message of this CreateTaskExecutionStatusDto.  # noqa: E501


        :return: The message of this CreateTaskExecutionStatusDto.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this CreateTaskExecutionStatusDto.


        :param message: The message of this CreateTaskExecutionStatusDto.  # noqa: E501
        :type: str
        """
        if message is None:
            raise ValueError("Invalid value for `message`, must not be `None`")  # noqa: E501

        self._message = message

    @property
    def type(self):
        """Gets the type of this CreateTaskExecutionStatusDto.  # noqa: E501


        :return: The type of this CreateTaskExecutionStatusDto.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this CreateTaskExecutionStatusDto.


        :param type: The type of this CreateTaskExecutionStatusDto.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def metadata(self):
        """Gets the metadata of this CreateTaskExecutionStatusDto.  # noqa: E501


        :return: The metadata of this CreateTaskExecutionStatusDto.  # noqa: E501
        :rtype: object
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this CreateTaskExecutionStatusDto.


        :param metadata: The metadata of this CreateTaskExecutionStatusDto.  # noqa: E501
        :type: object
        """

        self._metadata = metadata

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(CreateTaskExecutionStatusDto, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CreateTaskExecutionStatusDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
