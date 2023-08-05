from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    AbstractProjectDto,
    AbstractProjectDtoV2,
    AddTargetLangDto,
    AddWorkflowStepsDto,
    AnalyseSettingsDto,
    AssignableTemplatesDto,
    AssignVendorDto,
    AsyncRequestWrapperV2Dto,
    CloneProjectDto,
    CreateProjectFromTemplateAsyncV2Dto,
    CreateProjectFromTemplateV2Dto,
    CreateProjectV3Dto,
    EditProjectMTSettingsDto,
    EditProjectMTSettPerLangListDto,
    EditProjectSecuritySettingsDtoV2,
    EditProjectV2Dto,
    EditQASettingsDtoV2,
    EnabledQualityChecksDto,
    FileImportSettingsCreateDto,
    FileImportSettingsDto,
    FileNamingSettingsDto,
    FinancialSettingsDto,
    JobPartReferences,
    JobPartsDto,
    LqaSettingsDto,
    MTSettingsPerLanguageListDto,
    PageDtoAbstractProjectDto,
    PageDtoAnalyseReference,
    PageDtoProviderReference,
    PageDtoQuoteDto,
    PageDtoTermBaseDto,
    PageDtoTransMemoryDto,
    PatchProjectDto,
    PreTranslateSettingsV3Dto,
    ProjectSecuritySettingsDtoV2,
    ProjectTermBaseListDto,
    ProjectTransMemoryListDtoV3,
    ProjectWorkflowStepListDtoV2,
    ProviderListDtoV2,
    QASettingsDtoV2,
    SearchResponseListTmDto,
    SearchTMRequestDto,
    SetFinancialSettingsDto,
    SetProjectStatusDto,
    SetProjectTransMemoriesV3Dto,
    SetTermBaseDto,
)


class ProjectOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def assignLinguistsFromTemplateToJobParts(
        self,
        projectUid: str,
        templateUid: str,
        body: JobPartReferences,
        phrase_token: Optional[str] = None,
    ) -> JobPartsDto:
        """
        Assigns providers from template (specific jobs)

        :param projectUid: string (required), path.
        :param templateUid: string (required), path.
        :param body: JobPartReferences (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: JobPartsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/applyTemplate/{templateUid}/assignProviders/forJobParts"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return JobPartsDto(**r)

    async def listProjects(
        self,
        nameOrInternalId: str = None,
        buyerId: int = None,
        jobStatusGroup: str = None,
        jobStatuses: List[str] = None,
        ownerId: int = None,
        sourceLangs: List[str] = None,
        createdInLastHours: int = None,
        dueInHours: int = None,
        costCenterName: str = None,
        costCenterId: int = None,
        subDomainName: str = None,
        subDomainId: int = None,
        domainName: str = None,
        domainId: int = None,
        targetLangs: List[str] = None,
        statuses: List[str] = None,
        businessUnitName: str = None,
        businessUnitId: int = None,
        clientName: str = None,
        clientId: int = None,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        includeArchived: bool = "False",
        archivedOnly: bool = "False",
        phrase_token: Optional[str] = None,
    ) -> PageDtoAbstractProjectDto:
        """
        List projects

        :param nameOrInternalId: string (optional), query. Name or internal ID of project.
        :param buyerId: integer (optional), query.
        :param jobStatusGroup: string (optional), query. Allowed for linguists only.
        :param jobStatuses: array (optional), query. Allowed for linguists only.
        :param ownerId: integer (optional), query.
        :param sourceLangs: array (optional), query.
        :param createdInLastHours: integer (optional), query.
        :param dueInHours: integer (optional), query. -1 for projects that are overdue.
        :param costCenterName: string (optional), query.
        :param costCenterId: integer (optional), query.
        :param subDomainName: string (optional), query.
        :param subDomainId: integer (optional), query.
        :param domainName: string (optional), query.
        :param domainId: integer (optional), query.
        :param targetLangs: array (optional), query.
        :param statuses: array (optional), query.
        :param businessUnitName: string (optional), query.
        :param businessUnitId: integer (optional), query.
        :param clientName: string (optional), query.
        :param clientId: integer (optional), query.
        :param name: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.
        :param includeArchived: boolean (optional), query. List also archived projects.
        :param archivedOnly: boolean (optional), query. List only archived projects, regardless of `includeArchived`.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoAbstractProjectDto
        """
        endpoint = f"/api2/v1/projects"
        params = {
            "name": name,
            "clientId": clientId,
            "clientName": clientName,
            "businessUnitId": businessUnitId,
            "businessUnitName": businessUnitName,
            "statuses": statuses,
            "targetLangs": targetLangs,
            "domainId": domainId,
            "domainName": domainName,
            "subDomainId": subDomainId,
            "subDomainName": subDomainName,
            "costCenterId": costCenterId,
            "costCenterName": costCenterName,
            "dueInHours": dueInHours,
            "createdInLastHours": createdInLastHours,
            "sourceLangs": sourceLangs,
            "ownerId": ownerId,
            "jobStatuses": jobStatuses,
            "jobStatusGroup": jobStatusGroup,
            "buyerId": buyerId,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "nameOrInternalId": nameOrInternalId,
            "includeArchived": includeArchived,
            "archivedOnly": archivedOnly,
        }

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoAbstractProjectDto(**r)

    async def getProject(
        self, projectUid: str, phrase_token: Optional[str] = None
    ) -> AbstractProjectDto:
        """
        Get project

        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AbstractProjectDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AbstractProjectDto(**r)

    async def deleteProject(
        self, projectUid: str, purge: bool = "False", phrase_token: Optional[str] = None
    ) -> None:
        """
        Delete project

        :param projectUid: string (required), path.
        :param purge: boolean (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}"
        params = {"purge": purge}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def patchProject(
        self, projectUid: str, body: PatchProjectDto, phrase_token: Optional[str] = None
    ) -> AbstractProjectDto:
        """
        Edit project

        :param projectUid: string (required), path.
        :param body: PatchProjectDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AbstractProjectDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.patch(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AbstractProjectDto(**r)

    async def addTargetLanguageToProject(
        self,
        projectUid: str,
        body: AddTargetLangDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Add target languages
        Add target languages to project
        :param projectUid: string (required), path.
        :param body: AddTargetLangDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/targetLangs"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def addWorkflowSteps(
        self,
        projectUid: str,
        body: AddWorkflowStepsDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Add workflow steps

        :param projectUid: string (required), path.
        :param body: AddWorkflowStepsDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/workflowSteps"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def assignVendorToProject(
        self, projectUid: str, body: AssignVendorDto, phrase_token: Optional[str] = None
    ) -> None:
        """
                Assign vendor
                To unassign Vendor from Project, use empty body:
        ```
        {}
        ```
                :param projectUid: string (required), path.
                :param body: AssignVendorDto (required), body.

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/assignVendor"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def cloneProject(
        self, projectUid: str, body: CloneProjectDto, phrase_token: Optional[str] = None
    ) -> AbstractProjectDto:
        """
        Clone project

        :param projectUid: string (required), path.
        :param body: CloneProjectDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AbstractProjectDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/clone"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AbstractProjectDto(**r)

    async def getProjectAssignments(
        self,
        projectUid: str,
        providerName: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoProviderReference:
        """
        List project providers

        :param projectUid: string (required), path.
        :param providerName: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoProviderReference
        """
        endpoint = f"/api2/v1/projects/{projectUid}/providers"
        params = {
            "providerName": providerName,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoProviderReference(**r)

    async def setProjectStatus(
        self,
        projectUid: str,
        body: SetProjectStatusDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Edit project status

        :param projectUid: string (required), path.
        :param body: SetProjectStatusDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/setStatus"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def assignableTemplates(
        self, projectUid: str, phrase_token: Optional[str] = None
    ) -> AssignableTemplatesDto:
        """
        List assignable templates

        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AssignableTemplatesDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/assignableTemplates"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AssignableTemplatesDto(**r)

    async def assignLinguistsFromTemplate(
        self, projectUid: str, templateUid: str, phrase_token: Optional[str] = None
    ) -> JobPartsDto:
        """
        Assigns providers from template

        :param projectUid: string (required), path.
        :param templateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: JobPartsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/applyTemplate/{templateUid}/assignProviders"
        params = {}

        files = None
        payload = None

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return JobPartsDto(**r)

    async def getFinancialSettings(
        self, projectUid: str, phrase_token: Optional[str] = None
    ) -> FinancialSettingsDto:
        """
        Get financial settings

        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: FinancialSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/financialSettings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return FinancialSettingsDto(**r)

    async def setFinancialSettings(
        self,
        projectUid: str,
        body: SetFinancialSettingsDto,
        phrase_token: Optional[str] = None,
    ) -> FinancialSettingsDto:
        """
        Edit financial settings

        :param projectUid: string (required), path.
        :param body: SetFinancialSettingsDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: FinancialSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/financialSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return FinancialSettingsDto(**r)

    async def enabledQualityChecks(
        self, projectUid: str, phrase_token: Optional[str] = None
    ) -> EnabledQualityChecksDto:
        """
        Get QA checks
        Returns enabled quality assurance settings.
        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: EnabledQualityChecksDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/qaSettingsChecks"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return EnabledQualityChecksDto(**r)

    async def getProjectSettings(
        self,
        projectUid: str,
        workflowLevel: int = "1",
        phrase_token: Optional[str] = None,
    ) -> LqaSettingsDto:
        """
        Get LQA settings

        :param projectUid: string (required), path.
        :param workflowLevel: integer (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LqaSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/lqaSettings"
        params = {"workflowLevel": workflowLevel}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LqaSettingsDto(**r)

    async def getMtSettingsForProject(
        self, projectUid: str, phrase_token: Optional[str] = None
    ) -> MTSettingsPerLanguageListDto:
        """
        Get project machine translate settings

        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: MTSettingsPerLanguageListDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/mtSettings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return MTSettingsPerLanguageListDto(**r)

    async def setMtSettingsForProject(
        self,
        projectUid: str,
        body: EditProjectMTSettingsDto,
        phrase_token: Optional[str] = None,
    ) -> MTSettingsPerLanguageListDto:
        """
        Edit machine translate settings
        This will erase all mtSettings per language for project.
        To remove all machine translate settings from project call without a machineTranslateSettings parameter.
        :param projectUid: string (required), path.
        :param body: EditProjectMTSettingsDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: MTSettingsPerLanguageListDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/mtSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return MTSettingsPerLanguageListDto(**r)

    async def getQuotesForProject(
        self,
        projectUid: str,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoQuoteDto:
        """
        List quotes

        :param projectUid: string (required), path.
        :param pageNumber: integer (optional), query.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoQuoteDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/quotes"
        params = {"pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoQuoteDto(**r)

    async def setMtSettingsPerLanguageForProject(
        self,
        projectUid: str,
        body: EditProjectMTSettPerLangListDto,
        phrase_token: Optional[str] = None,
    ) -> MTSettingsPerLanguageListDto:
        """
        Edit machine translate settings per language
        This will erase mtSettings for project
        :param projectUid: string (required), path.
        :param body: EditProjectMTSettPerLangListDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: MTSettingsPerLanguageListDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/mtSettingsPerLanguage"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return MTSettingsPerLanguageListDto(**r)

    async def getAnalyseSettingsForProject(
        self, projectUid: str, phrase_token: Optional[str] = None
    ) -> AnalyseSettingsDto:
        """
        Get analyse settings

        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AnalyseSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/analyseSettings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AnalyseSettingsDto(**r)

    async def getImportSettings_2(
        self, projectUid: str, phrase_token: Optional[str] = None
    ) -> FileImportSettingsDto:
        """
        Get projects's default import settings

        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: FileImportSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/importSettings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return FileImportSettingsDto(**r)

    async def editImportSettings_1(
        self,
        projectUid: str,
        body: FileImportSettingsCreateDto,
        phrase_token: Optional[str] = None,
    ) -> FileImportSettingsDto:
        """
        Edit project import settings

        :param projectUid: string (required), path.
        :param body: FileImportSettingsCreateDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: FileImportSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/importSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return FileImportSettingsDto(**r)

    async def getFileNamingSettings(
        self, projectUid: str, phrase_token: Optional[str] = None
    ) -> FileNamingSettingsDto:
        """
        Get file naming settings for project

        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: FileNamingSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/fileNamingSettings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return FileNamingSettingsDto(**r)

    async def updateFileNamingSettings(
        self,
        projectUid: str,
        body: FileNamingSettingsDto,
        phrase_token: Optional[str] = None,
    ) -> FileNamingSettingsDto:
        """
        Update file naming settings for project

        :param projectUid: string (required), path.
        :param body: FileNamingSettingsDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: FileNamingSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/fileNamingSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return FileNamingSettingsDto(**r)

    async def getProjectTermBases(
        self, projectUid: str, phrase_token: Optional[str] = None
    ) -> ProjectTermBaseListDto:
        """
        Get term bases

        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTermBaseListDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/termBases"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTermBaseListDto(**r)

    async def setProjectTermBases(
        self, projectUid: str, body: SetTermBaseDto, phrase_token: Optional[str] = None
    ) -> ProjectTermBaseListDto:
        """
        Edit term bases

        :param projectUid: string (required), path.
        :param body: SetTermBaseDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTermBaseListDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/termBases"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTermBaseListDto(**r)

    async def relevantTermBases(
        self,
        projectUid: str,
        targetLangs: List[str] = None,
        subDomainName: str = None,
        clientName: str = None,
        domainName: str = None,
        name: str = None,
        strictLangMatching: bool = "False",
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoTermBaseDto:
        """
        List project relevant term bases

        :param projectUid: string (required), path.
        :param targetLangs: array (optional), query.
        :param subDomainName: string (optional), query.
        :param clientName: string (optional), query.
        :param domainName: string (optional), query.
        :param name: string (optional), query.
        :param strictLangMatching: boolean (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoTermBaseDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/termBases/relevant"
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

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoTermBaseDto(**r)

    async def relevantTransMemories_1(
        self,
        projectUid: str,
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
        List project relevant translation memories

        :param projectUid: string (required), path.
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
        endpoint = f"/api2/v1/projects/{projectUid}/transMemories/relevant"
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

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoTransMemoryDto(**r)

    async def searchSegment_1(
        self,
        projectUid: str,
        body: SearchTMRequestDto,
        phrase_token: Optional[str] = None,
    ) -> SearchResponseListTmDto:
        """
        Search translation memory for segment in the project
        Returns at most <i>maxSegments</i>
            records with <i>score >= scoreThreshold</i> and at most <i>maxSubsegments</i> records which are subsegment,
            i.e. the source text is substring of the query text.
        :param projectUid: string (required), path.
        :param body: SearchTMRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SearchResponseListTmDto
        """
        endpoint = (
            f"/api2/v1/projects/{projectUid}/transMemories/searchSegmentInProject"
        )
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SearchResponseListTmDto(**r)

    async def setProjectQASettingsV2(
        self,
        projectUid: str,
        body: EditQASettingsDtoV2,
        phrase_token: Optional[str] = None,
    ) -> QASettingsDtoV2:
        """
        Edit quality assurance settings

        :param projectUid: string (required), path.
        :param body: EditQASettingsDtoV2 (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: QASettingsDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/qaSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return QASettingsDtoV2(**r)

    async def createProjectFromTemplateV2(
        self,
        templateUid: str,
        body: CreateProjectFromTemplateV2Dto,
        phrase_token: Optional[str] = None,
    ) -> AbstractProjectDtoV2:
        """
        Create project from template

        :param templateUid: string (required), path.
        :param body: CreateProjectFromTemplateV2Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AbstractProjectDtoV2
        """
        endpoint = f"/api2/v2/projects/applyTemplate/{templateUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AbstractProjectDtoV2(**r)

    async def createProjectFromTemplateV2Async(
        self,
        templateUid: str,
        body: CreateProjectFromTemplateAsyncV2Dto,
        phrase_token: Optional[str] = None,
    ) -> AsyncRequestWrapperV2Dto:
        """
        Create project from template (async)

        :param templateUid: string (required), path.
        :param body: CreateProjectFromTemplateAsyncV2Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AsyncRequestWrapperV2Dto
        """
        endpoint = f"/api2/v2/projects/applyTemplate/async/{templateUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AsyncRequestWrapperV2Dto(**r)

    async def getProjectAccessSettingsV2(
        self, projectUid: str, phrase_token: Optional[str] = None
    ) -> ProjectSecuritySettingsDtoV2:
        """
        Get access and security settings

        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectSecuritySettingsDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/accessSettings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectSecuritySettingsDtoV2(**r)

    async def editProjectAccessSettingsV2(
        self,
        projectUid: str,
        body: EditProjectSecuritySettingsDtoV2,
        phrase_token: Optional[str] = None,
    ) -> ProjectSecuritySettingsDtoV2:
        """
        Edit access and security settings

        :param projectUid: string (required), path.
        :param body: EditProjectSecuritySettingsDtoV2 (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectSecuritySettingsDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/accessSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectSecuritySettingsDtoV2(**r)

    async def getProjectWorkflowStepsV2(
        self,
        projectUid: str,
        withAssignedJobs: bool = "False",
        phrase_token: Optional[str] = None,
    ) -> ProjectWorkflowStepListDtoV2:
        """
        Get workflow steps

        :param projectUid: string (required), path.
        :param withAssignedJobs: boolean (optional), query. Return only steps containing jobs assigned to the calling linguist..

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectWorkflowStepListDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/workflowSteps"
        params = {"withAssignedJobs": withAssignedJobs}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectWorkflowStepListDtoV2(**r)

    async def editProjectV2(
        self,
        projectUid: str,
        body: EditProjectV2Dto,
        phrase_token: Optional[str] = None,
    ) -> AbstractProjectDtoV2:
        """
        Edit project

        :param projectUid: string (required), path.
        :param body: EditProjectV2Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AbstractProjectDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AbstractProjectDtoV2(**r)

    async def listProviders_3(
        self, projectUid: str, phrase_token: Optional[str] = None
    ) -> ProviderListDtoV2:
        """
        Get suggested providers

        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProviderListDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/providers/suggest"
        params = {}

        files = None
        payload = None

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProviderListDtoV2(**r)

    async def getPreTranslateSettingsForProject_2(
        self, projectUid: str, phrase_token: Optional[str] = None
    ) -> PreTranslateSettingsV3Dto:
        """
        Get Pre-translate settings

        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PreTranslateSettingsV3Dto
        """
        endpoint = f"/api2/v3/projects/{projectUid}/preTranslateSettings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PreTranslateSettingsV3Dto(**r)

    async def editProjectPreTranslateSettings_2(
        self,
        projectUid: str,
        body: PreTranslateSettingsV3Dto,
        phrase_token: Optional[str] = None,
    ) -> PreTranslateSettingsV3Dto:
        """
        Update Pre-translate settings

        :param projectUid: string (required), path.
        :param body: PreTranslateSettingsV3Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PreTranslateSettingsV3Dto
        """
        endpoint = f"/api2/v3/projects/{projectUid}/preTranslateSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PreTranslateSettingsV3Dto(**r)

    async def createProjectV3(
        self, body: CreateProjectV3Dto, phrase_token: Optional[str] = None
    ) -> AbstractProjectDtoV2:
        """
        Create project

        :param body: CreateProjectV3Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AbstractProjectDtoV2
        """
        endpoint = f"/api2/v3/projects"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AbstractProjectDtoV2(**r)

    async def listByProjectV3(
        self,
        projectUid: str,
        onlyOwnerOrg: bool = None,
        uid: str = None,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        sort: str = "DATE_CREATED",
        order: str = "desc",
        phrase_token: Optional[str] = None,
    ) -> PageDtoAnalyseReference:
        """
        List analyses by project

        :param projectUid: string (required), path.
        :param onlyOwnerOrg: boolean (optional), query.
        :param uid: string (optional), query. Uid to search by.
        :param name: string (optional), query. Name to search by.
        :param pageNumber: integer (optional), query.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.
        :param sort: string (optional), query. Sorting field.
        :param order: string (optional), query. Sorting order.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoAnalyseReference
        """
        endpoint = f"/api2/v3/projects/{projectUid}/analyses"
        params = {
            "name": name,
            "uid": uid,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "sort": sort,
            "order": order,
            "onlyOwnerOrg": onlyOwnerOrg,
        }

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoAnalyseReference(**r)

    async def getProjectTransMemories_1(
        self,
        projectUid: str,
        wfStepUid: str = None,
        targetLang: str = None,
        phrase_token: Optional[str] = None,
    ) -> ProjectTransMemoryListDtoV3:
        """
        Get translation memories

        :param projectUid: string (required), path.
        :param wfStepUid: string (optional), query. Filter project translation memories by workflow step.
        :param targetLang: string (optional), query. Filter project translation memories by target language.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTransMemoryListDtoV3
        """
        endpoint = f"/api2/v3/projects/{projectUid}/transMemories"
        params = {"targetLang": targetLang, "wfStepUid": wfStepUid}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTransMemoryListDtoV3(**r)

    async def setProjectTransMemoriesV3(
        self,
        projectUid: str,
        body: SetProjectTransMemoriesV3Dto,
        phrase_token: Optional[str] = None,
    ) -> ProjectTransMemoryListDtoV3:
        """
        Edit translation memories
        If user wants to edit “All target languages” or "All workflow steps”,
                       but there are already varied TM settings for individual languages or steps,
                       then the user risks to overwrite these individual choices.
        :param projectUid: string (required), path.
        :param body: SetProjectTransMemoriesV3Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTransMemoryListDtoV3
        """
        endpoint = f"/api2/v3/projects/{projectUid}/transMemories"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTransMemoryListDtoV3(**r)
