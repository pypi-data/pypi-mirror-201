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

class CreateCohortDto(object):
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
        'model_id': 'str',
        'train_cohort_id': 'str',
        'cohort_windows': 'list[CohortWindow]',
        'revised_at': 'datetime'
    }

    attribute_map = {
        'name': 'name',
        'model_id': 'modelId',
        'train_cohort_id': 'trainCohortId',
        'cohort_windows': 'cohortWindows',
        'revised_at': 'revisedAt'
    }

    def __init__(self, name=None, model_id=None, train_cohort_id=None, cohort_windows=None, revised_at=None):  # noqa: E501
        """CreateCohortDto - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._model_id = None
        self._train_cohort_id = None
        self._cohort_windows = None
        self._revised_at = None
        self.discriminator = None
        if name is not None:
            self.name = name
        if model_id is not None:
            self.model_id = model_id
        if train_cohort_id is not None:
            self.train_cohort_id = train_cohort_id
        self.cohort_windows = cohort_windows
        if revised_at is not None:
            self.revised_at = revised_at

    @property
    def name(self):
        """Gets the name of this CreateCohortDto.  # noqa: E501


        :return: The name of this CreateCohortDto.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CreateCohortDto.


        :param name: The name of this CreateCohortDto.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def model_id(self):
        """Gets the model_id of this CreateCohortDto.  # noqa: E501


        :return: The model_id of this CreateCohortDto.  # noqa: E501
        :rtype: str
        """
        return self._model_id

    @model_id.setter
    def model_id(self, model_id):
        """Sets the model_id of this CreateCohortDto.


        :param model_id: The model_id of this CreateCohortDto.  # noqa: E501
        :type: str
        """

        self._model_id = model_id

    @property
    def train_cohort_id(self):
        """Gets the train_cohort_id of this CreateCohortDto.  # noqa: E501


        :return: The train_cohort_id of this CreateCohortDto.  # noqa: E501
        :rtype: str
        """
        return self._train_cohort_id

    @train_cohort_id.setter
    def train_cohort_id(self, train_cohort_id):
        """Sets the train_cohort_id of this CreateCohortDto.


        :param train_cohort_id: The train_cohort_id of this CreateCohortDto.  # noqa: E501
        :type: str
        """

        self._train_cohort_id = train_cohort_id

    @property
    def cohort_windows(self):
        """Gets the cohort_windows of this CreateCohortDto.  # noqa: E501


        :return: The cohort_windows of this CreateCohortDto.  # noqa: E501
        :rtype: list[CohortWindow]
        """
        return self._cohort_windows

    @cohort_windows.setter
    def cohort_windows(self, cohort_windows):
        """Sets the cohort_windows of this CreateCohortDto.


        :param cohort_windows: The cohort_windows of this CreateCohortDto.  # noqa: E501
        :type: list[CohortWindow]
        """
        if cohort_windows is None:
            raise ValueError("Invalid value for `cohort_windows`, must not be `None`")  # noqa: E501

        self._cohort_windows = cohort_windows

    @property
    def revised_at(self):
        """Gets the revised_at of this CreateCohortDto.  # noqa: E501


        :return: The revised_at of this CreateCohortDto.  # noqa: E501
        :rtype: datetime
        """
        return self._revised_at

    @revised_at.setter
    def revised_at(self, revised_at):
        """Sets the revised_at of this CreateCohortDto.


        :param revised_at: The revised_at of this CreateCohortDto.  # noqa: E501
        :type: datetime
        """

        self._revised_at = revised_at

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
        if issubclass(CreateCohortDto, dict):
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
        if not isinstance(other, CreateCohortDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
