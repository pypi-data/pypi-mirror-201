# Copyright 2017-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may
# not use this file except in compliance with the License. A copy of the License is located at
#
#        http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
'''
Rule Name:
  ALB_HTTP_TO_HTTPS_REDIRECTION_CHECK

Description:
  Checks whether HTTP to HTTPS redirection is configured.

Trigger:
  Periodic

Reports on:
  AWS::ElasticLoadBalancingV2::LoadBalancer

Rule Parameters:
  None

Scenarios:
  Scenario: 1
     Given: No Application Load Balancer is present
      Then: Return NOT_APPLICABLE
  Scenario: 2
     Given: There is at least 1 Application Load Balancer
       And: Application Load Balancer has only HTTPS listener(s)
      Then: Return COMPLIANT
  Scenario: 3
     Given: There is at least 1 Application Load Balancer
       And: Application Load Balancer has one or more HTTP listeners configured
       And: At least one HTTP listener rule does not have HTTP to HTTPS redirection action configured
      Then: Return NON_COMPLIANT
  Scenario: 4
     Given: There is at least 1 Application Load Balancer
       And: Application Load Balancer has one or more HTTP listeners configured
       And: All HTTP listener rules have HTTP to HTTPS redirection action configured
      Then: Return COMPLIANT
'''

def add(i: int, j: int) -> int:
    """
    Adds two integers and returns the sum
    :param i: First int.
    :param j: Second int.
    :return: The sum of i and j
    """
    return i + j