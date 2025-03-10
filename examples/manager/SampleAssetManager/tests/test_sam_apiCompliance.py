#
#   Copyright 2013-2022 The Foundry Visionmongers Ltd
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
"""
Test cases for the SampleAssetManager that make use of the OpenAssetIO
manager test harness.

Note that this file simply wraps the openassetio.test.manager harness in
a pytest test, so that it can be run as part of the project test suite.
It also serves as an example of how to programmatically execute the test
harness, should you wish to extend it with tests for your own business
logic.

It is not required in order to make use of the test harness. The base
API compliance tests can simply be run from a command line with
openassetio available, and the target plugin on
$OPENASSETIO_PLUGIN_PATH:

  python -m openassetio.test.manager -f path/to/fixtures.py
"""

# pylint: disable=no-self-use
# pylint: disable=invalid-name,redefined-outer-name
# pylint: disable=missing-class-docstring,missing-function-docstring

import os
import pytest

from openassetio.test.manager import harness, apiComplianceSuite


#
# Tests
#


class Test_SampleAssetManager:
    def test_passes_apiComplianceSuite(self, api_compliance_fixtures):
        assert harness.executeSuite(apiComplianceSuite, api_compliance_fixtures)


#
# Fixtures
#


@pytest.fixture(autouse=True)
def sam_plugin_env(sam_base_dir, monkeypatch):
    """
    Provides a modified environment with the SampleAssetManager
    plugin on the OpenAssetIO search path.
    """
    plugin_dir = os.path.join(sam_base_dir, "python")
    monkeypatch.setenv("OPENASSETIO_PLUGIN_PATH", plugin_dir)


@pytest.fixture
def api_compliance_fixtures(sam_base_dir):
    """
    Provides the fixtues dict for the SampleAssetManager when used with
    the openassetio.test.manager.apiComplianceSuite.
    """
    fixtures_path = os.path.join(sam_base_dir, "tests", "fixtures.py")
    return harness.fixturesFromPyFile(fixtures_path)


@pytest.fixture
def sam_base_dir():
    """
    Provides the path to the base directory for the SampleAssetManager
    codebase.
    """
    return os.path.dirname(os.path.dirname(__file__))
