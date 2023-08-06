#
# MIT License
#
# Copyright © 2022 Hank AI, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Classes for AutoCoding Enum."""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

import hankai.lib
import hankai.orchestrator


class ServiceFeature(hankai.lib.MemberValue):
    """Enum or DocuVision service feature attribute names."""

    APP = "app"


class SetService(hankai.orchestrator.SetService):
    """Supported DocuVision Sets and Services and optional Service features."""

    _supported: Dict[
        int, Dict[hankai.orchestrator.Service, Optional[Dict[ServiceFeature, Any]]]
    ] = {
        1: {hankai.orchestrator.Service.AUTOCODING_1: None},
    }

    @classmethod
    def supported(
        cls,
        service: Union[str, hankai.orchestrator.Service],
        service_set: Optional[int] = None,
    ) -> bool:
        """Supported DocuVision set and service."""
        supported = False
        _service: Optional[hankai.orchestrator.Service]
        if isinstance(service, str):
            _service = hankai.orchestrator.Service.member_by(member=service)
        else:
            _service = service

        if _service is not None:
            if service_set is None:
                for _, service_features in cls._supported.items():
                    if _service in service_features:
                        supported = True
                        break
            else:
                try:
                    if service_set is not None:
                        _ = cls._supported[service_set][_service]
                        supported = True
                except KeyError:
                    pass

        return supported

    @classmethod
    def features(
        cls, service_set: int, service: hankai.orchestrator.Service
    ) -> Optional[Dict[ServiceFeature, Any]]:
        """Supported DocuVision set and service features."""
        if cls.supported(service_set=service_set, service=service):
            return cls._supported[service_set][service]

        return None

    @classmethod
    def sets(cls, service: Union[str, hankai.orchestrator.Service]) -> List[int]:
        """List of supported DocuVision sets by service."""
        service_sets: List[int] = []

        if isinstance(service, str):
            _service = hankai.orchestrator.Service.member_by(member=service)
            if _service is None:
                return service_sets
        else:
            _service = service

        for service_set, service_features in cls._supported.items():
            if service in service_features:
                service_sets.append(service_set)

        return service_sets

    @classmethod
    def services_by_set(cls, service_set: int) -> List[hankai.orchestrator.Service]:
        """List of supported DocuVision services by set."""
        services: List[hankai.orchestrator.Service] = []

        if service_set not in cls._supported:
            return services

        service_features = cls._supported[service_set]

        for service in service_features.keys():
            services.append(service)

        return services

    @classmethod
    def services_by_set_str(cls, service_set: int) -> List[str]:
        """List of supported DocuVision set services as string."""
        services: List[str] = []

        for service in cls.services_by_set(service_set=service_set):
            services.append(str(service))

        return services

    @classmethod
    def services(cls) -> List[hankai.orchestrator.Service]:
        """List of supported DocuVision services."""
        services: List[hankai.orchestrator.Service] = []
        for _, service_features in cls._supported.items():
            services.extend(service_features.keys())

        return services

    @classmethod
    def services_str(cls) -> List[str]:
        """List of supported DocuVision services as string."""
        services_str_list: List[str] = []
        services = cls.services()
        for service in services:
            services_str_list.append(service.value)

        return services_str_list
