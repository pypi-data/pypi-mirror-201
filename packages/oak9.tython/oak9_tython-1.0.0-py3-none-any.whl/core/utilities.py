"""Module providingFunction utilities for the runner."""
import json
from typing import List
from core.tools import get_config_id
from policyuniverse.policy import Policy
from policyuniverse.statement import Statement


def has_IP_Match_Rule(AzureWAF):
    if not len(AzureWAF.custom_rules) > 0:
        return False
    
    else:
        count = 0
        for rule in AzureWAF.custom_rules:
            if len(rule.match_conditions) > 0:
                for condition in rule.match_conditions:
                    if condition.operator.lower() == 'ipmatch':
                        count = count +1
        
        return False if count == 0 else True


def has_Geo_Match_Rule(AzureWAF):
    if not len(AzureWAF.custom_rules) > 0:
        return False
    
    else:
        count = 0
        for rule in AzureWAF.custom_rules:
            if len(rule.match_conditions) > 0:
                for condition in rule.match_conditions:
                    if condition.operator.lower() == 'geomatch':
                        count = count +1
        
        return False if count == 0 else True


def has_Managed_Rule_Set(AzureWAF, rulesetname):
    if not len(AzureWAF.managed_rules.managed_rule_sets) > 0:
        return False
    
    else:
        count = 0
        for rule_set in AzureWAF.managed_rules.managed_rule_sets:
            if rule_set.rule_set_type.__contains__(rulesetname):
                count = count + 1

        if count == 0:
            return False
        
        else:
            return True


def has_Managed_Rule_Set_Overrides(AzureWAF, rulesetname):
    if not len(AzureWAF.managed_rules.managed_rule_sets) > 0:
        return True
    
    else:
        count = 0
        for rule_set in AzureWAF.managed_rules.managed_rule_sets:
            if rule_set.rule_set_type.__contains__(rulesetname) and len(rule_set.rule_group_overrides) > 0:
                count = count+1
                
        if count == 0:
            return False
        
        else:
            return True


def has_Rate_Limit_Rule(AzureWAF):
    if not len(AzureWAF.custom_rules) > 0:
        return False
    
    else:
        count = 0
        for rule in AzureWAF.custom_rules:
            if rule.rule_type == 'RateLimitRule':
                count = count +1
        
        return False if count == 0 else True


def get_aws_json_policy(json_object: str):

    try:
        
        policy = json.loads(json_object.replace("\n;", ""))
        policy = Policy(policy)
        
    except Exception as e:
        
        # failed to generate json and create policy object
        return None

    if policy:
        return policy
    else:
        return None


def check_aws_policy_action(statement: Statement, insecure_actions: list[str]) -> List[str]:
    """_summary_
        This method will check the statement of a policy for the action(s) specified

    Args:
        statement (Statement): The policy statement to be evaluated 
        actions (list[str]): The list of insecure actions 

    Returns:
       insecure_actions_found (list[str]): The insecure actions found within the statement
       
    """
    
    insecure_actions_found: list[str] = []
    
    if statement.effect.lower() == "allow":
        
        for insecure_action in insecure_actions:
            if insecure_action in statement.actions:
                 
                insecure_actions_found.append(insecure_action)

    return insecure_actions_found


def check_aws_policy_resource(statement: Statement, insecure_resources: list[str]) -> List[str]:
    
    """_summary_
    This method will check the statement of a policy for the resource(s) specified
    
    Args:
        statement (Statement): The policy statement to be evaluated 
        resources (list[str]): The list of insecure resources

    Returns:
       insecure_resource_found (list[str]): The insecure actions found within the statement
    """
    
    insecure_resource_found: list[str] = []
    
    if statement.effect.lower() == "allow":
            
        for insecure_resource in insecure_resources:
            if insecure_resource in statement.resources:
                 
                insecure_resource_found.append(insecure_resource)
    
    return insecure_resource_found


def check_aws_policy_principal(statement: Statement, insecure_principals: list[str]) -> List[str]:
    
    """_summary_
    This method will check the statement of a policy for the principal(s) specified
    
    Args:
        statement (Statement): The policy statement to be evaluated
        principal (list[str]): The list of insecure principals

    Returns:
    
       insecure_principal_found (list[str]): The insecure principals found within the statement
    """
    
    insecure_principal_found: list[str] = []
    
    if statement.effect.lower() == "allow":
            
        for insecure_principal in insecure_principals:
            if insecure_principal in statement.principals:
                 
                insecure_principal_found.append(insecure_principal)
        
    return insecure_principal_found

def azure_keyvault_policies_are_defined(keyvault):
    config_list = []
    obj_list = []
    is_defined: bool = False    

    if len(keyvault.vaults_access_policies) > 0:
        obj_list.append(keyvault.vaults_access_policies)
        config_list.append(get_config_id(keyvault, 'vaults_access_policies', keyvault))
        is_defined = True
    if len(keyvault.vaults.access_policies) > 0:
        obj_list.append([keyvault.vaults])
        config_list.append(get_config_id(keyvault, 'access_policies', keyvault.vaults))
        is_defined = True
    if not (len(keyvault.vaults_access_policies) > 0 or len(keyvault.vaults.access_policies) > 0):
        config_list.append(get_config_id(keyvault, 'vaults_access_policies', keyvault))

    return (is_defined, config_list, obj_list)
