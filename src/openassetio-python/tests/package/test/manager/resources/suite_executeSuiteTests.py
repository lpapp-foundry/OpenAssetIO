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
Test cases that are run as part of the unit tests for `executeSuite`.
They assert the expected public API of `FixtureAugmentedTestCase`, and
that the harness implementation supplies the correct state to each test.
"""

# pylint: disable=invalid-name
# pylint: disable=missing-class-docstring,missing-function-docstring

from openassetio.hostApi import Manager
from openassetio.test.manager.specifications import ManagerTestHarnessLocale
from openassetio.test.manager.harness import FixtureAugmentedTestCase


__all__ = []


class Test_executeSuite_manager_settings(FixtureAugmentedTestCase):
    def test_when_settings_present_in_fixtures_then_are_set_on_manager(self):
        self.assertEqual(self._manager.settings(), {"test_setting": "a_value"})


class Test_executeSuite_manager(FixtureAugmentedTestCase):
    def test_when_called_then_manager_is_set(self):
        self.assertIsInstance(self._manager, Manager)

    def test_when_called_then_manager_is_the_expected_manager(self):
        self.assertEqual(self._manager.identifier(), "org.openassetio.test.manager.stubManager")


class Test_executeSuite_fixtures(FixtureAugmentedTestCase):
    def test_fixtures_include_those_for_the_test(self):
        self.assertEqual(self._fixtures["a_unique_value"], 5)

    def test_fixtures_include_global_shared_fixtures(self):
        self.assertEqual(self._fixtures["a_global_value"], 1)

    def test_fixtures_include_class_shared_fixtures(self):
        self.assertEqual(self._fixtures["a_class_value"], 2)

    def test_when_class_fixture_is_set_then_overrides_global(self):
        self.assertEqual(self._fixtures["a_class_overridden_global_value"], 4)

    def test_when_function_fixture_is_set_then_overrides_global(self):
        self.assertEqual(self._fixtures["a_function_overridden_global_value"], 7)

    def test_when_function_fixtures_missing_then_includes_shared(self):
        self.assertEqual(
            self._fixtures,
            {
                "a_global_value": 1,
                "a_class_value": 2,
                "a_class_overridden_global_value": 4,
                "a_function_overridden_global_value": 6,
            },
        )

    def test_fixtures_contain_no_additional_keys(self):
        self.assertEqual(
            self._fixtures,
            {
                "a_global_value": 1,
                "a_class_value": 2,
                "a_class_overridden_global_value": 4,
                "a_function_overridden_global_value": 6,
                "another_unique_value": 42,
            },
        )


class Test_executeSuite_fixtures_with_no_values(FixtureAugmentedTestCase):
    def test_when_class_fixtures_missing_then_includes_shared(self):
        self.assertEqual(
            self._fixtures,
            {
                "a_global_value": 1,
                "a_class_overridden_global_value": 3,
                "a_function_overridden_global_value": 6,
            },
        )


class Test_executeSuite_locale(FixtureAugmentedTestCase):
    def test_when_test_function_is_run_then_locale_is_set(self):
        self.assertSetEqual(self._locale.traitSet(), ManagerTestHarnessLocale.kTraitSet)
        self.assertEqual(
            ManagerTestHarnessLocale(self._locale).testTrait().getCaseName(),
            "Test_executeSuite_locale" ".test_when_test_function_is_run_then_locale_is_set",
        )

    def test_when_test_function_is_run_then_locale_testCase_is_function_specific(self):
        self.assertEqual(
            ManagerTestHarnessLocale(self._locale).testTrait().getCaseName(),
            "Test_executeSuite_locale"
            ".test_when_test_function_is_run_then_locale_testCase_is_function_specific",
        )


class Test_executeSuite_shareManager_is_true_by_default(FixtureAugmentedTestCase):
    """
    A slightly different formulation as we need to assert that different
    test cases are invoked with the same manager.
    """

    __managers = {}

    def test_case_a(self):
        self.__managers["a"] = self._manager

    def test_case_b(self):
        self.__managers["b"] = self._manager

    @classmethod
    def tearDownClass(cls):
        assert len(cls.__managers) == 2
        assert len(set(cls.__managers.values())) == 1


class Test_executeSuite_when_shareManager_is_false_then_managers_unique(FixtureAugmentedTestCase):
    """
    A slightly different formulation as we need to assert that different
    test cases are invoked with unique, uninitialized managers.
    """

    shareManager = False

    __managers = {}

    def test_case_a(self):
        self.__managers["a"] = self._manager

    def test_case_b(self):
        self.__managers["b"] = self._manager

    @classmethod
    def tearDownClass(cls):
        assert len(cls.__managers) == 2
        assert len(set(cls.__managers.values())) == 2
        # The StubManager used for these tests captures the host
        # identifier during initialize, so this serves as a handy check
        # to ensure the manager is uninitialized.
        for manager in cls.__managers.values():
            assert "host_identifier" not in manager.info()


# Contrived tests that are expected by the actual test suite.
# They exist so that we can validate they are run and present in
# the process output.


class Test_executeSuite_no_case_fixtures(FixtureAugmentedTestCase):
    def test_with_no_fixture_values(self):
        pass


class Test_executeSuite_with_case_fixtures(FixtureAugmentedTestCase):
    def test_with_no_fixture_values(self):
        pass
