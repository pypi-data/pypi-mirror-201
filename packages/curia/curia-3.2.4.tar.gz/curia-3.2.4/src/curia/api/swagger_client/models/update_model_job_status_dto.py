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

class UpdateModelJobStatusDto(object):
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
        'model_job_id': 'str',
        'project_id': 'str',
        'source': 'str',
        'step': 'str',
        'message': 'str',
        'type': 'str',
        'order': 'float',
        'progress': 'float',
        'metadata': 'object'
    }

    attribute_map = {
        'model_job_id': 'modelJobId',
        'project_id': 'projectId',
        'source': 'source',
        'step': 'step',
        'message': 'message',
        'type': 'type',
        'order': 'order',
        'progress': 'progress',
        'metadata': 'metadata'
    }

    def __init__(self, model_job_id=None, project_id=None, source=None, step=None, message=None, type=None, order=None, progress=None, metadata=None):  # noqa: E501
        """UpdateModelJobStatusDto - a model defined in Swagger"""  # noqa: E501
        self._model_job_id = None
        self._project_id = None
        self._source = None
        self._step = None
        self._message = None
        self._type = None
        self._order = None
        self._progress = None
        self._metadata = None
        self.discriminator = None
        if model_job_id is not None:
            self.model_job_id = model_job_id
        if project_id is not None:
            self.project_id = project_id
        if source is not None:
            self.source = source
        if step is not None:
            self.step = step
        if message is not None:
            self.message = message
        if type is not None:
            self.type = type
        if order is not None:
            self.order = order
        if progress is not None:
            self.progress = progress
        if metadata is not None:
            self.metadata = metadata

    @property
    def model_job_id(self):
        """Gets the model_job_id of this UpdateModelJobStatusDto.  # noqa: E501


        :return: The model_job_id of this UpdateModelJobStatusDto.  # noqa: E501
        :rtype: str
        """
        return self._model_job_id

    @model_job_id.setter
    def model_job_id(self, model_job_id):
        """Sets the model_job_id of this UpdateModelJobStatusDto.


        :param model_job_id: The model_job_id of this UpdateModelJobStatusDto.  # noqa: E501
        :type: str
        """

        self._model_job_id = model_job_id

    @property
    def project_id(self):
        """Gets the project_id of this UpdateModelJobStatusDto.  # noqa: E501


        :return: The project_id of this UpdateModelJobStatusDto.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this UpdateModelJobStatusDto.


        :param project_id: The project_id of this UpdateModelJobStatusDto.  # noqa: E501
        :type: str
        """

        self._project_id = project_id

    @property
    def source(self):
        """Gets the source of this UpdateModelJobStatusDto.  # noqa: E501


        :return: The source of this UpdateModelJobStatusDto.  # noqa: E501
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this UpdateModelJobStatusDto.


        :param source: The source of this UpdateModelJobStatusDto.  # noqa: E501
        :type: str
        """

        self._source = source

    @property
    def step(self):
        """Gets the step of this UpdateModelJobStatusDto.  # noqa: E501


        :return: The step of this UpdateModelJobStatusDto.  # noqa: E501
        :rtype: str
        """
        return self._step

    @step.setter
    def step(self, step):
        """Sets the step of this UpdateModelJobStatusDto.


        :param step: The step of this UpdateModelJobStatusDto.  # noqa: E501
        :type: str
        """

        self._step = step

    @property
    def message(self):
        """Gets the message of this UpdateModelJobStatusDto.  # noqa: E501


        :return: The message of this UpdateModelJobStatusDto.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this UpdateModelJobStatusDto.


        :param message: The message of this UpdateModelJobStatusDto.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def type(self):
        """Gets the type of this UpdateModelJobStatusDto.  # noqa: E501


        :return: The type of this UpdateModelJobStatusDto.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this UpdateModelJobStatusDto.


        :param type: The type of this UpdateModelJobStatusDto.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def order(self):
        """Gets the order of this UpdateModelJobStatusDto.  # noqa: E501


        :return: The order of this UpdateModelJobStatusDto.  # noqa: E501
        :rtype: float
        """
        return self._order

    @order.setter
    def order(self, order):
        """Sets the order of this UpdateModelJobStatusDto.


        :param order: The order of this UpdateModelJobStatusDto.  # noqa: E501
        :type: float
        """

        self._order = order

    @property
    def progress(self):
        """Gets the progress of this UpdateModelJobStatusDto.  # noqa: E501


        :return: The progress of this UpdateModelJobStatusDto.  # noqa: E501
        :rtype: float
        """
        return self._progress

    @progress.setter
    def progress(self, progress):
        """Sets the progress of this UpdateModelJobStatusDto.


        :param progress: The progress of this UpdateModelJobStatusDto.  # noqa: E501
        :type: float
        """

        self._progress = progress

    @property
    def metadata(self):
        """Gets the metadata of this UpdateModelJobStatusDto.  # noqa: E501


        :return: The metadata of this UpdateModelJobStatusDto.  # noqa: E501
        :rtype: object
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this UpdateModelJobStatusDto.


        :param metadata: The metadata of this UpdateModelJobStatusDto.  # noqa: E501
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
        if issubclass(UpdateModelJobStatusDto, dict):
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
        if not isinstance(other, UpdateModelJobStatusDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
