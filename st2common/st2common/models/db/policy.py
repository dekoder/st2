# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mongoengine as me

from st2common import log as logging
from st2common.models.db import stormbase


__all__ = ['PolicyTypeDB', 'PolicyDB']

LOG = logging.getLogger(__name__)


class PolicyTypeDB(stormbase.StormBaseDB):
    """
    The representation of an PolicyType in the system.

    Attributes:
        id: See StormBaseAPI
        name: See StormBaseAPI
        description: See StormBaseAPI
        resource_type: The type of resource that this policy type can be applied to.
        enabled: A flag indicating whether the policies for this type is enabled.
        module: The python module that implements the policy for this type.
        parameters: The specification for parameters for the policy type.
    """
    resource_type = me.StringField(
        required=True,
        help_text='The type of resource that this policy type can be applied to.')
    enabled = me.BooleanField(
        required=True,
        default=True,
        help_text='A flag indicating whether the runner for this type is enabled.')
    module = me.StringField(
        required=True,
        help_text='The python module that implements the policy for this type.')
    parameters = me.DictField(
        help_text='The specification for parameters for the policy type.')


class PolicyDB(stormbase.StormFoundationDB, stormbase.ContentPackResourceMixin):
    """
    The representation for a policy in the system.

    Attribute:
        enabled: A flag indicating whether this policy is enabled in the system.
        policy_type: The type of policy.
        parameters: The specification of input parameters for the policy.
    """
    name = me.StringField(required=True)
    ref = me.StringField(required=True)
    pack = me.StringField(
        required=False,
        unique_with='name',
        help_text='Name of the content pack.')
    description = me.StringField()
    enabled = me.BooleanField(
        required=True,
        default=True,
        help_text='A flag indicating whether this policy is enabled in the system.')
    resource_ref = me.StringField(required=True)
    policy_type = me.StringField(
        required=True,
        unique_with='resource_ref',
        help_text='The type of policy.')
    parameters = me.DictField(
        help_text='The specification of input parameters for the policy.')


MODELS = [PolicyTypeDB, PolicyDB]
