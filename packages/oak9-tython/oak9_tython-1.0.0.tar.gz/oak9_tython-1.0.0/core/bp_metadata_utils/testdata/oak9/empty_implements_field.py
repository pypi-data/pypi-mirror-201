def check_transparent_data_encryption_aks(aks, context):
    """
    Temp disks and cache for agent node pools in Azure Kubernetes Service clusters should be encrypted at host.

    To enhance data security, the data stored on the virtual machine (VM) host of your Azure Kubernetes Service
    nodes VMs should be encrypted at rest. This is a common requirement in many regulatory and industry compliance
    standards.

    Implements:
    """
    violations = []

    return violations