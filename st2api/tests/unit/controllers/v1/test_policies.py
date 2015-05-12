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

import six

from st2common.models.api.policy import PolicyTypeAPI
from st2common.persistence.policy import PolicyType
from st2tests.fixturesloader import FixturesLoader
from tests import FunctionalTest


TEST_FIXTURES = {
    'policytypes': [
        'policy_type_1.yaml',
        'policy_type_2.yaml'
    ]
}

PACK = 'generic'
LOADER = FixturesLoader()
FIXTURES = LOADER.load_fixtures(fixtures_pack=PACK, fixtures_dict=TEST_FIXTURES)


class PolicyTypeControllerTest(FunctionalTest):

    @classmethod
    def setUpClass(cls):
        super(PolicyTypeControllerTest, cls).setUpClass()

        for _, fixture in six.iteritems(FIXTURES['policytypes']):
            instance = PolicyTypeAPI(**fixture)
            PolicyType.add_or_update(PolicyTypeAPI.to_model(instance))

    def test_get_all(self):
        url = '/v1/policytypes'
        resp = self.app.get(url)
        self.assertEqual(resp.status_int, 200)
        self.assertGreater(len(resp.json), 0, '%s is empty.' % url)

    def test_filter(self):
        url = '/v1/policytypes'
        resp = self.app.get(url)
        self.assertEqual(resp.status_int, 200)
        self.assertGreater(len(resp.json), 0, '%s is empty.' % url)
        selected = resp.json[0]

        url = '/v1/policytypes?name=%s' % selected['name']
        resp = self.app.get(url)
        self.assertEqual(resp.status_int, 200)
        self.assertEqual(len(resp.json), 1, '%s did not return exactly one instance.' % url)
        retrieved = resp.json[0]
        self.assertEqual(retrieved['id'], selected['id'],
                         '%s returned incorrect policy_type.' % url)

    def test_filter_empty(self):
        url = '/v1/policytypes?name=whatever'
        resp = self.app.get(url)
        self.assertEqual(resp.status_int, 200)
        self.assertEqual(len(resp.json), 0, '%s is not empty.' % url)

    def test_get_one(self):
        url = '/v1/policytypes'
        resp = self.app.get(url)
        self.assertEqual(resp.status_int, 200)
        self.assertGreater(len(resp.json), 0, '%s is empty.' % url)
        selected = resp.json[0]

        url = '/v1/policytypes/%s' % selected['id']
        resp = self.app.get(url)
        self.assertEqual(resp.status_int, 200)
        retrieved = resp.json
        self.assertEqual(retrieved['id'], selected['id'],
                         '%s returned incorrect policy_type.' % url)

    def test_get_one_fail(self):
        url = '/v1/policytypes/1'
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(resp.status_int, 404)
