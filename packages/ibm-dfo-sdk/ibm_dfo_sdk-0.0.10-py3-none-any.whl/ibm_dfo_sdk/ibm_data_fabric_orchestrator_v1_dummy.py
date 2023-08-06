# coding: utf-8

# (C) Copyright IBM Corp. 2023.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
IBM Data Fabric Orchestrator control plane API.

API Version: 1.0.0
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List
import json
import uuid

from ibm_cloud_sdk_core import BaseService, DetailedResponse
from ibm_cloud_sdk_core.authenticators.authenticator import Authenticator
from ibm_cloud_sdk_core.get_authenticator import get_authenticator_from_environment
from ibm_cloud_sdk_core.utils import convert_model, datetime_to_string, string_to_datetime
from .ibm_data_fabric_orchestrator_v1 import IbmDataFabricOrchestratorV1, ApplicationResource, AssetResource, DataAsset, InstanceResource

from .common import get_sdk_headers

##############################################################################
# Service
##############################################################################

class DfoNotInstalledError(Exception):
    """Exception raised during ."""
    def __init__(self, message = None):
        if message is None:
            self.message = "This method is not supported when DFO is not installed"
        else:
            self.message = message

class IbmDataFabricOrchestratorV1Dummy(IbmDataFabricOrchestratorV1):
    """The IBM Data Fabric Orchestrator V1 service."""
    def __init__(self, flight_url, authenticator: Authenticator = None) -> None:
        BaseService.__init__(self,
                             service_url = None,
                             authenticator = authenticator)

        # Save off the flight url.  We'll need it later to synthesize endpoint requests.
        self.flight_url = flight_url

    def create_instance(self,
        context_type: str,
        context_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Create data fabric orchestrator instance.

        Create a data fabric orchestrator instance for a specified context.

        :param str context_type: Type of the context to associate this data fabric
               orchestrator instance with.
        :param str context_id: Identifier of the context to associate this data
               fabric orchestrator instance with.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `InstanceResource` object
        """

        if context_type is None:
            raise ValueError('context_type must be provided')
        if context_id is None:
            raise ValueError('context_id must be provided')

        # Make up a response
        return DetailedResponse(
            response = InstanceResource(
                instance_id = context_id,
                state = "CREATED",
                creation_time = datetime.now(timezone.utc),
                context_type = context_type,
                context_id = context_id
            ).to_dict(),
            status_code = 201
        )


    def list_instance(self,
        context_type: str,
        context_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        List data fabric orchestrator instance.

        List the data fabric orchestrator instance for a specified context ID and type.

        :param str context_type: Associated context type. A data fabric
               orchestrator instance must be associated with either a catalog or project
               as its context. The supported values for context_type are catalogs or
               projects.
        :param str context_id: Identifier of the catalog or project that the
               instance is associated with.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `InstanceResource` object
        """

        if context_type is None:
            raise ValueError('context_type must be provided')
        if context_id is None:
            raise ValueError('context_id must be provided')

        # Make up a response
        return DetailedResponse(
            response = InstanceResource(
                instance_id = context_id,
                state = "CREATED",
                creation_time = datetime.now(timezone.utc),
                context_type = context_type,
                context_id = context_id
            ).to_dict(),
            status_code = 200
        )


    def get_instance(self,
        instance_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get data fabric orchestrator instance.

        Retrieve information about a particular data fabric orchestrator instance, such as
        status, creator, creation time, context type (catalog or project), and context ID.

        :param str instance_id: Identifier of a data fabric orchestrator instance.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `InstanceResource` object
        """

        if instance_id is None:
            raise ValueError('instance_id must be provided')

        # Make up a response
        return DetailedResponse(
            response = InstanceResource(
                instance_id = instance_id,
                state = "CREATED",
                creation_time = datetime.now(timezone.utc),
                context_id = instance_id,
                context_type = "catalogs"
            ).to_dict(),
            status_code = 200
        )


    def delete_instance(self,
        instance_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Delete the data fabric orchestrator instance.

        Delete the specified data fabric orchestrator instance. After deletion, the
        instance details are no longer accessible.

        :param str instance_id: Identifier of a data fabric orchestrator instance.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if instance_id is None:
            raise ValueError('instance_id must be provided')

        # The delete does nothing, and has no response except the status_code
        return DetailedResponse(status_code = 204)


    def create_application(self,
        instance_id: str,
        intent: str,
        location: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Create data fabric orchestrator application.

        Create data fabric orchestrator application for the specified location and intent.
        A data fabric orchestrator application handles the policy enforcement on data
        asset that is accessed.

        :param str instance_id: Identifier of a data fabric orchestrator instance.
        :param str intent: Purpose for which the application is used.
        :param str location: Location where the client for this application is run.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `ApplicationResource` object
        """

        if instance_id is None:
            raise ValueError('instance_id must be provided')
        if intent is None:
            raise ValueError('intent must be provided')
        if location is None:
            raise ValueError('location must be provided')

        # Make up a response
        return DetailedResponse(
            response = ApplicationResource(
                application_id = str(uuid.uuid5(uuid.UUID(instance_id), intent + "/" + location)),
                state = "Ready"
            ).to_dict(),
            status_code = 201
        )


    def list_application(self,
        instance_id: str,
        intent: str,
        location: str,
        **kwargs
    ) -> DetailedResponse:
        """
        List data fabric orchestrator application.

        List the data fabric orchestrator application for the specified location and
        intent.

        :param str instance_id: Identifier of a data fabric orchestrator instance.
        :param str intent: Purpose of the data fabric orchestrator application.
        :param str location: Location of the data fabric orchestrator application.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `ApplicationResource` object
        """

        if instance_id is None:
            raise ValueError('instance_id must be provided')
        if intent is None:
            raise ValueError('intent must be provided')
        if location is None:
            raise ValueError('location must be provided')

        # Make up a response
        return DetailedResponse(
            response = ApplicationResource(
                application_id = str(uuid.uuid5(uuid.UUID(instance_id), intent + "/" + location)),
                state = "Ready"
            ).to_dict(),
            status_code = 200
        )


    def get_application(self,
        instance_id: str,
        application_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get data fabric orchestrator application.

        Retrieve information about a particular data fabric orchestrator application, such
        as application ID, state, and message.

        :param str instance_id: Identifier of a data fabric orchestrator instance.
        :param str application_id: Identifier of a data fabric orchestrator
               application in a data fabric orchestrator instance.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `ApplicationResource` object
        """

        if instance_id is None:
            raise ValueError('instance_id must be provided')
        if application_id is None:
            raise ValueError('application_id must be provided')

        # Make up a response
        return DetailedResponse(
            response = ApplicationResource(
                application_id = application_id,
                state = "Ready"
            ).to_dict(),
            status_code = 200
        )


    def delete_application(self,
        instance_id: str,
        application_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Delete data fabric orchestrator application.

        Delete data fabric orchestrator application from the specified instance. After
        deletion, the application is no longer available to work with data assets.

        :param str instance_id: Identifier of a data fabric orchestrator instance.
        :param str application_id: Identifier of a data fabric orchestrator
               application in a data fabric orchestrator instance.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if instance_id is None:
            raise ValueError('instance_id must be provided')
        if application_id is None:
            raise ValueError('application_id must be provided')

        # The delete does nothing, and has no response except the status_code
        return DetailedResponse(status_code = 204)

    def reconcile_application(self,
        instance_id: str,
        application_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Reconcile data fabric orchestrator application.

        Calling this API triggers the data fabric orchestrator application to reconcile
        the asset metadata and policies stored in its internal cache. A client is required
        to call this API for a long running application, if asset metadata or access
        policies are changed from the time the application was started.

        :param str instance_id: Identifier of a data fabric orchestrator instance.
        :param str application_id: Identifier of a data fabric orchestrator
               application in a data fabric orchestrator instance.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if not instance_id:
            raise ValueError('instance_id must be provided')
        if not application_id:
            raise ValueError('application_id must be provided')

        # The reconcile does nothing, and has no response except the status_code
        return DetailedResponse(status_code = 204)

    def list_active_assets(self,
        instance_id: str,
        application_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        List active data assets from an application.

        Get list of active data assets of a specified application.

        :param str instance_id: Identifier of a data fabric orchestrator instance.
        :param str application_id: Identifier of a data fabric orchestrator
               application in a data fabric orchestrator instance.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `AssetResources` object
        """

        if not instance_id:
            raise ValueError('instance_id must be provided')
        if not application_id:
            raise ValueError('application_id must be provided')

        return DetailedResponse(
            response = { "assets": []
            },
            status_code = 200
        )

    def add_assets(self,
        instance_id: str,
        application_id: str,
        assets: List['DataAsset'] = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Add assets to application.

        Add a list of data assets to a specified application. All assets that you want to
        access with policy enforcement must be added to a data fabric orchestrator
        application.

        :param str instance_id: Identifier of a data fabric orchestrator instance.
        :param str application_id: Identifier of a data fabric orchestrator
               application in a data fabric orchestrator instance.
        :param List[DataAsset] assets: Collection of data assets.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `AssetResources` object
        """

        if instance_id is None:
            raise ValueError('instance_id must be provided')
        if application_id is None:
            raise ValueError('application_id must be provided')
        if assets is None:
            raise ValueError('assets must be provided')

        assets_result = []
        for a in assets:
            if a.format is None or a.format == "arrow":
                assets.append(
                    AssetResource(
                        asset_id = a.asset_id,
                        state = "ADDED",
                        endpoint = self.flight_url
                    ).to_dict()
                )
            else:
                assets.append(
                    AssetResource(
                        asset_id = a.asset_id,
                        state = "REJECTED",
                        message = "Only arrow format is supported by the IbmDataFabricOrchestratorV1Dummy service."
                    ).to_dict()
                )

        return DetailedResponse(
            response = { 'assets': assets_result },
            status_code = 201
        )

    def get_asset(self,
        instance_id: str,
        application_id: str,
        asset_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get data access information for an asset from an application.

        Retrieve information about a particular data asset, such as asset ID, state,
        message, and endpoint.

        :param str instance_id: Identifier of a data fabric orchestrator instance.
        :param str application_id: Identifier of a data fabric orchestrator
               application in a data fabric orchestrator instance.
        :param str asset_id: Identifier of a data asset in a data fabric
               orchestrator application.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `AssetResource` object
        """

        if instance_id is None:
            raise ValueError('instance_id must be provided')
        if application_id is None:
            raise ValueError('application_id must be provided')
        if asset_id is None:
            raise ValueError('asset_id must be provided')

        return DetailedResponse(
            response = AssetResource(
                asset_id = asset_id,
                state = "Ready",
                endpoint = self.flight_url
            ).to_dict(),
            status_code = 200
        )


    def remove_asset(self,
        instance_id: str,
        application_id: str,
        asset_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Remove the data access for a specified asset from an application.

        Remove data access asset from the specified data fabric orchestrator application
        in a data fabric orchestrator instance. After removal, the data asset can no
        longer be retrieved through the application. To access, you must add the data
        asset again.

        :param str instance_id: Identifier of a data fabric orchestrator instance.
        :param str application_id: Identifier of a data fabric orchestrator
               application in a data fabric orchestrator instance.
        :param str asset_id: Identifier of a data asset in a data fabric
               orchestrator application.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if instance_id is None:
            raise ValueError('instance_id must be provided')
        if application_id is None:
            raise ValueError('application_id must be provided')
        if asset_id is None:
            raise ValueError('asset_id must be provided')

        # The delete does nothing, and has no response except the status_code
        return DetailedResponse(status_code = 204)

    def get_asset_endpoint(self,
        instance_id: str,
        application_id: str,
        asset_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get data access endpoint for an asset from an application.

        Returns an endpoint that can be used by consumers for making further requests to
        Apache Arrow Flight service for accessing data asset.

        :param str instance_id: Identifier of a data fabric orchestrator instance.
        :param str application_id: Identifier of a data fabric orchestrator
               application in a data fabric orchestrator instance.
        :param str asset_id: Identifier of a data asset in a data fabric
               orchestrator application.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `str` result
        """

        if not instance_id:
            raise ValueError('instance_id must be provided')
        if not application_id:
            raise ValueError('application_id must be provided')
        if not asset_id:
            raise ValueError('asset_id must be provided')

        return DetailedResponse(
            response = self.flight_url,
            status_code = 200
        )



    #########################
    # wkc-asset-controller
    #########################


    def get_wkc_asset(self,
        instance_id: str,
        asset_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get WKC data asset.

        Retrieve profiling information about a particular WKC data asset.

        :param str instance_id: Identifier of a data fabric orchestrator instance.
        :param str asset_id: Identifier of a data asset in a data fabric
               orchestrator application.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WkcGetAssetResource` object
        """
        raise DfoNotInstalledError()


    def update_wkc_asset(self,
        instance_id: str,
        asset_id: str,
        *,
        profile_status: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Update the WKC data asset.

        Use this API to update WKC data asset. For example, initiate profiling of the data
        asset.

        :param str instance_id: Identifier of a data fabric orchestrator instance.
        :param str asset_id: Identifier of a data asset in a data fabric
               orchestrator application.
        :param str profile_status: (optional) Profiling status of the asset.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WkcUpdateAssetResource` object
        """
        raise DfoNotInstalledError()


    def delete_wkc_asset(self,
        instance_id: str,
        asset_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Remove the asset from Watson Knowledge Catalog.

        Removes the asset entry from Watson Knowledge Catalog. The original data asset is
        not impacted by this operation.

        :param str instance_id: Identifier of a data fabric orchestrator instance.
        :param str asset_id: Identifier of a data asset in a data fabric
               orchestrator application.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """
        raise DfoNotInstalledError()


    def create_wkc_asset(self,
        instance_id: str,
        connection_id: str,
        connection_path: str,
        *,
        description: str = None,
        name: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Create asset in Watson Knowledge Catalog.

        Create a new WKC data asset for a given connection_id.

        :param str instance_id: Identifier of a data fabric orchestrator instance.
        :param str connection_id: connection id in which asset to be added.
        :param str connection_path: connection path for the assets.
        :param str description: (optional) Asset description.
        :param str name: (optional) Asset name to identify the asset on UI.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WkcCreateAssetResource` object
        """
        raise DfoNotInstalledError()
