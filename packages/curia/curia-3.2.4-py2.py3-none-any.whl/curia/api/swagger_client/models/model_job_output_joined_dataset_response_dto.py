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

class ModelJobOutputJoinedDatasetResponseDto(object):
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
        'name': 'str',
        'description': 'str',
        'tags': 'list[str]',
        'type': 'object',
        'model_type': 'str',
        'outcome_type': 'object',
        'treatment_type': 'object',
        'location': 'str',
        'file_content_type': 'str',
        'file_size': 'str',
        'file_type': 'str',
        'row_count': 'str',
        'column_count': 'float',
        'status': 'str',
        'is_downloadable': 'bool',
        'organization_id': 'str',
        'last_updated_by': 'str',
        'created_by': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'archived_at': 'datetime',
        'version': 'float'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'description': 'description',
        'tags': 'tags',
        'type': 'type',
        'model_type': 'modelType',
        'outcome_type': 'outcomeType',
        'treatment_type': 'treatmentType',
        'location': 'location',
        'file_content_type': 'fileContentType',
        'file_size': 'fileSize',
        'file_type': 'fileType',
        'row_count': 'rowCount',
        'column_count': 'columnCount',
        'status': 'status',
        'is_downloadable': 'isDownloadable',
        'organization_id': 'organizationId',
        'last_updated_by': 'lastUpdatedBy',
        'created_by': 'createdBy',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'archived_at': 'archivedAt',
        'version': 'version'
    }

    def __init__(self, id=None, name=None, description=None, tags=None, type=None, model_type=None, outcome_type=None, treatment_type=None, location=None, file_content_type=None, file_size=None, file_type=None, row_count=None, column_count=None, status=None, is_downloadable=None, organization_id=None, last_updated_by=None, created_by=None, created_at=None, updated_at=None, archived_at=None, version=None):  # noqa: E501
        """ModelJobOutputJoinedDatasetResponseDto - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._name = None
        self._description = None
        self._tags = None
        self._type = None
        self._model_type = None
        self._outcome_type = None
        self._treatment_type = None
        self._location = None
        self._file_content_type = None
        self._file_size = None
        self._file_type = None
        self._row_count = None
        self._column_count = None
        self._status = None
        self._is_downloadable = None
        self._organization_id = None
        self._last_updated_by = None
        self._created_by = None
        self._created_at = None
        self._updated_at = None
        self._archived_at = None
        self._version = None
        self.discriminator = None
        if id is not None:
            self.id = id
        self.name = name
        if description is not None:
            self.description = description
        if tags is not None:
            self.tags = tags
        self.type = type
        if model_type is not None:
            self.model_type = model_type
        if outcome_type is not None:
            self.outcome_type = outcome_type
        if treatment_type is not None:
            self.treatment_type = treatment_type
        if location is not None:
            self.location = location
        if file_content_type is not None:
            self.file_content_type = file_content_type
        if file_size is not None:
            self.file_size = file_size
        if file_type is not None:
            self.file_type = file_type
        if row_count is not None:
            self.row_count = row_count
        if column_count is not None:
            self.column_count = column_count
        if status is not None:
            self.status = status
        if is_downloadable is not None:
            self.is_downloadable = is_downloadable
        self.organization_id = organization_id
        if last_updated_by is not None:
            self.last_updated_by = last_updated_by
        if created_by is not None:
            self.created_by = created_by
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
        """Gets the id of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The id of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ModelJobOutputJoinedDatasetResponseDto.


        :param id: The id of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The name of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ModelJobOutputJoinedDatasetResponseDto.


        :param name: The name of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The description of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ModelJobOutputJoinedDatasetResponseDto.


        :param description: The description of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def tags(self):
        """Gets the tags of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The tags of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this ModelJobOutputJoinedDatasetResponseDto.


        :param tags: The tags of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def type(self):
        """Gets the type of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The type of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: object
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ModelJobOutputJoinedDatasetResponseDto.


        :param type: The type of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: object
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def model_type(self):
        """Gets the model_type of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The model_type of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._model_type

    @model_type.setter
    def model_type(self, model_type):
        """Sets the model_type of this ModelJobOutputJoinedDatasetResponseDto.


        :param model_type: The model_type of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: str
        """
        allowed_values = ["risk", "impactability"]  # noqa: E501
        if model_type not in allowed_values:
            raise ValueError(
                "Invalid value for `model_type` ({0}), must be one of {1}"  # noqa: E501
                .format(model_type, allowed_values)
            )

        self._model_type = model_type

    @property
    def outcome_type(self):
        """Gets the outcome_type of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The outcome_type of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: object
        """
        return self._outcome_type

    @outcome_type.setter
    def outcome_type(self, outcome_type):
        """Sets the outcome_type of this ModelJobOutputJoinedDatasetResponseDto.


        :param outcome_type: The outcome_type of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: object
        """

        self._outcome_type = outcome_type

    @property
    def treatment_type(self):
        """Gets the treatment_type of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The treatment_type of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: object
        """
        return self._treatment_type

    @treatment_type.setter
    def treatment_type(self, treatment_type):
        """Sets the treatment_type of this ModelJobOutputJoinedDatasetResponseDto.


        :param treatment_type: The treatment_type of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: object
        """

        self._treatment_type = treatment_type

    @property
    def location(self):
        """Gets the location of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The location of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location):
        """Sets the location of this ModelJobOutputJoinedDatasetResponseDto.


        :param location: The location of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: str
        """

        self._location = location

    @property
    def file_content_type(self):
        """Gets the file_content_type of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The file_content_type of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._file_content_type

    @file_content_type.setter
    def file_content_type(self, file_content_type):
        """Sets the file_content_type of this ModelJobOutputJoinedDatasetResponseDto.


        :param file_content_type: The file_content_type of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: str
        """

        self._file_content_type = file_content_type

    @property
    def file_size(self):
        """Gets the file_size of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The file_size of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._file_size

    @file_size.setter
    def file_size(self, file_size):
        """Sets the file_size of this ModelJobOutputJoinedDatasetResponseDto.


        :param file_size: The file_size of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: str
        """

        self._file_size = file_size

    @property
    def file_type(self):
        """Gets the file_type of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The file_type of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._file_type

    @file_type.setter
    def file_type(self, file_type):
        """Sets the file_type of this ModelJobOutputJoinedDatasetResponseDto.


        :param file_type: The file_type of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: str
        """

        self._file_type = file_type

    @property
    def row_count(self):
        """Gets the row_count of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The row_count of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._row_count

    @row_count.setter
    def row_count(self, row_count):
        """Sets the row_count of this ModelJobOutputJoinedDatasetResponseDto.


        :param row_count: The row_count of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: str
        """

        self._row_count = row_count

    @property
    def column_count(self):
        """Gets the column_count of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The column_count of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: float
        """
        return self._column_count

    @column_count.setter
    def column_count(self, column_count):
        """Sets the column_count of this ModelJobOutputJoinedDatasetResponseDto.


        :param column_count: The column_count of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: float
        """

        self._column_count = column_count

    @property
    def status(self):
        """Gets the status of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The status of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ModelJobOutputJoinedDatasetResponseDto.


        :param status: The status of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def is_downloadable(self):
        """Gets the is_downloadable of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The is_downloadable of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: bool
        """
        return self._is_downloadable

    @is_downloadable.setter
    def is_downloadable(self, is_downloadable):
        """Sets the is_downloadable of this ModelJobOutputJoinedDatasetResponseDto.


        :param is_downloadable: The is_downloadable of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: bool
        """

        self._is_downloadable = is_downloadable

    @property
    def organization_id(self):
        """Gets the organization_id of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The organization_id of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._organization_id

    @organization_id.setter
    def organization_id(self, organization_id):
        """Sets the organization_id of this ModelJobOutputJoinedDatasetResponseDto.


        :param organization_id: The organization_id of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: str
        """
        if organization_id is None:
            raise ValueError("Invalid value for `organization_id`, must not be `None`")  # noqa: E501

        self._organization_id = organization_id

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The last_updated_by of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this ModelJobOutputJoinedDatasetResponseDto.


        :param last_updated_by: The last_updated_by of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_by(self):
        """Gets the created_by of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The created_by of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this ModelJobOutputJoinedDatasetResponseDto.


        :param created_by: The created_by of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def created_at(self):
        """Gets the created_at of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The created_at of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ModelJobOutputJoinedDatasetResponseDto.


        :param created_at: The created_at of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The updated_at of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this ModelJobOutputJoinedDatasetResponseDto.


        :param updated_at: The updated_at of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def archived_at(self):
        """Gets the archived_at of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The archived_at of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._archived_at

    @archived_at.setter
    def archived_at(self, archived_at):
        """Sets the archived_at of this ModelJobOutputJoinedDatasetResponseDto.


        :param archived_at: The archived_at of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :type: datetime
        """

        self._archived_at = archived_at

    @property
    def version(self):
        """Gets the version of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501


        :return: The version of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ModelJobOutputJoinedDatasetResponseDto.


        :param version: The version of this ModelJobOutputJoinedDatasetResponseDto.  # noqa: E501
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
        if issubclass(ModelJobOutputJoinedDatasetResponseDto, dict):
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
        if not isinstance(other, ModelJobOutputJoinedDatasetResponseDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
