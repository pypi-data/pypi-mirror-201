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

class CreateUserFavoriteDto(object):
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
        'user_id': 'str',
        'favorite_model_id': 'str',
        'favorite_project_id': 'str'
    }

    attribute_map = {
        'user_id': 'userId',
        'favorite_model_id': 'favoriteModelId',
        'favorite_project_id': 'favoriteProjectId'
    }

    def __init__(self, user_id=None, favorite_model_id=None, favorite_project_id=None):  # noqa: E501
        """CreateUserFavoriteDto - a model defined in Swagger"""  # noqa: E501
        self._user_id = None
        self._favorite_model_id = None
        self._favorite_project_id = None
        self.discriminator = None
        if user_id is not None:
            self.user_id = user_id
        if favorite_model_id is not None:
            self.favorite_model_id = favorite_model_id
        if favorite_project_id is not None:
            self.favorite_project_id = favorite_project_id

    @property
    def user_id(self):
        """Gets the user_id of this CreateUserFavoriteDto.  # noqa: E501


        :return: The user_id of this CreateUserFavoriteDto.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this CreateUserFavoriteDto.


        :param user_id: The user_id of this CreateUserFavoriteDto.  # noqa: E501
        :type: str
        """

        self._user_id = user_id

    @property
    def favorite_model_id(self):
        """Gets the favorite_model_id of this CreateUserFavoriteDto.  # noqa: E501


        :return: The favorite_model_id of this CreateUserFavoriteDto.  # noqa: E501
        :rtype: str
        """
        return self._favorite_model_id

    @favorite_model_id.setter
    def favorite_model_id(self, favorite_model_id):
        """Sets the favorite_model_id of this CreateUserFavoriteDto.


        :param favorite_model_id: The favorite_model_id of this CreateUserFavoriteDto.  # noqa: E501
        :type: str
        """

        self._favorite_model_id = favorite_model_id

    @property
    def favorite_project_id(self):
        """Gets the favorite_project_id of this CreateUserFavoriteDto.  # noqa: E501


        :return: The favorite_project_id of this CreateUserFavoriteDto.  # noqa: E501
        :rtype: str
        """
        return self._favorite_project_id

    @favorite_project_id.setter
    def favorite_project_id(self, favorite_project_id):
        """Sets the favorite_project_id of this CreateUserFavoriteDto.


        :param favorite_project_id: The favorite_project_id of this CreateUserFavoriteDto.  # noqa: E501
        :type: str
        """

        self._favorite_project_id = favorite_project_id

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
        if issubclass(CreateUserFavoriteDto, dict):
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
        if not isinstance(other, CreateUserFavoriteDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
