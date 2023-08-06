def check_transparent_data_encryption_aks(aks, context):
    """
    Temp disks and cache for agent node pools in Azure Kubernetes Service clusters should be encrypted at host.

    To enhance data security, the data stored on the virtual machine (VM) host of your Azure Kubernetes Service
    nodes VMs should be encrypted at rest. This is a common requirement in many regulatory and industry compliance
    standards.

    Implements:
        AZURE_POLICY: https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Kubernetes/AKS_EncryptionAtHost_Deny.json
        KUBE_BENCH: https://github.com/aquasecurity/blob/master/kube-bench/cfg/cis-1.6/master.yaml
    Coverage:
        Partial:
            TODO (atcherniakhovski): Validate that this handles the case of multiple node-pools.
    """
    violations = []

    return violations