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

# IBM OpenAPI SDK Code Generator Version: 3.62.0-a2a22f95-20221115-162524

"""
IBM Data Fabric Orchestrator control plane API.

API Version: 1.0.0
See: https://fybrik.io
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List
import json

from ibm_cloud_sdk_core import BaseService, DetailedResponse
from ibm_cloud_sdk_core.authenticators.authenticator import Authenticator
from ibm_cloud_sdk_core.get_authenticator import get_authenticator_from_environment
from ibm_cloud_sdk_core.utils import convert_model, datetime_to_string, string_to_datetime

from .common import get_sdk_headers

##############################################################################
# Service
##############################################################################

class IbmDataFabricOrchestratorV1(BaseService):
    """The IBM Data Fabric Orchestrator V1 service."""

    DEFAULT_SERVICE_URL = 'https://api.us-south.dfo.cloud.ibm.com'
    DEFAULT_SERVICE_NAME = 'ibm_data_fabric_orchestrator'

    @classmethod
    def new_instance(cls,
                     service_name: str = DEFAULT_SERVICE_NAME,
                    ) -> 'IbmDataFabricOrchestratorV1':
        """
        Return a new client for the IBM Data Fabric Orchestrator service using the
               specified parameters and external configuration.
        """
        authenticator = get_authenticator_from_environment(service_name)
        service = cls(
            authenticator
            )
        service.configure_service(service_name)
        return service

    def __init__(self,
                 authenticator: Authenticator = None,
                ) -> None:
        """
        Construct a new client for the IBM Data Fabric Orchestrator service.

        :param Authenticator authenticator: The authenticator specifies the authentication mechanism.
               Get up to date information from https://github.com/IBM/python-sdk-core/blob/main/README.md
               about initializing the authenticator of your choice.
        """
        BaseService.__init__(self,
                             service_url=self.DEFAULT_SERVICE_URL,
                             authenticator=authenticator)


    #########################
    # instance-controller
    #########################


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

        if not context_type:
            raise ValueError('context_type must be provided')
        if not context_id:
            raise ValueError('context_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_instance')
        headers.update(sdk_headers)

        params = {
            'context_type': context_type,
            'context_id': context_id
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            del kwargs['headers']
        headers['Accept'] = 'application/json'

        url = '/data_fabric/v1/instances'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request, **kwargs)
        return response


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
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='create_instance')
        headers.update(sdk_headers)

        data = {
            'context_type': context_type,
            'context_id': context_id
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            del kwargs['headers']
        headers['Accept'] = 'application/json'

        url = '/data_fabric/v1/instances'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


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

        if not instance_id:
            raise ValueError('instance_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_instance')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            del kwargs['headers']
        headers['Accept'] = 'application/json'

        path_param_keys = ['instance_id']
        path_param_values = self.encode_path_vars(instance_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/data_fabric/v1/instances/{instance_id}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


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

        if not instance_id:
            raise ValueError('instance_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='delete_instance')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            del kwargs['headers']

        path_param_keys = ['instance_id']
        path_param_values = self.encode_path_vars(instance_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/data_fabric/v1/instances/{instance_id}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response

    #########################
    # application-controller
    #########################


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

        if not instance_id:
            raise ValueError('instance_id must be provided')
        if not intent:
            raise ValueError('intent must be provided')
        if not location:
            raise ValueError('location must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_application')
        headers.update(sdk_headers)

        params = {
            'intent': intent,
            'location': location
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            del kwargs['headers']
        headers['Accept'] = 'application/json'

        path_param_keys = ['instance_id']
        path_param_values = self.encode_path_vars(instance_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/data_fabric/v1/instances/{instance_id}/applications'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request, **kwargs)
        return response


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

        if not instance_id:
            raise ValueError('instance_id must be provided')
        if intent is None:
            raise ValueError('intent must be provided')
        if location is None:
            raise ValueError('location must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='create_application')
        headers.update(sdk_headers)

        data = {
            'intent': intent,
            'location': location
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            del kwargs['headers']
        headers['Accept'] = 'application/json'

        path_param_keys = ['instance_id']
        path_param_values = self.encode_path_vars(instance_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/data_fabric/v1/instances/{instance_id}/applications'.format(**path_param_dict)
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


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
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='reconcile_application')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            del kwargs['headers']

        path_param_keys = ['instance_id', 'application_id']
        path_param_values = self.encode_path_vars(instance_id, application_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/data_fabric/v1/instances/{instance_id}/applications/{application_id}/reconcile'.format(**path_param_dict)
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


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

        if not instance_id:
            raise ValueError('instance_id must be provided')
        if not application_id:
            raise ValueError('application_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_application')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            del kwargs['headers']
        headers['Accept'] = 'application/json'

        path_param_keys = ['instance_id', 'application_id']
        path_param_values = self.encode_path_vars(instance_id, application_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/data_fabric/v1/instances/{instance_id}/applications/{application_id}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


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

        if not instance_id:
            raise ValueError('instance_id must be provided')
        if not application_id:
            raise ValueError('application_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='delete_application')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            del kwargs['headers']

        path_param_keys = ['instance_id', 'application_id']
        path_param_values = self.encode_path_vars(instance_id, application_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/data_fabric/v1/instances/{instance_id}/applications/{application_id}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response

    #########################
    # asset-controller
    #########################


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
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_active_assets')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            del kwargs['headers']
        headers['Accept'] = 'application/json'

        path_param_keys = ['instance_id', 'application_id']
        path_param_values = self.encode_path_vars(instance_id, application_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/data_fabric/v1/instances/{instance_id}/applications/{application_id}/assets'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def add_assets(self,
        instance_id: str,
        application_id: str,
        assets: List['DataAsset'],
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

        if not instance_id:
            raise ValueError('instance_id must be provided')
        if not application_id:
            raise ValueError('application_id must be provided')
        if assets is None:
            raise ValueError('assets must be provided')
        assets = [convert_model(x) for x in assets]
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='add_assets')
        headers.update(sdk_headers)

        data = {
            'assets': assets
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            del kwargs['headers']
        headers['Accept'] = 'application/json'

        path_param_keys = ['instance_id', 'application_id']
        path_param_values = self.encode_path_vars(instance_id, application_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/data_fabric/v1/instances/{instance_id}/applications/{application_id}/assets'.format(**path_param_dict)
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


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

        if not instance_id:
            raise ValueError('instance_id must be provided')
        if not application_id:
            raise ValueError('application_id must be provided')
        if not asset_id:
            raise ValueError('asset_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_asset')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            del kwargs['headers']
        headers['Accept'] = 'application/json'

        path_param_keys = ['instance_id', 'application_id', 'asset_id']
        path_param_values = self.encode_path_vars(instance_id, application_id, asset_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/data_fabric/v1/instances/{instance_id}/applications/{application_id}/assets/{asset_id}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


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

        if not instance_id:
            raise ValueError('instance_id must be provided')
        if not application_id:
            raise ValueError('application_id must be provided')
        if not asset_id:
            raise ValueError('asset_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='remove_asset')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            del kwargs['headers']

        path_param_keys = ['instance_id', 'application_id', 'asset_id']
        path_param_values = self.encode_path_vars(instance_id, application_id, asset_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/data_fabric/v1/instances/{instance_id}/applications/{application_id}/assets/{asset_id}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


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
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_asset_endpoint')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            del kwargs['headers']
        headers['Accept'] = 'application/json'

        path_param_keys = ['instance_id', 'application_id', 'asset_id']
        path_param_values = self.encode_path_vars(instance_id, application_id, asset_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/data_fabric/v1/instances/{instance_id}/applications/{application_id}/assets/{asset_id}/endpoint'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response

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

        if not instance_id:
            raise ValueError('instance_id must be provided')
        if not asset_id:
            raise ValueError('asset_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_wkc_asset')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            del kwargs['headers']
        headers['Accept'] = 'application/json'

        path_param_keys = ['instance_id', 'asset_id']
        path_param_values = self.encode_path_vars(instance_id, asset_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/data_fabric/v1/instances/{instance_id}/assets/{asset_id}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


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

        if not instance_id:
            raise ValueError('instance_id must be provided')
        if not asset_id:
            raise ValueError('asset_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='update_wkc_asset')
        headers.update(sdk_headers)

        data = {
            'profile_status': profile_status
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            del kwargs['headers']
        headers['Accept'] = 'application/json'

        path_param_keys = ['instance_id', 'asset_id']
        path_param_values = self.encode_path_vars(instance_id, asset_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/data_fabric/v1/instances/{instance_id}/assets/{asset_id}'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


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

        if not instance_id:
            raise ValueError('instance_id must be provided')
        if not asset_id:
            raise ValueError('asset_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='delete_wkc_asset')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            del kwargs['headers']

        path_param_keys = ['instance_id', 'asset_id']
        path_param_values = self.encode_path_vars(instance_id, asset_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/data_fabric/v1/instances/{instance_id}/assets/{asset_id}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


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

        if not instance_id:
            raise ValueError('instance_id must be provided')
        if connection_id is None:
            raise ValueError('connection_id must be provided')
        if connection_path is None:
            raise ValueError('connection_path must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='create_wkc_asset')
        headers.update(sdk_headers)

        data = {
            'connection_id': connection_id,
            'connection_path': connection_path,
            'description': description,
            'name': name
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            del kwargs['headers']
        headers['Accept'] = 'application/json'

        path_param_keys = ['instance_id']
        path_param_values = self.encode_path_vars(instance_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/data_fabric/v1/instances/{instance_id}/assets'.format(**path_param_dict)
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


class ListInstanceEnums:
    """
    Enums for list_instance parameters.
    """

    class ContextType(str, Enum):
        """
        Associated context type. A data fabric orchestrator instance must be associated
        with either a catalog or project as its context. The supported values for
        context_type are catalogs or projects.
        """
        PROJECTS = 'projects'
        CATALOGS = 'catalogs'
        SPACES = 'spaces'


##############################################################################
# Models
##############################################################################


class ApplicationResource():
    """
    Information about a particular data fabric orchestrator application.

    :attr str application_id: (optional) Identifier of the data fabric orchestrator
          application.
    :attr str state: (optional) Data fabric orchestrator application status.
    :attr str message: (optional) Additional information of the state of data fabric
          orchestrator application.
    """

    def __init__(self,
                 *,
                 application_id: str = None,
                 state: str = None,
                 message: str = None) -> None:
        """
        Initialize a ApplicationResource object.

        :param str application_id: (optional) Identifier of the data fabric
               orchestrator application.
        :param str state: (optional) Data fabric orchestrator application status.
        :param str message: (optional) Additional information of the state of data
               fabric orchestrator application.
        """
        self.application_id = application_id
        self.state = state
        self.message = message

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ApplicationResource':
        """Initialize a ApplicationResource object from a json dictionary."""
        args = {}
        if 'application_id' in _dict:
            args['application_id'] = _dict.get('application_id')
        if 'state' in _dict:
            args['state'] = _dict.get('state')
        if 'message' in _dict:
            args['message'] = _dict.get('message')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ApplicationResource object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'application_id') and self.application_id is not None:
            _dict['application_id'] = self.application_id
        if hasattr(self, 'state') and self.state is not None:
            _dict['state'] = self.state
        if hasattr(self, 'message') and self.message is not None:
            _dict['message'] = self.message
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ApplicationResource object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ApplicationResource') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ApplicationResource') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class AssetResource():
    """
    Represents an asset and its state within a DFO application. Also contains additional
    messages if there are problems with adding the asset to a DFO application.

    :attr str asset_id: (optional) Identifier of the data asset.
    :attr str state: (optional) Status of the data asset in the data fabric
          orchestrator application.
    :attr str message: (optional) Reason for the error/failed state of the data
          asset in the data fabric orchestrator application.
    :attr str endpoint: (optional) Endpoint of the data asset.
    """

    def __init__(self,
                 *,
                 asset_id: str = None,
                 state: str = None,
                 message: str = None,
                 endpoint: str = None) -> None:
        """
        Initialize a AssetResource object.

        :param str asset_id: (optional) Identifier of the data asset.
        :param str state: (optional) Status of the data asset in the data fabric
               orchestrator application.
        :param str message: (optional) Reason for the error/failed state of the
               data asset in the data fabric orchestrator application.
        :param str endpoint: (optional) Endpoint of the data asset.
        """
        self.asset_id = asset_id
        self.state = state
        self.message = message
        self.endpoint = endpoint

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'AssetResource':
        """Initialize a AssetResource object from a json dictionary."""
        args = {}
        if 'asset_id' in _dict:
            args['asset_id'] = _dict.get('asset_id')
        if 'state' in _dict:
            args['state'] = _dict.get('state')
        if 'message' in _dict:
            args['message'] = _dict.get('message')
        if 'endpoint' in _dict:
            args['endpoint'] = _dict.get('endpoint')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a AssetResource object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'asset_id') and self.asset_id is not None:
            _dict['asset_id'] = self.asset_id
        if hasattr(self, 'state') and self.state is not None:
            _dict['state'] = self.state
        if hasattr(self, 'message') and self.message is not None:
            _dict['message'] = self.message
        if hasattr(self, 'endpoint') and self.endpoint is not None:
            _dict['endpoint'] = self.endpoint
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this AssetResource object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'AssetResource') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'AssetResource') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class AssetResources():
    """
    Collection of AssetResource.

    :attr List[AssetResource] assets: (optional) Collection of asset resource.
    """

    def __init__(self,
                 *,
                 assets: List['AssetResource'] = None) -> None:
        """
        Initialize a AssetResources object.

        :param List[AssetResource] assets: (optional) Collection of asset resource.
        """
        self.assets = assets

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'AssetResources':
        """Initialize a AssetResources object from a json dictionary."""
        args = {}
        if 'assets' in _dict:
            args['assets'] = [AssetResource.from_dict(v) for v in _dict.get('assets')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a AssetResources object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'assets') and self.assets is not None:
            assets_list = []
            for v in self.assets:
                if isinstance(v, dict):
                    assets_list.append(v)
                else:
                    assets_list.append(v.to_dict())
            _dict['assets'] = assets_list
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this AssetResources object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'AssetResources') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'AssetResources') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class DataAsset():
    """
    Data access information of a data asset to add to the data fabric orchestrator
    application.  Encapsulates information required to access a data asset.

    :attr str asset_id: Identifier of the data asset.
    :attr str protocol: (optional) Protocol used to access the data asset.
    :attr str format: (optional) Format of the data asset.
    """

    def __init__(self,
                 asset_id: str,
                 *,
                 protocol: str = None,
                 format: str = None) -> None:
        """
        Initialize a DataAsset object.

        :param str asset_id: Identifier of the data asset.
        :param str protocol: (optional) Protocol used to access the data asset.
        :param str format: (optional) Format of the data asset.
        """
        self.asset_id = asset_id
        self.protocol = protocol
        self.format = format

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'DataAsset':
        """Initialize a DataAsset object from a json dictionary."""
        args = {}
        if 'asset_id' in _dict:
            args['asset_id'] = _dict.get('asset_id')
        else:
            raise ValueError('Required property \'asset_id\' not present in DataAsset JSON')
        if 'protocol' in _dict:
            args['protocol'] = _dict.get('protocol')
        if 'format' in _dict:
            args['format'] = _dict.get('format')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a DataAsset object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'asset_id') and self.asset_id is not None:
            _dict['asset_id'] = self.asset_id
        if hasattr(self, 'protocol') and self.protocol is not None:
            _dict['protocol'] = self.protocol
        if hasattr(self, 'format') and self.format is not None:
            _dict['format'] = self.format
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this DataAsset object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'DataAsset') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'DataAsset') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class ProtocolEnum(str, Enum):
        """
        Protocol used to access the data asset.
        """
        DFO_FLIGHT = 'dfo-flight'


    class FormatEnum(str, Enum):
        """
        Format of the data asset.
        """
        ARROW = 'arrow'


class InstanceResource():
    """
    Information about the data fabric orchestrator instance.

    :attr str instance_id: (optional) Identifier of the data fabric orchestrator
          instance.
    :attr str context_type: Type of the context to associate this data fabric
          orchestrator instance with.
    :attr str context_id: Identifier of the context to associate this data fabric
          orchestrator instance with.
    :attr str state: (optional) Data fabric orchestrator instance status.
    :attr datetime creation_time: (optional) Date and time when the data fabric
          orchestrator instance was created.
    """

    def __init__(self,
                 context_type: str,
                 context_id: str,
                 *,
                 instance_id: str = None,
                 state: str = None,
                 creation_time: datetime = None) -> None:
        """
        Initialize a InstanceResource object.

        :param str context_type: Type of the context to associate this data fabric
               orchestrator instance with.
        :param str context_id: Identifier of the context to associate this data
               fabric orchestrator instance with.
        """
        self.instance_id = instance_id
        self.context_type = context_type
        self.context_id = context_id
        self.state = state
        self.creation_time = creation_time

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'InstanceResource':
        """Initialize a InstanceResource object from a json dictionary."""
        args = {}
        if 'instance_id' in _dict:
            args['instance_id'] = _dict.get('instance_id')
        if 'context_type' in _dict:
            args['context_type'] = _dict.get('context_type')
        else:
            raise ValueError('Required property \'context_type\' not present in InstanceResource JSON')
        if 'context_id' in _dict:
            args['context_id'] = _dict.get('context_id')
        else:
            raise ValueError('Required property \'context_id\' not present in InstanceResource JSON')
        if 'state' in _dict:
            args['state'] = _dict.get('state')
        if 'creation_time' in _dict:
            args['creation_time'] = string_to_datetime(_dict.get('creation_time'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a InstanceResource object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'instance_id') and getattr(self, 'instance_id') is not None:
            _dict['instance_id'] = getattr(self, 'instance_id')
        if hasattr(self, 'context_type') and self.context_type is not None:
            _dict['context_type'] = self.context_type
        if hasattr(self, 'context_id') and self.context_id is not None:
            _dict['context_id'] = self.context_id
        if hasattr(self, 'state') and getattr(self, 'state') is not None:
            _dict['state'] = getattr(self, 'state')
        if hasattr(self, 'creation_time') and getattr(self, 'creation_time') is not None:
            _dict['creation_time'] = datetime_to_string(getattr(self, 'creation_time'))
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this InstanceResource object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'InstanceResource') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'InstanceResource') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class ContextTypeEnum(str, Enum):
        """
        Type of the context to associate this data fabric orchestrator instance with.
        """
        PROJECTS = 'projects'
        CATALOGS = 'catalogs'
        SPACES = 'spaces'


class WkcCreateAssetResource():
    """
    Response returned for 'wkc create asset' API call.

    :attr str asset_id: (optional) Identifier of the WKC asset.
    :attr str connection_id: (optional) Identifier of the connection where asset is
          added.
    :attr str path: (optional) Path of the connection to add the asset.
    :attr str asset_type: (optional) Asset type to be added dataAsset or
          ConnectionAsset.
    :attr str description: (optional) Short description of the added asset.
    """

    def __init__(self,
                 *,
                 asset_id: str = None,
                 connection_id: str = None,
                 path: str = None,
                 asset_type: str = None,
                 description: str = None) -> None:
        """
        Initialize a WkcCreateAssetResource object.

        :param str asset_id: (optional) Identifier of the WKC asset.
        :param str connection_id: (optional) Identifier of the connection where
               asset is added.
        :param str path: (optional) Path of the connection to add the asset.
        :param str asset_type: (optional) Asset type to be added dataAsset or
               ConnectionAsset.
        :param str description: (optional) Short description of the added asset.
        """
        self.asset_id = asset_id
        self.connection_id = connection_id
        self.path = path
        self.asset_type = asset_type
        self.description = description

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WkcCreateAssetResource':
        """Initialize a WkcCreateAssetResource object from a json dictionary."""
        args = {}
        if 'asset_id' in _dict:
            args['asset_id'] = _dict.get('asset_id')
        if 'connection_id' in _dict:
            args['connection_id'] = _dict.get('connection_id')
        if 'path' in _dict:
            args['path'] = _dict.get('path')
        if 'asset_type' in _dict:
            args['asset_type'] = _dict.get('asset_type')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WkcCreateAssetResource object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'asset_id') and self.asset_id is not None:
            _dict['asset_id'] = self.asset_id
        if hasattr(self, 'connection_id') and self.connection_id is not None:
            _dict['connection_id'] = self.connection_id
        if hasattr(self, 'path') and self.path is not None:
            _dict['path'] = self.path
        if hasattr(self, 'asset_type') and self.asset_type is not None:
            _dict['asset_type'] = self.asset_type
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WkcCreateAssetResource object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WkcCreateAssetResource') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WkcCreateAssetResource') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WkcGetAssetResource():
    """
    Return the profiling status of an asset.

    :attr str asset_id: (optional) Identifier of the WKC asset.
    :attr str profile_status: (optional) Profiling status of the asset.
    """

    def __init__(self,
                 *,
                 asset_id: str = None,
                 profile_status: str = None) -> None:
        """
        Initialize a WkcGetAssetResource object.

        :param str asset_id: (optional) Identifier of the WKC asset.
        :param str profile_status: (optional) Profiling status of the asset.
        """
        self.asset_id = asset_id
        self.profile_status = profile_status

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WkcGetAssetResource':
        """Initialize a WkcGetAssetResource object from a json dictionary."""
        args = {}
        if 'asset_id' in _dict:
            args['asset_id'] = _dict.get('asset_id')
        if 'profile_status' in _dict:
            args['profile_status'] = _dict.get('profile_status')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WkcGetAssetResource object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'asset_id') and self.asset_id is not None:
            _dict['asset_id'] = self.asset_id
        if hasattr(self, 'profile_status') and self.profile_status is not None:
            _dict['profile_status'] = self.profile_status
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WkcGetAssetResource object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WkcGetAssetResource') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WkcGetAssetResource') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WkcUpdateAssetResource():
    """
    Currently, returns the asset profile status. More response body may be added in the
    future.

    :attr str profile_status: (optional) Profiling status of the asset.
    """

    def __init__(self,
                 *,
                 profile_status: str = None) -> None:
        """
        Initialize a WkcUpdateAssetResource object.

        :param str profile_status: (optional) Profiling status of the asset.
        """
        self.profile_status = profile_status

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WkcUpdateAssetResource':
        """Initialize a WkcUpdateAssetResource object from a json dictionary."""
        args = {}
        if 'profile_status' in _dict:
            args['profile_status'] = _dict.get('profile_status')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WkcUpdateAssetResource object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'profile_status') and self.profile_status is not None:
            _dict['profile_status'] = self.profile_status
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WkcUpdateAssetResource object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WkcUpdateAssetResource') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WkcUpdateAssetResource') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other
