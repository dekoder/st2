# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the 'License'); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from st2common.models.db.policy import PolicyTypeDB, PolicyDB
from st2common.persistence.policy import PolicyType, Policy
from st2tests import DbModelTestCase


class PolicyTypeTest(DbModelTestCase):
    access_type = PolicyType

    @staticmethod
    def _create_instance():
        parameters = {
            'threshold': {
                'type': 'integer',
                'required': True
            }
        }

        instance = PolicyTypeDB(name='action.concurrency',
                                description='TBD',
                                resource_type='Action',
                                module='st2action.policies.concurrency',
                                parameters=parameters)

        return instance

    def test_crud(self):
        instance = self._create_instance()

        defaults = {
            'enabled': True
        }

        updates = {
            'description': 'Limits the concurrent executions for the action.'
        }

        self._assert_crud(instance, defaults=defaults, updates=updates)

    def test_unique_key(self):
        instance = self._create_instance()
        self._assert_unique_key_constraint(instance)


class PolicyTest(DbModelTestCase):
    access_type = Policy

    @staticmethod
    def _create_instance():
        instance = PolicyDB(pack='core',
                            name='local.concurrency',
                            ref='core.local.concurrency',
                            description='TBD',
                            resource_ref='core.local',
                            policy_type='action.concurrency',
                            parameters={
                                'threshold': 25
                            })

        return instance

    def test_crud(self):
        instance = self._create_instance()

        defaults = {
            'enabled': True
        }

        updates = {
            'description': 'Limits the concurrent executions for the action "core.local".'
        }

        self._assert_crud(instance, defaults=defaults, updates=updates)

    def test_ref(self):
        instance = self._create_instance()
        ref = instance.get_reference()
        self.assertIsNotNone(ref)
        self.assertEqual(ref.pack, instance.pack)
        self.assertEqual(ref.name, instance.name)
        self.assertEqual(ref.ref, instance.pack + '.' + instance.name)
        self.assertEqual(ref.ref, instance.ref)

    def test_unique_key(self):
        instance = self._create_instance()
        self._assert_unique_key_constraint(instance)
