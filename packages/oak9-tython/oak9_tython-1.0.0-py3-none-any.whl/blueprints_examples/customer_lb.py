from typing import Set

# **** Cloud Resource Types (Protos) ****
# **** Core Types ****

from oak9.sac_framework.core.types import Blueprint
# **** Security Capabilities ****
from oak9.sac_framework.core.types import Finding, FindingType


"""
    Example use-case where Customer extends oak9's blueprint
"""


class CustomerLB(Blueprint):
    """

    This is an example customer blueprint to check loadbalancer configurations

    Name:
        abcd

    Author:
        ashah@oak9.io

    """


    def validate_custom_lb_pattern(self):
        """
        Customer's custom validation check for loadbalancers

        CustomerReq:
            Req.1

        Implements:
            CSA: https://Link_to_CSA
            NIST: https://link_to_nist
            Customer Framework: https://link_to_customer_compliance

        Returns:
            Finding: Security design finding
        """

        my_finding = Finding(
            finding_type=FindingType.DesignGap,
            desc="Listener configuration needs to be updated"
        )

        return my_finding

    def validate_another_custom_pattern(self):
        """
        Customer's second custom validation check

        CustomerReq:
            Req.2

        Implements:
            CSA: https://Link_to_CSA
            NIST: https://link_to_nist
            Customer Framework: https://link_to_customer_compliance

        Returns:
            Finding: Security design finding
        """

        my_finding = Finding(
            finding_type=FindingType.DesignGap,
            desc="Loadbalancer TLS configuration needs to be updated"
        )

        return my_finding

    def validate(self) -> Set[Finding]:
        design_gaps = set()
        design_gaps.add(self.validate_custom_lb_pattern())
        design_gaps.add(self.validate_another_custom_pattern())
        return design_gaps
