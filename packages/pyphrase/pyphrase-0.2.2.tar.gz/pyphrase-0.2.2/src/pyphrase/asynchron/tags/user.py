from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    AbstractUserCreateDto,
    AbstractUserEditDto,
    PageDtoAssignedJobDto,
    PageDtoLastLoginDto,
    PageDtoProjectReference,
    PageDtoString,
    PageDtoUserDto,
    PageDtoWorkflowStepReference,
    UserDetailsDtoV3,
    UserDto,
    UserPasswordEditDto,
    UserStatisticsListDto,
)


class UserOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def deleteUser_1(
        self, userUid: str, phrase_token: Optional[str] = None
    ) -> None:
        """
        Delete user

        :param userUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/users/{userUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def listAssignedProjects(
        self,
        userUid: str,
        projectName: str = None,
        filename: str = None,
        dueInHours: int = None,
        workflowStepId: int = None,
        targetLang: List[str] = None,
        status: List[str] = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoProjectReference:
        """
        List assigned projects

        :param userUid: string (required), path.
        :param projectName: string (optional), query.
        :param filename: string (optional), query.
        :param dueInHours: integer (optional), query. -1 for jobs that are overdue.
        :param workflowStepId: integer (optional), query.
        :param targetLang: array (optional), query.
        :param status: array (optional), query.
        :param pageNumber: integer (optional), query.
        :param pageSize: integer (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoProjectReference
        """
        endpoint = f"/api2/v1/users/{userUid}/projects"
        params = {
            "status": status,
            "targetLang": targetLang,
            "workflowStepId": workflowStepId,
            "dueInHours": dueInHours,
            "filename": filename,
            "projectName": projectName,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoProjectReference(**r)

    async def listTargetLangs(
        self,
        userUid: str,
        filename: str = None,
        dueInHours: int = None,
        workflowStepId: int = None,
        projectUid: str = None,
        status: List[str] = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoString:
        """
        List assigned target languages

        :param userUid: string (required), path.
        :param filename: string (optional), query.
        :param dueInHours: integer (optional), query. -1 for jobs that are overdue.
        :param workflowStepId: integer (optional), query.
        :param projectUid: string (optional), query.
        :param status: array (optional), query.
        :param pageNumber: integer (optional), query.
        :param pageSize: integer (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoString
        """
        endpoint = f"/api2/v1/users/{userUid}/targetLangs"
        params = {
            "status": status,
            "projectUid": projectUid,
            "workflowStepId": workflowStepId,
            "dueInHours": dueInHours,
            "filename": filename,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoString(**r)

    async def user_lastLogins(
        self,
        order: List[str] = None,
        sort: List[str] = None,
        role: List[str] = None,
        userName: str = None,
        pageNumber: int = "0",
        pageSize: int = "100",
        phrase_token: Optional[str] = None,
    ) -> PageDtoLastLoginDto:
        """
        List last login dates

        :param order: array (optional), query.
        :param sort: array (optional), query.
        :param role: array (optional), query.
        :param userName: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 100, default 100.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoLastLoginDto
        """
        endpoint = f"/api2/v1/users/lastLogins"
        params = {
            "userName": userName,
            "role": role,
            "sort": sort,
            "order": order,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoLastLoginDto(**r)

    async def listJobs(
        self,
        userUid: str,
        filename: str = None,
        dueInHours: int = None,
        workflowStepId: int = None,
        targetLang: List[str] = None,
        projectUid: str = None,
        status: List[str] = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoAssignedJobDto:
        """
        List assigned jobs

        :param userUid: string (required), path.
        :param filename: string (optional), query.
        :param dueInHours: integer (optional), query. -1 for jobs that are overdue.
        :param workflowStepId: integer (optional), query.
        :param targetLang: array (optional), query.
        :param projectUid: string (optional), query.
        :param status: array (optional), query.
        :param pageNumber: integer (optional), query.
        :param pageSize: integer (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoAssignedJobDto
        """
        endpoint = f"/api2/v1/users/{userUid}/jobs"
        params = {
            "status": status,
            "projectUid": projectUid,
            "targetLang": targetLang,
            "workflowStepId": workflowStepId,
            "dueInHours": dueInHours,
            "filename": filename,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoAssignedJobDto(**r)

    async def sendLoginInfo(
        self, userUid: str, phrase_token: Optional[str] = None
    ) -> None:
        """
        Send login information

        :param userUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/users/{userUid}/emailLoginInformation"
        params = {}

        files = None
        payload = None

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def cancelDeletion(
        self, userUid: str, phrase_token: Optional[str] = None
    ) -> UserDto:
        """
        Restore user

        :param userUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: UserDto
        """
        endpoint = f"/api2/v1/users/{userUid}/undelete"
        params = {}

        files = None
        payload = None

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return UserDto(**r)

    async def loginActivity(
        self, userUid: str, phrase_token: Optional[str] = None
    ) -> UserStatisticsListDto:
        """
        Login statistics

        :param userUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: UserStatisticsListDto
        """
        endpoint = f"/api2/v1/users/{userUid}/loginStatistics"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return UserStatisticsListDto(**r)

    async def getListOfUsersFiltered(
        self,
        order: List[str] = None,
        sort: List[str] = None,
        role: List[str] = None,
        nameOrEmail: str = None,
        email: str = None,
        userName: str = None,
        name: str = None,
        lastName: str = None,
        firstName: str = None,
        includeDeleted: bool = "False",
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoUserDto:
        """
        List users

        :param order: array (optional), query.
        :param sort: array (optional), query.
        :param role: array (optional), query.
        :param nameOrEmail: string (optional), query. Filter for last name, first name or email starting with the value.
        :param email: string (optional), query.
        :param userName: string (optional), query.
        :param name: string (optional), query. Filter for last name or first name, that starts with value.
        :param lastName: string (optional), query. Filter for last name, that starts with value.
        :param firstName: string (optional), query. Filter for first name, that starts with value.
        :param includeDeleted: boolean (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoUserDto
        """
        endpoint = f"/api2/v1/users"
        params = {
            "firstName": firstName,
            "lastName": lastName,
            "name": name,
            "userName": userName,
            "email": email,
            "nameOrEmail": nameOrEmail,
            "role": role,
            "includeDeleted": includeDeleted,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "sort": sort,
            "order": order,
        }

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoUserDto(**r)

    async def listWorkflowSteps(
        self,
        userUid: str,
        filename: str = None,
        dueInHours: int = None,
        targetLang: List[str] = None,
        projectUid: str = None,
        status: List[str] = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoWorkflowStepReference:
        """
        List assigned workflow steps

        :param userUid: string (required), path.
        :param filename: string (optional), query.
        :param dueInHours: integer (optional), query. -1 for jobs that are overdue.
        :param targetLang: array (optional), query.
        :param projectUid: string (optional), query.
        :param status: array (optional), query.
        :param pageNumber: integer (optional), query.
        :param pageSize: integer (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoWorkflowStepReference
        """
        endpoint = f"/api2/v1/users/{userUid}/workflowSteps"
        params = {
            "status": status,
            "projectUid": projectUid,
            "targetLang": targetLang,
            "dueInHours": dueInHours,
            "filename": filename,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoWorkflowStepReference(**r)

    async def updatePassword(
        self,
        userUid: str,
        body: UserPasswordEditDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
                Update password
                * Password length must be between 8 and 255
        * Password must not be same as the username
                :param userUid: string (required), path.
                :param body: UserPasswordEditDto (required), body.

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return: None
        """
        endpoint = f"/api2/v1/users/{userUid}/updatePassword"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def getUserV3(
        self, userUid: str, phrase_token: Optional[str] = None
    ) -> UserDetailsDtoV3:
        """
        Get user

        :param userUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: UserDetailsDtoV3
        """
        endpoint = f"/api2/v3/users/{userUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return UserDetailsDtoV3(**r)

    async def updateUserV3(
        self,
        userUid: str,
        body: AbstractUserEditDto,
        phrase_token: Optional[str] = None,
    ) -> UserDetailsDtoV3:
        """
        Edit user

        :param userUid: string (required), path.
        :param body: AbstractUserEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: UserDetailsDtoV3
        """
        endpoint = f"/api2/v3/users/{userUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return UserDetailsDtoV3(**r)

    async def createUserV3(
        self, body: AbstractUserCreateDto, phrase_token: Optional[str] = None
    ) -> UserDetailsDtoV3:
        """
        Create user

        :param body: AbstractUserCreateDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: UserDetailsDtoV3
        """
        endpoint = f"/api2/v3/users"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return UserDetailsDtoV3(**r)
