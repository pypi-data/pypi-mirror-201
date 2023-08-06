from oak9.sac_framework.core.types import Severity, Violation
from oak9.sac_framework.core.exception import ViolationException
from oak9.sac_framework.core.tools import get_config_id


class AzureAks():
    oak9_base = 'Oak9.Containers.ContainerManagement.Application'
    blueprint_type = 'AzureAks'
    sn = 'aks'

    def check_logging_aks(aks, context):

        violations = []

        try:
            pass

        except Exception as e:
            violations.append(ViolationException(e))

        return violations

    def check_transparent_data_encryption_aks(aks, context):
        """
        Temp disks and cache for agent node pools in Azure Kubernetes Service clusters should be encrypted at host.

        To enhance data security, the data stored on the virtual machine (VM) host of your Azure Kubernetes Service
        nodes VMs should be encrypted at rest. This is a common requirement in many regulatory and industry compliance
        standards.

        Implements:
            AZURE_POLICY: https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Kubernetes/AKS_EncryptionAtHost_Deny.json
        Coverage:
            Partial:
                TODO (atcherniakhovski): Validate that this handles the case of multiple node-pools.
        """
        violations = []

        try:

            if aks.managed_clusters.disk_encryption_set_id == "":
                violations.append(
                    Violation(
                        severity=Severity.Critical,
                        config_id=get_config_id(aks, 'disk_encryption_set_id'),
                        resource_id=aks.managed_clusters.resource_info.id,
                        resource_type=aks.managed_clusters.resource_into.resource_type,
                        config_value=aks.managed_clusters.disk_encryption_set_id
                    )
                )

        except Exception as e:
            violations.append(ViolationException(e))

        return violations

