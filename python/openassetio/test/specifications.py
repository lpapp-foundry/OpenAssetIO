#
#   Copyright 2022 The Foundry Visionmongers Ltd
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
@namespace openassetio.test.specifications
Specifications for use within openassetio test harnesses.
"""

from openassetio import Specification, Trait


# pylint: disable=missing-function-docstring


class TestTrait(Trait):
    """
    A trait that represents a calling context that is some kind of
    test environment.
    """

    kId = "test"

    __kCaseName = "case"
    __kSuiteName = "suite"

    def setCaseName(self, name):
        self._specification.setTraitProperty(self.kId, self.__kCaseName, name)

    def getCaseName(self):
        return self._specification.getTraitProperty(self.kId, self.__kCaseName)

    def setSuiteName(self, name):
        self._specification.setTraitProperty(self.kId, self.__kSuiteName, name)

    def getSuiteName(self):
        return self._specification.getTraitProperty(self.kId, self.__kSuiteName)


class HarnessTrait(Trait):
    """
    A trait that defines a calling context that is some kind of
    automated scriptable framework that operates on a specific
    target object.
    """

    kId = "harness"


class TestHarnessLocale(Specification):
    """
    A locale for test cases run as part of one of the API supplied
    test harnesses.
    """

    kTraitIds = {TestTrait.kId, HarnessTrait.kId}

    ## TODO(TC): Add a python base Specification class once
    ## https://github.com/TheFoundryVisionmongers/OpenAssetIO/issues/348
    ## has been completed.
    def __init__(self):
        super().__init__(self.kTraitIds)

    def testTrait(self):
        return TestTrait(self)

    def harnessTrait(self):
        return HarnessTrait(self)
