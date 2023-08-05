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

class ModelJobEvent(object):
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
        'id': 'str',
        'timestamp': 'datetime',
        'type': 'str',
        'step': 'str',
        'details': 'object',
        'order': 'float',
        'model_job_id': 'str',
        'project_id': 'str',
        'project': 'Project',
        'model_job': 'ModelJob',
        'last_updated_by': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'archived_at': 'datetime',
        'version': 'float'
    }

    attribute_map = {
        'id': 'id',
        'timestamp': 'timestamp',
        'type': 'type',
        'step': 'step',
        'details': 'details',
        'order': 'order',
        'model_job_id': 'modelJobId',
        'project_id': 'projectId',
        'project': 'project',
        'model_job': 'modelJob',
        'last_updated_by': 'lastUpdatedBy',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'archived_at': 'archivedAt',
        'version': 'version'
    }

    def __init__(self, id=None, timestamp=None, type=None, step=None, details=None, order=None, model_job_id=None, project_id=None, project=None, model_job=None, last_updated_by=None, created_at=None, updated_at=None, archived_at=None, version=None):  # noqa: E501
        """ModelJobEvent - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._timestamp = None
        self._type = None
        self._step = None
        self._details = None
        self._order = None
        self._model_job_id = None
        self._project_id = None
        self._project = None
        self._model_job = None
        self._last_updated_by = None
        self._created_at = None
        self._updated_at = None
        self._archived_at = None
        self._version = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if timestamp is not None:
            self.timestamp = timestamp
        if type is not None:
            self.type = type
        if step is not None:
            self.step = step
        if details is not None:
            self.details = details
        if order is not None:
            self.order = order
        if model_job_id is not None:
            self.model_job_id = model_job_id
        self.project_id = project_id
        if project is not None:
            self.project = project
        if model_job is not None:
            self.model_job = model_job
        if last_updated_by is not None:
            self.last_updated_by = last_updated_by
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at
        if archived_at is not None:
            self.archived_at = archived_at
        if version is not None:
            self.version = version

    @property
    def id(self):
        """Gets the id of this ModelJobEvent.  # noqa: E501


        :return: The id of this ModelJobEvent.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ModelJobEvent.


        :param id: The id of this ModelJobEvent.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def timestamp(self):
        """Gets the timestamp of this ModelJobEvent.  # noqa: E501


        :return: The timestamp of this ModelJobEvent.  # noqa: E501
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this ModelJobEvent.


        :param timestamp: The timestamp of this ModelJobEvent.  # noqa: E501
        :type: datetime
        """

        self._timestamp = timestamp

    @property
    def type(self):
        """Gets the type of this ModelJobEvent.  # noqa: E501


        :return: The type of this ModelJobEvent.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ModelJobEvent.


        :param type: The type of this ModelJobEvent.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def step(self):
        """Gets the step of this ModelJobEvent.  # noqa: E501


        :return: The step of this ModelJobEvent.  # noqa: E501
        :rtype: str
        """
        return self._step

    @step.setter
    def step(self, step):
        """Sets the step of this ModelJobEvent.


        :param step: The step of this ModelJobEvent.  # noqa: E501
        :type: str
        """

        self._step = step

    @property
    def details(self):
        """Gets the details of this ModelJobEvent.  # noqa: E501


        :return: The details of this ModelJobEvent.  # noqa: E501
        :rtype: object
        """
        return self._details

    @details.setter
    def details(self, details):
        """Sets the details of this ModelJobEvent.


        :param details: The details of this ModelJobEvent.  # noqa: E501
        :type: object
        """

        self._details = details

    @property
    def order(self):
        """Gets the order of this ModelJobEvent.  # noqa: E501


        :return: The order of this ModelJobEvent.  # noqa: E501
        :rtype: float
        """
        return self._order

    @order.setter
    def order(self, order):
        """Sets the order of this ModelJobEvent.


        :param order: The order of this ModelJobEvent.  # noqa: E501
        :type: float
        """

        self._order = order

    @property
    def model_job_id(self):
        """Gets the model_job_id of this ModelJobEvent.  # noqa: E501


        :return: The model_job_id of this ModelJobEvent.  # noqa: E501
        :rtype: str
        """
        return self._model_job_id

    @model_job_id.setter
    def model_job_id(self, model_job_id):
        """Sets the model_job_id of this ModelJobEvent.


        :param model_job_id: The model_job_id of this ModelJobEvent.  # noqa: E501
        :type: str
        """

        self._model_job_id = model_job_id

    @property
    def project_id(self):
        """Gets the project_id of this ModelJobEvent.  # noqa: E501


        :return: The project_id of this ModelJobEvent.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this ModelJobEvent.


        :param project_id: The project_id of this ModelJobEvent.  # noqa: E501
        :type: str
        """
        if project_id is None:
            raise ValueError("Invalid value for `project_id`, must not be `None`")  # noqa: E501

        self._project_id = project_id

    @property
    def project(self):
        """Gets the project of this ModelJobEvent.  # noqa: E501


        :return: The project of this ModelJobEvent.  # noqa: E501
        :rtype: Project
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this ModelJobEvent.


        :param project: The project of this ModelJobEvent.  # noqa: E501
        :type: Project
        """

        self._project = project

    @property
    def model_job(self):
        """Gets the model_job of this ModelJobEvent.  # noqa: E501


        :return: The model_job of this ModelJobEvent.  # noqa: E501
        :rtype: ModelJob
        """
        return self._model_job

    @model_job.setter
    def model_job(self, model_job):
        """Sets the model_job of this ModelJobEvent.


        :param model_job: The model_job of this ModelJobEvent.  # noqa: E501
        :type: ModelJob
        """

        self._model_job = model_job

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this ModelJobEvent.  # noqa: E501


        :return: The last_updated_by of this ModelJobEvent.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this ModelJobEvent.


        :param last_updated_by: The last_updated_by of this ModelJobEvent.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_at(self):
        """Gets the created_at of this ModelJobEvent.  # noqa: E501


        :return: The created_at of this ModelJobEvent.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ModelJobEvent.


        :param created_at: The created_at of this ModelJobEvent.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this ModelJobEvent.  # noqa: E501


        :return: The updated_at of this ModelJobEvent.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this ModelJobEvent.


        :param updated_at: The updated_at of this ModelJobEvent.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def archived_at(self):
        """Gets the archived_at of this ModelJobEvent.  # noqa: E501


        :return: The archived_at of this ModelJobEvent.  # noqa: E501
        :rtype: datetime
        """
        return self._archived_at

    @archived_at.setter
    def archived_at(self, archived_at):
        """Sets the archived_at of this ModelJobEvent.


        :param archived_at: The archived_at of this ModelJobEvent.  # noqa: E501
        :type: datetime
        """

        self._archived_at = archived_at

    @property
    def version(self):
        """Gets the version of this ModelJobEvent.  # noqa: E501


        :return: The version of this ModelJobEvent.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ModelJobEvent.


        :param version: The version of this ModelJobEvent.  # noqa: E501
        :type: float
        """

        self._version = version

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
        if issubclass(ModelJobEvent, dict):
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
        if not isinstance(other, ModelJobEvent):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
