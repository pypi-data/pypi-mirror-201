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

class CreateTaskDto(object):
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
        'name': 'str',
        'description': 'str',
        'type': 'str',
        'inputs': 'TaskInputs',
        'outputs': 'TaskOutputs'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'type': 'type',
        'inputs': 'inputs',
        'outputs': 'outputs'
    }

    def __init__(self, name=None, description=None, type=None, inputs=None, outputs=None):  # noqa: E501
        """CreateTaskDto - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._description = None
        self._type = None
        self._inputs = None
        self._outputs = None
        self.discriminator = None
        self.name = name
        if description is not None:
            self.description = description
        self.type = type
        if inputs is not None:
            self.inputs = inputs
        if outputs is not None:
            self.outputs = outputs

    @property
    def name(self):
        """Gets the name of this CreateTaskDto.  # noqa: E501


        :return: The name of this CreateTaskDto.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CreateTaskDto.


        :param name: The name of this CreateTaskDto.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this CreateTaskDto.  # noqa: E501


        :return: The description of this CreateTaskDto.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CreateTaskDto.


        :param description: The description of this CreateTaskDto.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def type(self):
        """Gets the type of this CreateTaskDto.  # noqa: E501


        :return: The type of this CreateTaskDto.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this CreateTaskDto.


        :param type: The type of this CreateTaskDto.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["DatabricksJob", "DataQuery"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def inputs(self):
        """Gets the inputs of this CreateTaskDto.  # noqa: E501


        :return: The inputs of this CreateTaskDto.  # noqa: E501
        :rtype: TaskInputs
        """
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        """Sets the inputs of this CreateTaskDto.


        :param inputs: The inputs of this CreateTaskDto.  # noqa: E501
        :type: TaskInputs
        """

        self._inputs = inputs

    @property
    def outputs(self):
        """Gets the outputs of this CreateTaskDto.  # noqa: E501


        :return: The outputs of this CreateTaskDto.  # noqa: E501
        :rtype: TaskOutputs
        """
        return self._outputs

    @outputs.setter
    def outputs(self, outputs):
        """Sets the outputs of this CreateTaskDto.


        :param outputs: The outputs of this CreateTaskDto.  # noqa: E501
        :type: TaskOutputs
        """

        self._outputs = outputs

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
        if issubclass(CreateTaskDto, dict):
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
        if not isinstance(other, CreateTaskDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
