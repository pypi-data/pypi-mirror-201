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

class Body2(object):
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
        'parts': 'list[DatasetsuploadlargecompleteParts]',
        'file_id': 'str',
        'file_key': 'str'
    }

    attribute_map = {
        'mime': 'mime',
        'parts': 'parts',
        'file_id': 'fileId',
        'file_key': 'fileKey'
    }

    def __init__(self, mime=None, parts=None, file_id=None, file_key=None):  # noqa: E501
        """Body2 - a model defined in Swagger"""  # noqa: E501
        self._mime = None
        self._parts = None
        self._file_id = None
        self._file_key = None
        self.discriminator = None
        if mime is not None:
            self.mime = mime
        if parts is not None:
            self.parts = parts
        if file_id is not None:
            self.file_id = file_id
        if file_key is not None:
            self.file_key = file_key

    @property
    def mime(self):
        """Gets the mime of this Body2.  # noqa: E501


        :return: The mime of this Body2.  # noqa: E501
        :rtype: str
        """
        return self._mime

    @mime.setter
    def mime(self, mime):
        """Sets the mime of this Body2.


        :param mime: The mime of this Body2.  # noqa: E501
        :type: str
        """

        self._mime = mime

    @property
    def parts(self):
        """Gets the parts of this Body2.  # noqa: E501


        :return: The parts of this Body2.  # noqa: E501
        :rtype: list[DatasetsuploadlargecompleteParts]
        """
        return self._parts

    @parts.setter
    def parts(self, parts):
        """Sets the parts of this Body2.


        :param parts: The parts of this Body2.  # noqa: E501
        :type: list[DatasetsuploadlargecompleteParts]
        """

        self._parts = parts

    @property
    def file_id(self):
        """Gets the file_id of this Body2.  # noqa: E501


        :return: The file_id of this Body2.  # noqa: E501
        :rtype: str
        """
        return self._file_id

    @file_id.setter
    def file_id(self, file_id):
        """Sets the file_id of this Body2.


        :param file_id: The file_id of this Body2.  # noqa: E501
        :type: str
        """

        self._file_id = file_id

    @property
    def file_key(self):
        """Gets the file_key of this Body2.  # noqa: E501


        :return: The file_key of this Body2.  # noqa: E501
        :rtype: str
        """
        return self._file_key

    @file_key.setter
    def file_key(self, file_key):
        """Sets the file_key of this Body2.


        :param file_key: The file_key of this Body2.  # noqa: E501
        :type: str
        """

        self._file_key = file_key

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
        if issubclass(Body2, dict):
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
        if not isinstance(other, Body2):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
