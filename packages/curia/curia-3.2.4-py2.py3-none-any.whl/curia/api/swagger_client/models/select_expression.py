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

class SelectExpression(object):
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
        'expression': 'ArithmeticExpression',
        'aggregation': 'str',
        'condition': 'Condition',
        'alias': 'str'
    }

    attribute_map = {
        'expression': 'expression',
        'aggregation': 'aggregation',
        'condition': 'condition',
        'alias': 'alias'
    }

    def __init__(self, expression=None, aggregation=None, condition=None, alias=None):  # noqa: E501
        """SelectExpression - a model defined in Swagger"""  # noqa: E501
        self._expression = None
        self._aggregation = None
        self._condition = None
        self._alias = None
        self.discriminator = None
        self.expression = expression
        self.aggregation = aggregation
        if condition is not None:
            self.condition = condition
        if alias is not None:
            self.alias = alias

    @property
    def expression(self):
        """Gets the expression of this SelectExpression.  # noqa: E501


        :return: The expression of this SelectExpression.  # noqa: E501
        :rtype: ArithmeticExpression
        """
        return self._expression

    @expression.setter
    def expression(self, expression):
        """Sets the expression of this SelectExpression.


        :param expression: The expression of this SelectExpression.  # noqa: E501
        :type: ArithmeticExpression
        """
        if expression is None:
            raise ValueError("Invalid value for `expression`, must not be `None`")  # noqa: E501

        self._expression = expression

    @property
    def aggregation(self):
        """Gets the aggregation of this SelectExpression.  # noqa: E501


        :return: The aggregation of this SelectExpression.  # noqa: E501
        :rtype: str
        """
        return self._aggregation

    @aggregation.setter
    def aggregation(self, aggregation):
        """Sets the aggregation of this SelectExpression.


        :param aggregation: The aggregation of this SelectExpression.  # noqa: E501
        :type: str
        """
        if aggregation is None:
            raise ValueError("Invalid value for `aggregation`, must not be `None`")  # noqa: E501
        allowed_values = ["count", "sum", "avg", "min", "max"]  # noqa: E501
        if aggregation not in allowed_values:
            raise ValueError(
                "Invalid value for `aggregation` ({0}), must be one of {1}"  # noqa: E501
                .format(aggregation, allowed_values)
            )

        self._aggregation = aggregation

    @property
    def condition(self):
        """Gets the condition of this SelectExpression.  # noqa: E501


        :return: The condition of this SelectExpression.  # noqa: E501
        :rtype: Condition
        """
        return self._condition

    @condition.setter
    def condition(self, condition):
        """Sets the condition of this SelectExpression.


        :param condition: The condition of this SelectExpression.  # noqa: E501
        :type: Condition
        """

        self._condition = condition

    @property
    def alias(self):
        """Gets the alias of this SelectExpression.  # noqa: E501


        :return: The alias of this SelectExpression.  # noqa: E501
        :rtype: str
        """
        return self._alias

    @alias.setter
    def alias(self, alias):
        """Sets the alias of this SelectExpression.


        :param alias: The alias of this SelectExpression.  # noqa: E501
        :type: str
        """

        self._alias = alias

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
        if issubclass(SelectExpression, dict):
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
        if not isinstance(other, SelectExpression):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
