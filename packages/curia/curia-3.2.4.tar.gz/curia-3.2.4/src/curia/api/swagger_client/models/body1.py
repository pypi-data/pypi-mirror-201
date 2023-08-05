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

class Body1(object):
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
        'mime': 'str',
        'parts': 'float'
    }

    attribute_map = {
        'mime': 'mime',
        'parts': 'parts'
    }

    def __init__(self, mime=None, parts=None):  # noqa: E501
        """Body1 - a model defined in Swagger"""  # noqa: E501
        self._mime = None
        self._parts = None
        self.discriminator = None
        if mime is not None:
            self.mime = mime
        if parts is not None:
            self.parts = parts

    @property
    def mime(self):
        """Gets the mime of this Body1.  # noqa: E501


        :return: The mime of this Body1.  # noqa: E501
        :rtype: str
        """
        return self._mime

    @mime.setter
    def mime(self, mime):
        """Sets the mime of this Body1.


        :param mime: The mime of this Body1.  # noqa: E501
        :type: str
        """

        self._mime = mime

    @property
    def parts(self):
        """Gets the parts of this Body1.  # noqa: E501


        :return: The parts of this Body1.  # noqa: E501
        :rtype: float
        """
        return self._parts

    @parts.setter
    def parts(self, parts):
        """Sets the parts of this Body1.


        :param parts: The parts of this Body1.  # noqa: E501
        :type: float
        """

        self._parts = parts

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
        if issubclass(Body1, dict):
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
        if not isinstance(other, Body1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
