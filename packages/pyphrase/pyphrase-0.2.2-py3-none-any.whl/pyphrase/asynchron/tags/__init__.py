from .additional_workflow_step import AdditionalWorkflowStepOperations
from .analysis import AnalysisOperations
from .async_request import AsyncRequestOperations
from .authentication import AuthenticationOperations
from .bilingual_file import BilingualFileOperations
from .business_unit import BusinessUnitOperations
from .client import ClientOperations
from .connector import ConnectorOperations
from .conversations import ConversationsOperations
from .cost_center import CostCenterOperations
from .custom_file_type import CustomFileTypeOperations
from .domain import DomainOperations
from .email_template import EmailTemplateOperations
from .file import FileOperations
from .glossary import GlossaryOperations
from .import_settings import ImportSettingsOperations
from .job import JobOperations
from .language_quality_assessment import LanguageQualityAssessmentOperations
from .machine_translation import MachineTranslationOperations
from .machine_translation_settings import MachineTranslationSettingsOperations
from .mapping import MappingOperations
from .net_rate_scheme import NetRateSchemeOperations
from .price_list import PriceListOperations
from .project import ProjectOperations
from .project_reference_file import ProjectReferenceFileOperations
from .project_template import ProjectTemplateOperations
from .provider import ProviderOperations
from .quality_assurance import QualityAssuranceOperations
from .quote import QuoteOperations
from .scim import ScimOperations
from .segmentation_rules import SegmentationRulesOperations
from .spell_check import SpellCheckOperations
from .subdomain import SubdomainOperations
from .supported_languages import SupportedLanguagesOperations
from .term_base import TermBaseOperations
from .translation import TranslationOperations
from .translation_memory import TranslationMemoryOperations
from .user import UserOperations
from .vendor import VendorOperations
from .webhook import WebhookOperations
from .workflow_changes import WorkflowChangesOperations
from .workflow_step import WorkflowStepOperations

all = [
    AdditionalWorkflowStepOperations,
    AnalysisOperations,
    AsyncRequestOperations,
    AuthenticationOperations,
    BilingualFileOperations,
    BusinessUnitOperations,
    ClientOperations,
    ConnectorOperations,
    ConversationsOperations,
    CostCenterOperations,
    CustomFileTypeOperations,
    NetRateSchemeOperations,
    DomainOperations,
    EmailTemplateOperations,
    JobOperations,
    FileOperations,
    GlossaryOperations,
    TranslationMemoryOperations,
    SupportedLanguagesOperations,
    LanguageQualityAssessmentOperations,
    QualityAssuranceOperations,
    MachineTranslationSettingsOperations,
    MachineTranslationOperations,
    MappingOperations,
    ImportSettingsOperations,
    ProjectOperations,
    TranslationOperations,
    TermBaseOperations,
    ProjectReferenceFileOperations,
    ProjectTemplateOperations,
    QuoteOperations,
    ScimOperations,
    SegmentationRulesOperations,
    SpellCheckOperations,
    SubdomainOperations,
    PriceListOperations,
    UserOperations,
    VendorOperations,
    WebhookOperations,
    WorkflowStepOperations,
    WorkflowChangesOperations,
    ProviderOperations,
]
