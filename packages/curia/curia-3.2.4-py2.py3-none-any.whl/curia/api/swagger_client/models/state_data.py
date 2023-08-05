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

class StateData(object):
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
        'state': 'str',
        'patient_count': 'float',
        'outcome_count': 'float',
        'intervention_count': 'float'
    }

    attribute_map = {
        'state': 'state',
        'patient_count': 'patientCount',
        'outcome_count': 'outcomeCount',
        'intervention_count': 'interventionCount'
    }

    def __init__(self, state=None, patient_count=None, outcome_count=None, intervention_count=None):  # noqa: E501
        """StateData - a model defined in Swagger"""  # noqa: E501
        self._state = None
        self._patient_count = None
        self._outcome_count = None
        self._intervention_count = None
        self.discriminator = None
        self.state = state
        self.patient_count = patient_count
        self.outcome_count = outcome_count
        self.intervention_count = intervention_count

    @property
    def state(self):
        """Gets the state of this StateData.  # noqa: E501


        :return: The state of this StateData.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this StateData.


        :param state: The state of this StateData.  # noqa: E501
        :type: str
        """
        if state is None:
            raise ValueError("Invalid value for `state`, must not be `None`")  # noqa: E501

        self._state = state

    @property
    def patient_count(self):
        """Gets the patient_count of this StateData.  # noqa: E501


        :return: The patient_count of this StateData.  # noqa: E501
        :rtype: float
        """
        return self._patient_count

    @patient_count.setter
    def patient_count(self, patient_count):
        """Sets the patient_count of this StateData.


        :param patient_count: The patient_count of this StateData.  # noqa: E501
        :type: float
        """
        if patient_count is None:
            raise ValueError("Invalid value for `patient_count`, must not be `None`")  # noqa: E501

        self._patient_count = patient_count

    @property
    def outcome_count(self):
        """Gets the outcome_count of this StateData.  # noqa: E501


        :return: The outcome_count of this StateData.  # noqa: E501
        :rtype: float
        """
        return self._outcome_count

    @outcome_count.setter
    def outcome_count(self, outcome_count):
        """Sets the outcome_count of this StateData.


        :param outcome_count: The outcome_count of this StateData.  # noqa: E501
        :type: float
        """
        if outcome_count is None:
            raise ValueError("Invalid value for `outcome_count`, must not be `None`")  # noqa: E501

        self._outcome_count = outcome_count

    @property
    def intervention_count(self):
        """Gets the intervention_count of this StateData.  # noqa: E501


        :return: The intervention_count of this StateData.  # noqa: E501
        :rtype: float
        """
        return self._intervention_count

    @intervention_count.setter
    def intervention_count(self, intervention_count):
        """Sets the intervention_count of this StateData.


        :param intervention_count: The intervention_count of this StateData.  # noqa: E501
        :type: float
        """
        if intervention_count is None:
            raise ValueError("Invalid value for `intervention_count`, must not be `None`")  # noqa: E501

        self._intervention_count = intervention_count

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
        if issubclass(StateData, dict):
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
        if not isinstance(other, StateData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
