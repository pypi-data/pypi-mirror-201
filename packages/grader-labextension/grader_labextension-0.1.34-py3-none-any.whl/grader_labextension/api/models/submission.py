# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from grader_labextension.api.models.base_model_ import Model
from grader_labextension.api import util


class Submission(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, submitted_at=None, auto_status=None, manual_status=None, username=None, score=None, commit_hash=None, feedback_available=None, edited=None, logs=None):  # noqa: E501
        """Submission - a model defined in OpenAPI

        :param id: The id of this Submission.  # noqa: E501
        :type id: int
        :param submitted_at: The submitted_at of this Submission.  # noqa: E501
        :type submitted_at: datetime
        :param auto_status: The auto_status of this Submission.  # noqa: E501
        :type auto_status: str
        :param manual_status: The manual_status of this Submission.  # noqa: E501
        :type manual_status: str
        :param username: The username of this Submission.  # noqa: E501
        :type username: str
        :param score: The score of this Submission.  # noqa: E501
        :type score: float
        :param commit_hash: The commit_hash of this Submission.  # noqa: E501
        :type commit_hash: str
        :param feedback_available: The feedback_available of this Submission.  # noqa: E501
        :type feedback_available: bool
        :param edited: The edited of this Submission.  # noqa: E501
        :type edited: bool
        :param logs: The logs of this Submission.  # noqa: E501
        :type logs: str
        """
        self.openapi_types = {
            'id': int,
            'submitted_at': datetime,
            'auto_status': str,
            'manual_status': str,
            'username': str,
            'score': float,
            'commit_hash': str,
            'feedback_available': bool,
            'edited': bool,
            'logs': str
        }

        self.attribute_map = {
            'id': 'id',
            'submitted_at': 'submitted_at',
            'auto_status': 'auto_status',
            'manual_status': 'manual_status',
            'username': 'username',
            'score': 'score',
            'commit_hash': 'commit_hash',
            'feedback_available': 'feedback_available',
            'edited': 'edited',
            'logs': 'logs'
        }

        self._id = id
        self._submitted_at = submitted_at
        self._auto_status = auto_status
        self._manual_status = manual_status
        self._username = username
        self._score = score
        self._commit_hash = commit_hash
        self._feedback_available = feedback_available
        self._edited = edited
        self._logs = logs

    @classmethod
    def from_dict(cls, dikt) -> 'Submission':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Submission of this Submission.  # noqa: E501
        :rtype: Submission
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Submission.


        :return: The id of this Submission.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Submission.


        :param id: The id of this Submission.
        :type id: int
        """

        self._id = id

    @property
    def submitted_at(self):
        """Gets the submitted_at of this Submission.


        :return: The submitted_at of this Submission.
        :rtype: datetime
        """
        return self._submitted_at

    @submitted_at.setter
    def submitted_at(self, submitted_at):
        """Sets the submitted_at of this Submission.


        :param submitted_at: The submitted_at of this Submission.
        :type submitted_at: datetime
        """

        self._submitted_at = submitted_at

    @property
    def auto_status(self):
        """Gets the auto_status of this Submission.


        :return: The auto_status of this Submission.
        :rtype: str
        """
        return self._auto_status

    @auto_status.setter
    def auto_status(self, auto_status):
        """Sets the auto_status of this Submission.


        :param auto_status: The auto_status of this Submission.
        :type auto_status: str
        """
        allowed_values = ["not_graded", "pending", "automatically_graded", "grading_failed"]  # noqa: E501
        if auto_status not in allowed_values:
            raise ValueError(
                "Invalid value for `auto_status` ({0}), must be one of {1}"
                .format(auto_status, allowed_values)
            )

        self._auto_status = auto_status

    @property
    def manual_status(self):
        """Gets the manual_status of this Submission.


        :return: The manual_status of this Submission.
        :rtype: str
        """
        return self._manual_status

    @manual_status.setter
    def manual_status(self, manual_status):
        """Sets the manual_status of this Submission.


        :param manual_status: The manual_status of this Submission.
        :type manual_status: str
        """
        allowed_values = ["not_graded", "manually_graded", "being_edited", "grading_failed"]  # noqa: E501
        if manual_status not in allowed_values:
            raise ValueError(
                "Invalid value for `manual_status` ({0}), must be one of {1}"
                .format(manual_status, allowed_values)
            )

        self._manual_status = manual_status

    @property
    def username(self):
        """Gets the username of this Submission.


        :return: The username of this Submission.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this Submission.


        :param username: The username of this Submission.
        :type username: str
        """

        self._username = username

    @property
    def score(self):
        """Gets the score of this Submission.


        :return: The score of this Submission.
        :rtype: float
        """
        return self._score

    @score.setter
    def score(self, score):
        """Sets the score of this Submission.


        :param score: The score of this Submission.
        :type score: float
        """

        self._score = score

    @property
    def commit_hash(self):
        """Gets the commit_hash of this Submission.


        :return: The commit_hash of this Submission.
        :rtype: str
        """
        return self._commit_hash

    @commit_hash.setter
    def commit_hash(self, commit_hash):
        """Sets the commit_hash of this Submission.


        :param commit_hash: The commit_hash of this Submission.
        :type commit_hash: str
        """

        self._commit_hash = commit_hash

    @property
    def feedback_available(self):
        """Gets the feedback_available of this Submission.


        :return: The feedback_available of this Submission.
        :rtype: bool
        """
        return self._feedback_available

    @feedback_available.setter
    def feedback_available(self, feedback_available):
        """Sets the feedback_available of this Submission.


        :param feedback_available: The feedback_available of this Submission.
        :type feedback_available: bool
        """

        self._feedback_available = feedback_available

    @property
    def edited(self):
        """Gets the edited of this Submission.


        :return: The edited of this Submission.
        :rtype: bool
        """
        return self._edited

    @edited.setter
    def edited(self, edited):
        """Sets the edited of this Submission.


        :param edited: The edited of this Submission.
        :type edited: bool
        """

        self._edited = edited

    @property
    def logs(self):
        """Gets the logs of this Submission.


        :return: The logs of this Submission.
        :rtype: str
        """
        return self._logs

    @logs.setter
    def logs(self, logs):
        """Sets the logs of this Submission.


        :param logs: The logs of this Submission.
        :type logs: str
        """

        self._logs = logs
