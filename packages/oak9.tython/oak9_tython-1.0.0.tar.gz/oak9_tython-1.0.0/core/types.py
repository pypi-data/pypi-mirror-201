import uuid
from models.shared.shared_pb2 import Blueprint as BP
from models.shared.shared_pb2 import ValidationMetaInfo
from models.shared.shared_pb2 import Graph, VertexType, Vertex
from models.shared.shared_pb2 import Context as Ctx
from dataclasses import dataclass, field
from enum import Enum, unique
from typing import List, Tuple, ClassVar, Callable, Dict, Union, Set, Any
from colorama import Fore, Style


ValidationFunction = Callable[[any], any]


@unique
class Capabilities(Enum):
    ACCESS_ENFORCEMENT = (
        'Oak9',
        'AE',
        2,
        [
            # TODO: (immutableT) Add the remaining ones.
            # This CR has many check functions, but many are stubs.
            # Come back here once we remove un-implemented checks.
            'check_access_policy_enforcement',
        ])
    APPLICATION_LAYER_ENCRYPTION = ('Oak9', 'DAR', 2, ['check_application_layer_encryption'])
    ASSET_INVENTORY = ('Oak9', 'AI', 1, ['check_asset_inventory'])
    AUTHENTICATION = ('Oak9', 'IA', 1, ['check_identification_and_authentication'])
    AUTHENTICATION_PROTECTION = ('Oak9', 'IA', 2, ['check_protect_authenticators'])
    BACKUP = ('Oak9', 'BR', 2, ['check_backups'])
    DATA_ENCRYPTION_AT_REST = ('Oak9', 'DAR', 1, ['check_transparent_data_encryption'])
    DATA_MINIMIZATION = ('Oak9', 'DM', 1, ['check_data_minimization_enabled'])
    DATA_SANITIZATION = ('Oak9', 'DAR', 4, ['check_securely_remove_data'])
    DENIAL_OF_SERVICE = ('Oak9', 'DOS', 1, ['check_load_balancing', 'check_ip_whitelisting'])
    FIREWALLS = ('Oak9', 'IFE', 1, ['check_firewalls'])
    HARDENING = ('Oak9', 'CM', 1, ['check_hardening'])
    HIGH_AVAILABILITY = ('Oak9', 'BR', 1, ['check_auto_scaling', 'check_high_availability'])
    IDENTIFICATION_AND_AUTHORIZATION = ('Oak9', 'IA', 1, [])
    IDENTITY_LIFECYCLE = ('Oak9', 'ILM', 1, ['check_identity_lifecycle_management'])
    INFORMATION_SYSTEMS_ENFORCING_NETWORK_ACCESS = ('Oak9', 'IFE', 10, ['check_subnet_isolation_enabled'])
    KEY_MANAGEMENT = ('Oak9', 'KM', 1, ['check_protect_cryptographic_keys'])
    LOGGING = ('Oak9', 'AA', 2, ['check_logging', 'check_log_integrity'])
    NETWORK_INFORMATION_FLOW_ENFORCEMENT = ('Oak9', 'IFE', 9, ['check_subnet_isolation_enabled'])
    PRIVILEGED_ACCESS_MANAGEMENT = ('Oak9', 'AE', 3, ['check_privileged_access_management'])
    ROLE_BASED_ACCESS_CONTROL = ('Oak9', 'ILM', 2, ['check_role_based_access_control'])
    SESSION_MANAGEMENT = ('Oak9', 'AE', 1, ['check_session_management'])
    TLS = ('Oak9', 'DIT', 1, ['check_tls', 'check_destination_authentication', 'check_source_authentication'])

    def __init__(self, company: str, category: str, index: int, validation_functions: list[str]):
        self.company = company
        self.category = category
        self.index = index
        self.validation_functions = list(validation_functions)

    def __str__(self):
        return f'{self.company}.CR.{self.category}.{self.index}'

    @property
    def id(self) -> str:
        return f'{self.company}.CR.{self.category}.{self.index}'


class OrderedEnum(Enum):

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

class Csp(Enum):
    Aws = 1
    Azure = 2


class DataSensitivity(OrderedEnum):
    Sensitive = 2
    NonSensitive = 1


class BusinessImpact(OrderedEnum):
    High = 3
    Medium = 2
    Low = 1


class DeploymentModel(OrderedEnum):
    Private = 3
    Hybrid = 2
    Public = 1


class SecurityLevel(OrderedEnum):
    Best = 3
    Better = 2
    Good = 1


class Context:

    def __init__(self, context: Ctx = None):
        """_summary_
        Context object that will be populated by the proto project_context object. This object is based on the
        security teams context definition located in the teams component template. 
        
        Component Template: https://github.com/oak9io/oak9.cf/blob/aeab1f1bf598719c8b2d16a70c9161f61755db5a/component_mappings/COMPONENT_MAPPING_TEMPLATE.jsonc#L26
          
        Args:
            context (context_pb2): The proto context object is passed in and converted into a python object
        """

        #  Default context
        if not context:
            self.business_impact: BusinessImpact = BusinessImpact.High
            self.data_sensitivity: DataSensitivity = DataSensitivity.Sensitive
            self.deployment_model: DeploymentModel = DeploymentModel.Public
            self.security_level: SecurityLevel = SecurityLevel.Good
            self.internal_access = True
            self.external_access = False
            self.remote_access = False
            self.wireless_access = False
            self.outbound_access = False
            self.workforce = True
            self.consumers = True
            self.business_partners = True
            self.physical = False
            self.open = False
            self.limited_sensitive_data = False
            self.broad_sensitive_data = True
            self.security_privileged = True
            self.component_core = True
            self.user_interface = True
            self.management_interface = True
            return

        # Proto context object is provided
        if context.susceptibility.business_impact.lower() == "high":
            self.business_impact: BusinessImpact = BusinessImpact.High
        elif context.susceptibility.business_impact.lower() == "medium":
            self.business_impact: BusinessImpact = BusinessImpact.Medium
        else:
            self.business_impact: BusinessImpact = BusinessImpact.Low

        if context.susceptibility.data_sensitivity.lower() == "businesssensitive":
            self.data_sensitivity = DataSensitivity.Sensitive
        else:
            self.data_sensitivity = DataSensitivity.NonSensitive

        if context.app_architecture.deployment_model.lower() == "private":
            self.deployment_model: DeploymentModel = DeploymentModel.Private
        elif context.app_architecture.deployment_model.lower() == "hybrid":
            self.deployment_model: DeploymentModel = DeploymentModel.Hybrid
        else:
            self.deployment_model: DeploymentModel = DeploymentModel.Public

        if context.security_architecture.security_level.lower() == "better":
            self.security_level: SecurityLevel = SecurityLevel.Better
        elif context.security_architecture.security_level.lower() == "best":
            self.security_level: SecurityLevel = SecurityLevel.Best
        else:
            self.security_level: SecurityLevel = SecurityLevel.Good

        self.internal_access = context.accessibility.access_type.internal_access.lower() == "required"
        self.external_access = context.accessibility.access_type.external_access.lower() == "required"
        self.remote_access = context.accessibility.access_type.remote_access.lower() == "required"
        self.wireless_access = context.accessibility.access_type.wireless_access.lower() == "required"
        self.outbound_access = context.accessibility.access_type.outbound_access.lower() == "required"

        self.workforce = context.accessibility.end_users.workforce.lower() == "required"
        self.consumers = context.accessibility.end_users.consumers.lower() == "required"
        self.business_partners = context.accessibility.end_users.business_partners.lower() == "required"

        self.physical = context.accessibility.level_of_access.physical.lower() == "required"
        self.open = context.accessibility.level_of_access.open.lower() == "required"
        self.limited_sensitive_data = context.accessibility.level_of_access.limited_sensitive_data.lower() == "required"
        self.broad_sensitive_data = context.accessibility.level_of_access.broad_sensitive_data.lower() == "required"
        self.security_privileged = context.accessibility.level_of_access.security_privileged.lower() == "required"

        self.component_core = context.accessibility.applicable_component_slices.component_core.lower() == "required"
        self.user_interface = context.accessibility.applicable_component_slices.user_interface.lower() == "required"
        self.management_interface = \
            context.accessibility.applicable_component_slices.management_interface.lower() == "required"

    def is_externally_accessible(self):
        if self.external_access and not self.internal_access:
            return True

        return False

    def is_data_sensitive(self):
        if self.data_sensitivity == DataSensitivity.Sensitive:
            return True
        return False

    def is_impact_high(self):

        if self.business_impact == BusinessImpact.High:
            return True

        return False

    def is_impact_moderate(self):

        if self.business_impact == BusinessImpact.Medium:
            return True

        return False

    def is_impact_low(self):

        if self.business_impact == BusinessImpact.Low:
            return True

        return False

    def is_business_critical(self):

        if self.business_impact == BusinessImpact.High and self.data_sensitivity == DataSensitivity.Sensitive:
            return True
        else:
            return False

    def is_impact_high_or_data_sensitive(self):

        if self.business_impact == BusinessImpact.High or self.data_sensitivity == DataSensitivity.Sensitive:
            return True
        else:
            return False

    def is_sensitive(self):
        if self.data_sensitivity == DataSensitivity.Sensitive:
            return True
        else:
            return False

    def is_sensitive_and_external(self):

        if self.data_sensitivity == DataSensitivity.Sensitive and self.external_access:
            return True
        else:
            return False

    def is_sensitive_and_internal(self):
        if self.data_sensitivity == DataSensitivity.Sensitive and self.internal_access:
            return True
        else:
            return False

    def determine_severity(self):

        if self.business_impact == BusinessImpact.High:
            config_violation_severity = Severity.High

        elif self.business_impact == BusinessImpact.Medium:
            config_violation_severity = Severity.Moderate

        else:
            config_violation_severity = Severity.Low

        return config_violation_severity


Default_Context = Context()


class BlueprintType(Enum):
    Component = 1
    Reference = 2
    Solution = 3
    Resource = 4
    Customer = 5



@dataclass
class Resource:
    id: str
    name: str
    csp: Csp
    resource_type: ClassVar[str]
    id: str
    name: str
    blueprint_id: str


class WellDoneRating(OrderedEnum):
    Amazing = 4
    Great = 3
    Good = 2
    Ok = 1


class Severity(OrderedEnum):
    Critical = 4
    High = 3
    Moderate = 2
    Low = 1


class RelatedConfig:
    """
    Related Configs allows the Violation to bundle additional configurations that don't need a separate violation
    and should be remediated together
    """
    config_id: str = ""
    config_value: Union[List, int, str] = ""
    preferred_value: Union[List, int, str] = ""
    comment: str = ""


class Violation:
    """
        Defines a violation object.
        This object is DEPRECATED and is only there for backwards compatibility
        Note that there are required and optional fields

        config_gap, config_impact, config_fix and oak9_guidance are all fields that support
        a specific markup for displaying design gaps correctly to the end user.  See link here:
        https://oak9.atlassian.net/wiki/spaces/SEC/pages/351240193/Violation+Markup+Support

    """

    def __init__(
            self,
            severity: Severity = Severity.Low,
            adjusted_severity: Severity = None,
            config_id: str = "",
            config_value: str = "",
            config_gap: str = "",
            config_impact: str = "",
            config_fix: str = "",
            preferred_value: Union[List, str, int] = "",
            additional_guidance: str = "",
            documentation: str = "",
            related_configs: List[RelatedConfig] = None,
            capability_id: str = "",
            capability_name: str = "",
            priority: int = 0
    ):

        # Severity of the violation.  Default to low. Severity should be determined based on the business context
        # Resource blueprints can also specify adjusted severity. When an adjusted severity is specified, it does
        # not allow the Component blueprint to set the severity for this violation.
        # Blueprint Author: REQUIRED
        self._severity = severity

        # Adjusted severity of the violation. This field is used by Resource blueprints to set the severity in a way
        # that higher level component or resource blueprints cannot modify.  This is to account for use-cases
        # it is clear from the resource blueprint that a mitigating design is in place so the resource blueprint can
        # account for that to force a severity
        # Blueprint Author: REQUIRED (Internal blueprint use only - this configuration does not get
        # propagated to the platform)
        self._adjusted_severity = adjusted_severity

        # the unique id (full path) of the configuration that has the issue
        # e.g. LoadBalancer.listeners[0].listenerCertificates[2].certificate[1].name
        # This field should be auto-populated using a utility function (get_config_id)
        # Blueprint Author: REQUIRED
        self.config_id = config_id

        # currently configure value of this configuration
        # Blueprint Author: REQUIRED
        if type(config_value) != str:
            self.config_value = str(config_value)

        else:
            self.config_value = config_value

        # Config gap is a description of the gap if the configuration(s) are
        # not set to the preferred values
        # See: https://oak9.atlassian.net/wiki/spaces/SEC/pages/243892225/Design+Gap+-+Hierarchy+and+Logic
        # config gaps should summarize the gap and possibly list the parent configuration that needs to be updated
        # Blueprint Author: OPTIONAL
        self.config_gap = config_gap

        # Document the impact of not fixing this violation
        # Blueprint Author: OPTIONAL
        self.config_impact = config_impact

        # Provide guidance on how to fix the issue
        # Blueprint Author: OPTIONAL
        self.config_fix = config_fix

        # oak9's preferred value
        # preferred values can be strings, integers, bools, lists, dictionaries
        # the platform is responsible for checking type to use-cases like remediation
        # or displaying design gaps
        # Blueprint Author: OPTIONAL (required for remediation)
        if type(preferred_value) == list:
            self.preferred_value = ', '.join(preferred_value)

        elif type(preferred_value) != str:
            self.preferred_value = str(preferred_value)

        else:
            self.preferred_value = preferred_value

        # Additional guidance (renamed from oak9 guidance)
        # Blueprint Author: OPTIONAL (required for remediation)
        self.additional_guidance = additional_guidance

        # Related configurations that should be remediated together and
        # are better presented bundled together
        # Blueprint Author: OPTIONAL
        self.related_configs: List[RelatedConfig] = related_configs

        """
        Configurations that are autopopulated and not populated by the blueprint author
        (Some could be populated in the Customer SaC use-case
        """

        # oak9 detailed requirement id
        # REQUIRED (for all oak9 blueprints)
        self._capability_id = capability_id

        # oak9 detailed requirement name
        # This is automatically populated on the platform side
        # In the future, we may use this for customer created blueprints
        self._capability_name = capability_name

        # add documentation link
        # This does not need to be populated
        # This will be auto-populated on the platform side
        self._documentation = documentation

        # Priority of finding to relatively prioritize across
        # qualitative ratings
        self._priority = priority

    @property
    def severity(self) -> Severity:
        return self._severity

    @severity.setter
    def severity(self, value):
        if self._adjusted_severity:
            self._severity = self._adjusted_severity
        else:
            self._severity = value

    @property
    def adjusted_severity(self):
        return self._adjusted_severity

    @adjusted_severity.setter
    def adjusted_severity(self, value):
        self._adjusted_severity = value

    @property
    def documentation(self):
        return self._documentation

    @property
    def capability_id(self):
        return self._capability_id

    @capability_id.setter
    def capability_id(self, value):
        self._capability_id = value

    @property
    def capability_name(self):
        return self._capability_name

    @capability_name.setter
    def capability_name(self, value):
        self._capability_name = value

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        if isinstance(value, int) and 101 > value > 0:
            self._priority = value


@dataclass
class DesignGap:
    # What is the  gap
    # Blueprint Author: OPTIONAL (For oak9 req ids only)
    capability_gap: str = ""
    # What is the impact
    # Blueprint Author: OPTIONAL (For oak9 req ids only)
    capability_impact: str = ""
    # severity of the design gap
    _severity: Severity = Severity.Low
    # List of violations
    violations: List[Violation] = field(default_factory=list)

    def add_violation(self, violations: List[Violation]):
        self.violations.extend(violations)
        self._update_severity()

    def _update_severity(self):
        for viol in self.violations:
            if viol.severity > self._severity:
                self._severity = viol.severity


class FindingType(Enum):
    DesignGap = 1
    Kudos = 2
    Warning = 3
    Task = 4
    ResourceGap = 5


class Finding:
    """
        Defines a observation object.
        Observations can be Violations, ResourceGaps or Passed Checks
        Note that there are required and optional fields

        config_gap, config_impact, config_fix and oak9_guidance are all fields that support
        a specific markup for displaying design gaps correctly to the end user.  See link here:
        https://oak9.atlassian.net/wiki/spaces/SEC/pages/351240193/Violation+Markup+Support

    """

    def __init__(
            self,
            finding_type: FindingType,
            desc: str,
            rating: Union[Severity, WellDoneRating] = Severity.Low,
            adjusted_severity: Severity = None,
            config_id: str = "",
            current_value: str = "",
            fix: str = "",
            preferred_value="",
            additional_guidance: str = "",
            related_configs: List[RelatedConfig] = None,
            related_findings: List[uuid.UUID] = None,
            req_id: str = "",
            req_name: str = "",
            priority: int = 0,
            documentation_url=""
    ):
        """
        Type of observation
        """

        self._id = uuid.uuid4()

        self._finding_type: FindingType = finding_type

        # For Design Gaps and Tasks: Severity of the gap or task.  Default to low. Severity should be determined based on the business context
        # Resource blueprints can also specify adjusted severity. When an adjusted severity is specified, it does
        # not allow the Component blueprint to set the severity for this violation.
        # For Kudos: Well done rating. Should be determined based on the business context
        # For Warnings: N/A
        self._rating = rating

        # Internal blueprint use only (this configuration does not get propagated to the platform)
        # Adjusted severity of the design gap. This field is used by Resource blueprints to set the severity in a way
        # that higher level component or resource blueprints cannot modify.  This is to account for use-cases
        # it is clear from the resource blueprint that a mitigating design is in place so the resource blueprint can
        # account for that to force a severity
        self._adjusted_severity = adjusted_severity

        # the unique id (full path) of the configuration that we want to call out
        # e.g. LoadBalancer.listeners[0].listenerCertificates[2].certificate[1].name
        # This field should be auto-populated using a utility function (get_config_id)
        self._config_id = config_id

        # currently configured value of this configuration
        if type(current_value) != str:
            self._current_value = str(current_value)
        else:
            self._current_value = current_value

        # For design gaps - Description of the gap to be fixed.
        # Note that design gaps can also use the gap field to populate the gap
        # For Kudos - Description of the passed check
        # For Tasks - Description of the task
        # For Warnings - Description of the warnings
        self._desc = desc

        # Specific details on the gap (for cases where the gap gets displayed separately)
        self._fix = fix

        # oak9's preferred value
        # preferred values can be strings, integers, bools, lists, dictionaries
        # the platform is responsible for checking type to use-cases like remediation
        # or displaying design gaps
        # (Required for remediation)
        if type(preferred_value) == list:
            self._preferred_value = ', '.join(preferred_value)

        elif type(preferred_value) != str:
            self._preferred_value = str(preferred_value)

        else:
            self._preferred_value = preferred_value

        # Additional guidance
        self._additional_guidance = additional_guidance

        # Related configurations that should be remediated together or
        # are better presented bundled together
        self._related_configs: List[RelatedConfig] = related_configs or []

        # add documentation link
        # Currently this is auto-populated on the platform side
        self._documentation_url = documentation_url

        # Requirement id
        # Could be oak9 or customer provided requirement id
        self._req_id = req_id

        # oak9 detailed requirement name
        # This is automatically populated on the platform side
        self._req_name = req_name

        # Priority of finding to relatively prioritize across
        # qualitative ratings.  Can be any number from 0-100
        self._priority = priority

        # Related findings
        # List of UUIDs for related findings
        self._related_findings = related_findings or []

    @property
    def id(self):
        return self._id

    @property
    def finding_type(self):
        return self._finding_type

    @finding_type.setter
    def finding_type(self, value):
        self._finding_type = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        self._rating = value

    @property
    def config_id(self):
        return self._config_id

    @config_id.setter
    def config_id(self, value):
        self._config_id = value

    @property
    def current_value(self):
        return self._current_value

    @current_value.setter
    def current_value(self, value):
        self._current_value = value

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, value):
        self._desc = value

    @property
    def fix(self):
        return self._fix

    @fix.setter
    def fix(self, value):
        self._fix = value

    @property
    def preferred_value(self):
        return self._preferred_value

    @preferred_value.setter
    def preferred_value(self, value):
        if type(value) == list:
            self._preferred_value = ', '.join(value)
        elif type(value) != str:
            self._preferred_value = str(value)
        else:
            self._preferred_value = value

    @property
    def additional_guidance(self):
        return self.additional_guidance

    @additional_guidance.setter
    def additional_guidance(self, value):
        self._additional_guidance = value

    @property
    def severity(self) -> Severity:
        return self._rating

    @severity.setter
    def severity(self, value):
        if self._adjusted_severity:
            self._rating = self._adjusted_severity
        else:
            self._rating = value

    @property
    def adjusted_severity(self):
        return self._adjusted_severity

    @adjusted_severity.setter
    def adjusted_severity(self, value):
        self._adjusted_severity = value

    @property
    def capability_id(self):
        return self._req_id

    @capability_id.setter
    def capability_id(self, value):
        self._req_id = value

    @property
    def capability_name(self):
        return self._req_name

    @capability_name.setter
    def capability_name(self, value):
        self._req_name = value

    @property
    def req_id(self):
        return self._req_id

    @req_id.setter
    def req_id(self, value):
        # TODO: add checks for customer provided ids vs oak9 ids
        self._req_id = value

    @property
    def req_name(self):
        return self._req_name

    @req_name.setter
    def req_name(self, value):
        # TODO: add checks for customer provided reqs vs oak9 reqs
        self._req_name = value

    @property
    def related_configs(self):
        return self._related_configs

    def add_related_config(self, related_config: RelatedConfig):
        self._related_configs.append(related_config)

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        if isinstance(value, int) and 101 > value > 0:
            self._priority = value

    @property
    def related_findings(self):
        return self._related_findings

    @property
    def documentation_url(self):
        return self._documentation_url

    @documentation_url.setter
    def documentation_url(self, value):
        self._documentation_url = value

    def add_related_findings(self, related_findings: Union[uuid.UUID, List]):
        if isinstance(related_findings, uuid.UUID):
            self._related_findings.append(related_findings)
        elif isinstance(related_findings, list):
            for finding in related_findings:
                if isinstance(related_findings, uuid.UUID):
                    self._related_findings.append(finding)

    @classmethod
    def from_violation(cls, viol: Violation):
        self = cls.__new__(cls)
        self._finding_type = FindingType.DesignGap
        self._desc = viol.config_gap
        self._rating = viol.severity
        self._adjusted_severity = viol.adjusted_severity
        self._config_id = viol.config_id
        self._current_value = viol.config_value
        self._desc = viol.config_fix
        self._preferred_value = viol.preferred_value
        self._additional_guidance = viol.additional_guidance
        self._documentation_url = viol.documentation
        self._related_configs = viol.related_configs or []
        self._req_id = viol.capability_id
        self._req_name = viol.capability_name
        self.priority = viol.priority
        return self


    def to_violation(self):
        viol = Violation()
        if self.finding_type not in [FindingType.DesignGap, FindingType.ResourceGap]:
            return None

        viol.config_gap = self.desc
        viol.severity = self.rating
        viol.adjusted_severity = self.adjusted_severity
        viol.config_id = self.config_id
        viol.config_value = self.current_value
        viol.config_fix = self.fix
        viol.preferred_value = self.preferred_value
        viol.additional_guidance = self.additional_guidance
        viol._documentation = self.documentation_url
        viol.related_configs = self.related_configs
        viol.capability_id = self.req_id
        viol.capability_name = self.req_name
        viol.priority = self.priority

        return viol

    def __str__(self):
        ret_str = ''
        ret_str += f"{Style.BRIGHT}Finding Type{Style.NORMAL}: {self.finding_type}\n"
        if self.finding_type in [FindingType.DesignGap, FindingType.ResourceGap, FindingType.Task]:
            ret_str += f"{Style.BRIGHT}Severity{Style.NORMAL}: {self.severity}\n"
            ret_str += f"{Style.BRIGHT}Action Required{Style.NORMAL}: {self.desc}\n"
            ret_str += f"{Style.BRIGHT}Fix{Style.NORMAL}: {self.fix}\n" if self.fix else ''
        elif self.finding_type == FindingType.Kudos:
            ret_str += f"{Style.BRIGHT}Rating{Style.NORMAL}: {self.rating}\n"
            ret_str += f"{Style.BRIGHT}Description{Style.NORMAL}: {self.desc}\n"
        elif self.finding_type == Warning:
            ret_str += f"{Style.BRIGHT}Description{Style.NORMAL}: {self.desc}\n"
        return ret_str

@dataclass
class ValidationMetaInfo:
    caller: str
    request_id: str
    resource_type: str
    blueprint_id: str
    resource_name: str
    resource_id: str


class DesignPref:
    pass


def find_all_resources_by_type(graph: Graph, resource_type: Graph) -> List[Vertex]:
    resource_list = []
    # for root_node in graph.root_nodes:
    #     if root_node.node.vertex_type == VertexType.Resource:
    #         if root_node.node.id == resource_type:
    #             resource_list.append(root_node.node)
    #
    return resource_list


def find_resource_by_id(graph: Graph, resource_id: str) -> Vertex:
    pass


def find_resource_by_name(graph: Graph, resource_name: str) -> Vertex:
    pass


class Blueprint:
    display_name: ClassVar[str] = None
    blueprint_type: ClassVar[BlueprintType] = BlueprintType.Customer
    id: ClassVar[str] = None
    parent_blueprint_id: ClassVar[str] = None
    version: ClassVar[str] = None

    def __init__(self, graph: Any, context: Context = None, design_pref: DesignPref = None) -> None:
        self._graph = graph
        self._context = context
        self.design_pref = design_pref
        self._meta_info = None

    @property
    def context(self):
        return self._context

    @property
    def meta_info(self):
        return self._meta_info

    @meta_info.setter
    def meta_info(self, value):
        pass

    @property
    def graph(self):
        return self._graph

    def validate(self) -> Set[Finding]:
        pass