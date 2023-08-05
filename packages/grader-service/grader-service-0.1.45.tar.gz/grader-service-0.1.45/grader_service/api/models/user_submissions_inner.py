# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from grader_service.api.models.base_model_ import Model
from grader_service.api.models.submission import Submission
from grader_service.api.models.user import User
from grader_service.api import util

from grader_service.api.models.submission import Submission  # noqa: E501
from grader_service.api.models.user import User  # noqa: E501

class UserSubmissionsInner(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, user=None, submissions=None):  # noqa: E501
        """UserSubmissionsInner - a model defined in OpenAPI

        :param user: The user of this UserSubmissionsInner.  # noqa: E501
        :type user: User
        :param submissions: The submissions of this UserSubmissionsInner.  # noqa: E501
        :type submissions: List[Submission]
        """
        self.openapi_types = {
            'user': User,
            'submissions': List[Submission]
        }

        self.attribute_map = {
            'user': 'user',
            'submissions': 'submissions'
        }

        self._user = user
        self._submissions = submissions

    @classmethod
    def from_dict(cls, dikt) -> 'UserSubmissionsInner':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The UserSubmissions_inner of this UserSubmissionsInner.  # noqa: E501
        :rtype: UserSubmissionsInner
        """
        return util.deserialize_model(dikt, cls)

    @property
    def user(self):
        """Gets the user of this UserSubmissionsInner.


        :return: The user of this UserSubmissionsInner.
        :rtype: User
        """
        return self._user

    @user.setter
    def user(self, user):
        """Sets the user of this UserSubmissionsInner.


        :param user: The user of this UserSubmissionsInner.
        :type user: User
        """

        self._user = user

    @property
    def submissions(self):
        """Gets the submissions of this UserSubmissionsInner.


        :return: The submissions of this UserSubmissionsInner.
        :rtype: List[Submission]
        """
        return self._submissions

    @submissions.setter
    def submissions(self, submissions):
        """Sets the submissions of this UserSubmissionsInner.


        :param submissions: The submissions of this UserSubmissionsInner.
        :type submissions: List[Submission]
        """

        self._submissions = submissions
