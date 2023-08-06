from typing import Set

# **** Cloud Resource Types (Protos) ****
# **** Core Types ****

from oak9.sac_framework.core.types import Blueprint
# **** Security Capabilities ****
from oak9.sac_framework.core.types import Finding, FindingType


"""
    Example use-case where Customer extends oak9's blueprint
"""


class CustomerBlueprint(Blueprint):
    """

    This is the first example customer blueprint

    Name:
        Asset Inventory Checks

    Author:
        ashah@oak9.io

    """


    def validate_custom_tagging_check(self):
        """
        Customer's custom validation check for asset inventory

        CustomerReq:
            Req.1

        Implements:
            CSA: https://Link_to_CSA
            NIST: https://link_to_nist
            Customer Framework: https://link_to_customer_compliance

        Returns:
            Finding: Security design finding
        """
        print("Running customer's custom tagging check")

        my_finding = Finding(
            finding_type=FindingType.DesignGap,
            desc="Tags are missing"
        )

        return my_finding

    def validate_custom_naming_check(self):
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
        print("Running customer's custom naming convention check")

        my_finding = Finding(
            finding_type=FindingType.DesignGap,
            desc="Naming convention is not in-line with standards"
        )

        return my_finding

    def validate(self) -> Set[Finding]:
        design_gaps = set()
        design_gaps.add(self.validate_custom_naming_check())
        design_gaps.add(self.validate_custom_tagging_check())
        return design_gaps
