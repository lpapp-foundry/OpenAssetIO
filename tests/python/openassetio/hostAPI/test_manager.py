#
#   Copyright 2013-2021 The Foundry Visionmongers Ltd
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
Tests that cover the openassetio.hostAPI.Manager wrapper class.
"""

# pylint: disable=no-self-use
# pylint: disable=invalid-name,redefined-outer-name
# pylint: disable=missing-class-docstring,missing-function-docstring

from unittest import mock

import pytest

from openassetio import Context, TraitsData
from openassetio.hostAPI import Manager
from openassetio.managerAPI import HostSession


## @todo Remove comments regarding Entity methods when splitting them from core API

@pytest.fixture
def host_session():
    return mock.create_autospec(HostSession)


@pytest.fixture
def manager(mock_manager_interface, host_session):
    return Manager(mock_manager_interface, host_session)


@pytest.fixture
def an_empty_traitsdata():
    return TraitsData(set())


@pytest.fixture
def some_entity_traitsdatas():
    return [TraitsData(set()), TraitsData(set())]


@pytest.fixture
def a_traitsdata():
    return TraitsData(set())


@pytest.fixture
def an_entity_trait_set():
    return {"blob", "lolcat"}


@pytest.fixture
def some_entity_trait_sets():
    return [{"blob"}, {"blob", "image"}]

@pytest.fixture
def a_context():
    return Context()


@pytest.fixture
def a_ref():
    return "asset://a"


@pytest.fixture
def some_refs():
    return ["asset://a", "asset://b"]

# __str__ and __repr__ aren't tested as they're debug tricks that need
# assessing when this is ported to cpp

class Test_Manager_init:

    def test_interface_returns_the_constructor_supplied_object(
            self, mock_manager_interface, host_session):

        # pylint: disable=protected-access
        a_manager = Manager(mock_manager_interface, host_session)
        assert a_manager._interface() is mock_manager_interface

    def test_when_constructed_with_ManagerInterface_as_None_then_raises_TypeError(
            self, host_session):
        with pytest.raises(TypeError) as err:
            Manager(None, host_session)

        assert str(err.value) == (
            '__init__(): incompatible constructor arguments. The following argument types '
            'are supported:\n'
            '    1. openassetio._openassetio.hostAPI.Manager(managerInterface: '
            'openassetio._openassetio.managerAPI.ManagerInterface)\n'
            '\n'
            'Invoked with: None')


class Test_Manager_identifier:

    def test_wraps_the_corresponding_method_of_the_held_interface(
            self, manager, mock_manager_interface):
        expected = "stub.manager"
        mock_manager_interface.mock.identifier.return_value = expected

        actual = manager.identifier()

        assert actual == expected

    def test_when_interface_provides_wrong_type_then_raises_RuntimeError(
            self, manager, mock_manager_interface):

        mock_manager_interface.mock.identifier.return_value = 123

        with pytest.raises(RuntimeError) as err:
            manager.identifier()

        # Pybind error messages vary between release and debug mode:
        # "Unable to cast Python instance of type <class 'int'> to C++
        # type 'std::string'"
        # vs.
        # "Unable to cast Python instance to C++ type (compile in debug
        # mode for details)"
        assert str(err.value).startswith("Unable to cast Python instance")


class Test_Manager_displayName:

    def test_wraps_the_corresponding_method_of_the_held_interface(
            self, manager, mock_manager_interface):

        expected = "stub.manager"
        mock_manager_interface.mock.displayName.return_value = expected

        actual = manager.displayName()

        assert actual == expected

    def test_when_interface_provides_wrong_type_then_raises_RuntimeError(
            self, manager, mock_manager_interface):

        mock_manager_interface.mock.displayName.return_value = 123

        with pytest.raises(RuntimeError) as err:
            manager.displayName()

        # Note: pybind error messages vary between release and debug mode.
        assert str(err.value).startswith("Unable to cast Python instance")


class Test_Manager_info:

    def test_wraps_the_corresponding_method_of_the_held_interface(
            self, manager, mock_manager_interface):

        expected = {"an int": 123}
        mock_manager_interface.mock.info.return_value = expected

        actual = manager.info()

        assert actual == expected

    def test_when_interface_provides_wrong_type_then_raises_RuntimeError(
            self, manager, mock_manager_interface):

        mock_manager_interface.mock.info.return_value = {123: 123}

        with pytest.raises(RuntimeError) as err:
            manager.info()

        # Note: pybind error messages vary between release and debug mode.
        assert str(err.value).startswith("Unable to cast Python instance")


class Test_Manager_updateTerminology:

    def test_wraps_the_corresponding_method_of_the_held_interface(
            self, manager, mock_manager_interface, host_session):

        method = mock_manager_interface.mock.updateTerminology
        a_dict = {"k", "v"}
        assert manager.updateTerminology(a_dict) is a_dict
        method.assert_called_once_with(a_dict, host_session)


class Test_Manager_getSettings:

    def test_wraps_the_corresponding_method_of_the_held_interface(
            self, manager, mock_manager_interface, host_session):

        method = mock_manager_interface.mock.getSettings
        assert manager.getSettings() == method.return_value
        method.assert_called_once_with(host_session)


class Test_Manager_setSettings:

    def test_wraps_the_corresponding_method_of_the_held_interface(
            self, manager, mock_manager_interface, host_session):

        method = mock_manager_interface.mock.setSettings
        a_dict = {"k", "v"}
        assert manager.setSettings(a_dict) == method.return_value
        method.assert_called_once_with(a_dict, host_session)


class Test_Manager_initialize:

    def test_wraps_the_corresponding_method_of_the_held_interface(
            self, manager, mock_manager_interface, host_session):

        method = mock_manager_interface.mock.initialize
        assert manager.initialize() == method.return_value
        method.assert_called_once_with(host_session)


class Test_Manager_prefetch:

    def test_wraps_the_corresponding_method_of_the_held_interface(
            self, manager, mock_manager_interface, host_session, some_refs, a_context):

        method = mock_manager_interface.mock.prefetch
        assert manager.prefetch(some_refs, a_context) == method.return_value
        method.assert_called_once_with(some_refs, a_context, host_session)


class Test_Manager_flushCaches:

    def test_wraps_the_corresponding_method_of_the_held_interface(
            self, manager, mock_manager_interface, host_session):

        method = mock_manager_interface.mock.flushCaches
        assert manager.flushCaches() == method.return_value
        method.assert_called_once_with(host_session)


class Test_Manager_isEntityReference:

    def test_wraps_the_corresponding_method_of_the_held_interface(
            self, manager, mock_manager_interface, host_session, some_refs):

        method = mock_manager_interface.mock.isEntityReference
        assert manager.isEntityReference(some_refs) == method.return_value
        method.assert_called_once_with(some_refs, host_session)


class Test_Manager_entityExists:

    def test_wraps_the_corresponding_method_of_the_held_interface(
            self, manager, mock_manager_interface, host_session, some_refs, a_context):

        method = mock_manager_interface.mock.entityExists
        assert manager.entityExists(some_refs, a_context) == method.return_value
        method.assert_called_once_with(some_refs, a_context, host_session)


class Test_Manager_defaultEntityReference:

    def test_wraps_the_corresponding_method_of_the_held_interface(
            self, manager, mock_manager_interface, host_session, a_context,
            some_entity_trait_sets):

        method = mock_manager_interface.mock.defaultEntityReference
        assert manager.defaultEntityReference(some_entity_trait_sets, a_context) \
                == method.return_value
        method.assert_called_once_with(some_entity_trait_sets, a_context, host_session)


class Test_Manager_entityName:

    def test_wraps_the_corresponding_method_of_the_held_interface(
            self, manager, mock_manager_interface, host_session, some_refs, a_context):

        method = mock_manager_interface.mock.entityName
        assert manager.entityName(some_refs, a_context) == method.return_value
        method.assert_called_once_with(some_refs, a_context, host_session)


class Test_Manager_entityDisplayNamer:

    def test_wraps_the_corresponding_method_of_the_held_interface(
            self, manager, mock_manager_interface, host_session, some_refs, a_context):

        method = mock_manager_interface.mock.entityDisplayName
        assert manager.entityDisplayName(some_refs, a_context) == method.return_value
        method.assert_called_once_with(some_refs, a_context, host_session)


class Test_Manager_entityVersion:

    def test_wraps_the_corresponding_method_of_the_held_interface(
            self, manager, mock_manager_interface, host_session, some_refs, a_context):

        method = mock_manager_interface.mock.entityVersion
        assert manager.entityVersion(some_refs, a_context) == method.return_value
        method.assert_called_once_with(some_refs, a_context, host_session)


class Test_Manager_entityVersions:

    def test_wraps_the_corresponding_method_of_the_held_interface(
            self, manager, mock_manager_interface, host_session, some_refs, a_context):

        method = mock_manager_interface.mock.entityVersions

        assert manager.entityVersions(some_refs, a_context) == method.return_value
        method.assert_called_once_with(
            some_refs, a_context, host_session, includeMetaVersions=False, maxNumVersions=-1)
        method.reset_mock()

        max_results = 5
        assert manager.entityVersions(
            some_refs, a_context, maxNumVersions=max_results) == method.return_value
        method.assert_called_once_with(
            some_refs, a_context, host_session,
            includeMetaVersions=False, maxNumVersions=max_results)
        method.reset_mock()

        include_meta = True
        assert manager.entityVersions(
            some_refs, a_context, maxNumVersions=max_results,
            includeMetaVersions=include_meta) == method.return_value
        method.assert_called_once_with(
            some_refs, a_context, host_session, includeMetaVersions=include_meta,
            maxNumVersions=max_results)


class Test_Manager_finalizedEntityVersion:

    def test_wraps_the_corresponding_method_of_the_held_interface(
            self, manager, mock_manager_interface, host_session, some_refs, a_context):

        method = mock_manager_interface.mock.finalizedEntityVersion
        assert manager.finalizedEntityVersion(some_refs, a_context) == method.return_value
        method.assert_called_once_with(
            some_refs, a_context, host_session, overrideVersionName=None)
        method.reset_mock()

        a_version_name = "aVersion"
        method = mock_manager_interface.mock.finalizedEntityVersion
        assert manager.finalizedEntityVersion(
            some_refs, a_context, overrideVersionName=a_version_name) == method.return_value
        method.assert_called_once_with(
            some_refs, a_context, host_session, overrideVersionName=a_version_name)


class Test_Manager_getRelatedReferences:

    def test_wraps_the_corresponding_method_of_the_held_interface(
            self, manager, mock_manager_interface, host_session, a_ref, an_empty_traitsdata,
            an_entity_trait_set, a_context):

        # pylint: disable=too-many-locals

        method = mock_manager_interface.mock.getRelatedReferences

        one_ref = a_ref
        two_refs = [a_ref, a_ref]
        three_refs = [a_ref, a_ref, a_ref]
        one_data = an_empty_traitsdata
        two_datas = [an_empty_traitsdata, an_empty_traitsdata]
        three_datas = [an_empty_traitsdata, an_empty_traitsdata, an_empty_traitsdata]

        # Check validation that one to many or equal length ref/data args are required

        for refs_arg, datas_arg in (
                (two_refs, three_datas),
                (three_refs, two_datas)
        ):
            with pytest.raises(ValueError):
                manager.getRelatedReferences(refs_arg, datas_arg, a_context)
            method.assert_not_called()
            method.reset_mock()

        for refs_arg, datas_arg, expected_refs_arg, expected_datas_arg in (
                (one_ref, three_datas, [one_ref], three_datas),
                (three_refs, one_data, three_refs, [one_data]),
                (three_refs, three_datas, three_refs, three_datas)
        ):
            assert manager.getRelatedReferences(
                refs_arg, datas_arg, a_context) == method.return_value
            method.assert_called_once_with(
                expected_refs_arg, expected_datas_arg, a_context, host_session,
                resultTraitSet=None)
            method.reset_mock()

        # Check optional resultTraitSet
        assert manager.getRelatedReferences(
            one_ref, one_data, a_context, resultTraitSet=an_entity_trait_set) \
                    == method.return_value
        method.assert_called_once_with(
            [one_ref], [one_data], a_context, host_session, resultTraitSet=an_entity_trait_set)


class Test_Manager_resolve:

    def test_wraps_the_corresponding_method_of_the_held_interface(
            self, manager, mock_manager_interface, host_session, some_refs, an_entity_trait_set,
            a_context):

        method = mock_manager_interface.mock.resolve
        assert manager.resolve(some_refs, an_entity_trait_set, a_context) \
                == method.return_value
        method.assert_called_once_with(some_refs, an_entity_trait_set, a_context, host_session)


class Test_Manager_managentPolicy:

    def test_wraps_the_corresponding_method_of_the_held_interface(
            self, manager, mock_manager_interface, host_session, some_entity_trait_sets,
            a_context):

        method = mock_manager_interface.mock.managementPolicy
        assert manager.managementPolicy(some_entity_trait_sets, a_context) == method.return_value
        method.assert_called_once_with(some_entity_trait_sets, a_context, host_session)


class Test_Manager_preflight:

    def test_wraps_the_corresponding_method_of_the_held_interface(
            self, manager, mock_manager_interface, host_session, some_refs, an_entity_trait_set,
            a_context):

        method = mock_manager_interface.mock.preflight
        assert manager.preflight(some_refs, an_entity_trait_set, a_context) \
                == method.return_value
        method.assert_called_once_with(some_refs, an_entity_trait_set, a_context, host_session)


class Test_Manager_register:

    def test_wraps_the_the_held_interface_register_methods(
            self, manager, mock_manager_interface, host_session, some_refs, a_traitsdata,
            a_context):

        datas = [a_traitsdata for _ in some_refs]
        mutated_refs = [f"{r}-registered" for r in some_refs]

        register_method = mock_manager_interface.mock.register
        register_method.return_value = mutated_refs

        assert manager.register(some_refs, datas, a_context) \
                == register_method.return_value
        register_method.assert_called_once_with(some_refs, datas, a_context, host_session)


    def test_when_called_with_mixed_array_lengths_then_IndexError_is_raised(
            self, manager, some_refs, a_traitsdata, a_context):

        datas = [a_traitsdata for _ in some_refs]

        with pytest.raises(IndexError):
            manager.register(some_refs[1:], datas, a_context)

        with pytest.raises(IndexError):
            manager.register(some_refs, datas[1:], a_context)


    def test_when_called_with_varying_trait_sets_then_ValueError_is_raised(
            self, manager, some_refs, a_context):

        datas = [TraitsData({f"trait{i}", "🦀"})for i in range(len(some_refs))]

        with pytest.raises(ValueError):
            manager.register(some_refs, datas, a_context)
