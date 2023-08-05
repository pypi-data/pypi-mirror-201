from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    AbstractAnalyseSettingsDto,
    EditAnalyseSettingsDto,
    EditProjectSecuritySettingsDtoV2,
    FileImportSettingsDto,
    MTSettingsPerLanguageListDto,
    PageDtoProjectTemplateReference,
    PageDtoTransMemoryDto,
    PreTranslateSettingsV3Dto,
    ProjectSecuritySettingsDtoV2,
    ProjectTemplateCreateActionDto,
    ProjectTemplateDto,
    ProjectTemplateEditDto,
    ProjectTemplateTermBaseListDto,
    ProjectTemplateTransMemoryListDtoV3,
    ProjectTemplateTransMemoryListV2Dto,
    SetProjectTemplateTermBaseDto,
    SetProjectTemplateTransMemoriesV2Dto,
)


class ProjectTemplateOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def relevantTransMemories(
        self,
        projectTemplateUid: str,
        targetLangs: List[str] = None,
        subDomainName: str = None,
        clientName: str = None,
        domainName: str = None,
        name: str = None,
        strictLangMatching: bool = "False",
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoTransMemoryDto:
        """
        List project template relevant translation memories

        :param projectTemplateUid: string (required), path.
        :param targetLangs: array (optional), query.
        :param subDomainName: string (optional), query.
        :param clientName: string (optional), query.
        :param domainName: string (optional), query.
        :param name: string (optional), query.
        :param strictLangMatching: boolean (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoTransMemoryDto
        """
        endpoint = (
            f"/api2/v1/projectTemplates/{projectTemplateUid}/transMemories/relevant"
        )
        params = {
            "name": name,
            "domainName": domainName,
            "clientName": clientName,
            "subDomainName": subDomainName,
            "targetLangs": targetLangs,
            "strictLangMatching": strictLangMatching,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoTransMemoryDto(**r)

    def getProjectTemplates(
        self,
        businessUnitName: str = None,
        costCenterName: str = None,
        costCenterId: int = None,
        subDomainName: str = None,
        domainName: str = None,
        ownerUid: str = None,
        clientName: str = None,
        clientId: int = None,
        name: str = None,
        sort: str = "dateCreated",
        direction: str = "desc",
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoProjectTemplateReference:
        """
        List project templates

        :param businessUnitName: string (optional), query.
        :param costCenterName: string (optional), query.
        :param costCenterId: integer (optional), query.
        :param subDomainName: string (optional), query.
        :param domainName: string (optional), query.
        :param ownerUid: string (optional), query.
        :param clientName: string (optional), query.
        :param clientId: integer (optional), query.
        :param name: string (optional), query.
        :param sort: string (optional), query.
        :param direction: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoProjectTemplateReference
        """
        endpoint = f"/api2/v1/projectTemplates"
        params = {
            "name": name,
            "clientId": clientId,
            "clientName": clientName,
            "ownerUid": ownerUid,
            "domainName": domainName,
            "subDomainName": subDomainName,
            "costCenterId": costCenterId,
            "costCenterName": costCenterName,
            "businessUnitName": businessUnitName,
            "sort": sort,
            "direction": direction,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoProjectTemplateReference(**r)

    def createProjectTemplate(
        self,
        body: ProjectTemplateCreateActionDto,
        phrase_token: Optional[str] = None,
    ) -> ProjectTemplateDto:
        """
        Create project template

        :param body: ProjectTemplateCreateActionDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTemplateDto
        """
        endpoint = f"/api2/v1/projectTemplates"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTemplateDto(**r)

    def getProjectTemplateTermBases(
        self,
        projectTemplateUid: str,
        phrase_token: Optional[str] = None,
    ) -> ProjectTemplateTermBaseListDto:
        """
        Get term bases

        :param projectTemplateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTemplateTermBaseListDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/termBases"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTemplateTermBaseListDto(**r)

    def setProjectTemplateTermBases(
        self,
        projectTemplateUid: str,
        body: SetProjectTemplateTermBaseDto,
        phrase_token: Optional[str] = None,
    ) -> ProjectTemplateTermBaseListDto:
        """
        Edit term bases in project template

        :param projectTemplateUid: string (required), path.
        :param body: SetProjectTemplateTermBaseDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTemplateTermBaseListDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/termBases"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTemplateTermBaseListDto(**r)

    def getProjectTemplateAccessSettings(
        self,
        projectTemplateUid: str,
        phrase_token: Optional[str] = None,
    ) -> ProjectSecuritySettingsDtoV2:
        """
        Get project template access and security settings

        :param projectTemplateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectSecuritySettingsDtoV2
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/accessSettings"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectSecuritySettingsDtoV2(**r)

    def editProjectTemplateAccessSettings(
        self,
        projectTemplateUid: str,
        body: EditProjectSecuritySettingsDtoV2,
        phrase_token: Optional[str] = None,
    ) -> ProjectSecuritySettingsDtoV2:
        """
        Edit project template access and security settings

        :param projectTemplateUid: string (required), path.
        :param body: EditProjectSecuritySettingsDtoV2 (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectSecuritySettingsDtoV2
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/accessSettings"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectSecuritySettingsDtoV2(**r)

    def getProjectTemplate(
        self,
        projectTemplateUid: str,
        phrase_token: Optional[str] = None,
    ) -> ProjectTemplateDto:
        """
        Get project template
        Note: importSettings in response is deprecated and will be always null
        :param projectTemplateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTemplateDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTemplateDto(**r)

    def editProjectTemplate(
        self,
        projectTemplateUid: str,
        body: ProjectTemplateEditDto,
        phrase_token: Optional[str] = None,
    ) -> ProjectTemplateDto:
        """
        Edit project template

        :param projectTemplateUid: string (required), path.
        :param body: ProjectTemplateEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTemplateDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTemplateDto(**r)

    def deleteProjectTemplate(
        self,
        projectTemplateUid: str,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete project template

        :param projectTemplateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def getAnalyseSettingsForProjectTemplate(
        self,
        projectTemplateUid: str,
        phrase_token: Optional[str] = None,
    ) -> AbstractAnalyseSettingsDto:
        """
        Get analyse settings

        :param projectTemplateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AbstractAnalyseSettingsDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/analyseSettings"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AbstractAnalyseSettingsDto(**r)

    def updateAnalyseSettingsForProjectTemplate(
        self,
        projectTemplateUid: str,
        body: EditAnalyseSettingsDto,
        phrase_token: Optional[str] = None,
    ) -> AbstractAnalyseSettingsDto:
        """
        Edit analyse settings

        :param projectTemplateUid: string (required), path.
        :param body: EditAnalyseSettingsDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AbstractAnalyseSettingsDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/analyseSettings"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AbstractAnalyseSettingsDto(**r)

    def getImportSettingsForProjectTemplate(
        self,
        projectTemplateUid: str,
        phrase_token: Optional[str] = None,
    ) -> FileImportSettingsDto:
        """
        Get import settings

        :param projectTemplateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: FileImportSettingsDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/importSettings"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return FileImportSettingsDto(**r)

    def getMachineTranslateSettingsForProjectTemplate(
        self,
        projectTemplateUid: str,
        phrase_token: Optional[str] = None,
    ) -> MTSettingsPerLanguageListDto:
        """
        Get project template machine translate settings

        :param projectTemplateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: MTSettingsPerLanguageListDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/mtSettings"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return MTSettingsPerLanguageListDto(**r)

    def setProjectTemplateTransMemoriesV2(
        self,
        projectTemplateUid: str,
        body: SetProjectTemplateTransMemoriesV2Dto,
        phrase_token: Optional[str] = None,
    ) -> ProjectTemplateTransMemoryListV2Dto:
        """
        Edit translation memories
        If user wants to edit “All target languages” or "All workflow steps”,
                       but there are already varied TM settings for individual languages or steps,
                       then the user risks to overwrite these individual choices.
        :param projectTemplateUid: string (required), path.
        :param body: SetProjectTemplateTransMemoriesV2Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTemplateTransMemoryListV2Dto
        """
        endpoint = f"/api2/v2/projectTemplates/{projectTemplateUid}/transMemories"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTemplateTransMemoryListV2Dto(**r)

    def getPreTranslateSettingsForProjectTemplate_2(
        self,
        projectTemplateUid: str,
        phrase_token: Optional[str] = None,
    ) -> PreTranslateSettingsV3Dto:
        """
        Get Pre-translate settings

        :param projectTemplateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PreTranslateSettingsV3Dto
        """
        endpoint = (
            f"/api2/v3/projectTemplates/{projectTemplateUid}/preTranslateSettings"
        )
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PreTranslateSettingsV3Dto(**r)

    def updatePreTranslateSettingsForProjectTemplate_2(
        self,
        projectTemplateUid: str,
        body: PreTranslateSettingsV3Dto,
        phrase_token: Optional[str] = None,
    ) -> PreTranslateSettingsV3Dto:
        """
        Update Pre-translate settings

        :param projectTemplateUid: string (required), path.
        :param body: PreTranslateSettingsV3Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PreTranslateSettingsV3Dto
        """
        endpoint = (
            f"/api2/v3/projectTemplates/{projectTemplateUid}/preTranslateSettings"
        )
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PreTranslateSettingsV3Dto(**r)

    def getProjectTemplateTransMemories_2(
        self,
        projectTemplateUid: str,
        wfStepUid: str = None,
        targetLang: str = None,
        phrase_token: Optional[str] = None,
    ) -> ProjectTemplateTransMemoryListDtoV3:
        """
        Get translation memories

        :param projectTemplateUid: string (required), path.
        :param wfStepUid: string (optional), query. Filter project translation memories by workflow step.
        :param targetLang: string (optional), query. Filter project translation memories by target language.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTemplateTransMemoryListDtoV3
        """
        endpoint = f"/api2/v3/projectTemplates/{projectTemplateUid}/transMemories"
        params = {"targetLang": targetLang, "wfStepUid": wfStepUid}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTemplateTransMemoryListDtoV3(**r)
