# coding: utf-8

# (C) Copyright IBM Corp. 2021.
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
IBM Data Fabric Orchestrator Control Plane Extended API.
"""

import time
from typing import List
import requests
from pyarrow import flight
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import Authenticator
from .ibm_data_fabric_orchestrator_v1 import IbmDataFabricOrchestratorV1, DataAsset, WkcGetAssetResource, WkcUpdateAssetResource
from .token_auth_handler import TokenClientAuthHandler

DEFAULT_APPLICATION_LOCATION = "Unset"
APPLICATION_LOCATION_FILENAME = "/opt/ibm/fabric/conf/location"

class ResourceNotFoundError(Exception):
    """Exception raised if a particular entity does not exist on the server."""
    def __init__(self, uri, message):
        self.uri = uri
        self.message = message

class AssetError(Exception):
    """Exception raised if a data asset has a particular error state that makes it currently unusable."""
    def __init__(self, message):
        self.message = message

class WkcAssetError(Exception):
    """Exception raised during ."""
    def __init__(self, message):
        self.message = message

class DFOInstance():
    """Represents a data fabric orchestrator instance that can be used to find, create, and use a data fabric orchestrator applications."""

    @classmethod
    def findOrCreate(cls, service: IbmDataFabricOrchestratorV1, context_type: str, context_id: str) -> 'DFOInstance':
        """Attempt to find an existing DFOInstance for the specified context, or create one if none were found.

        Uses the passed-in IbmDataFabricOrchestratorV1 service for all API calls, which must have its endpoint and authenticators 
        properly configured. If given an IbmDataFabricOrchestratorV1Dummy service, all normal operations succeed, and when asked
        for an Apache Arrow Flight endpoint, the standard Flight service (nonenforcing) endpoint is returned for your convenience.

        When you use the IbmDataFabricOrchestratorV1 service, the specified context_id and context_type pair must exist in the 
        Watson Knowledge Catalog the service is using, and you must have authority to see it. If you use the IbmDataFabricOrchestratorV1Dummy
        service, the context is not queried, might not exist, and no authority is required.
        """

        # This will throw an ApiException if there was a problem with the service or we couldn't find an instance for the context.
        # We'll have to catch that, since we want to create a new one if it's just that we couldn't find one.
        try:
            rsp = service.list_instance(context_type, context_id)
        except ApiException as e:
            if e.code == 404:
                # Couldn't find an instance for this context. We'll have to create a new one.
                # This could throw a new exception if we can't create an instance, or the service is bad or whatever.
                # But we'll just let that one propogate, as we've done all we can here.
                rsp = service.create_instance(context_type, context_id)
            else:
                # Some other error with the service.  Let it propogate.
                raise
        # If we've made it here, we've either found or created an instance, and rsp should have the details.
        dfi = cls(service, rsp.result["instance_id"], resource=rsp.result)
        return dfi

    @classmethod
    def get(cls, service: IbmDataFabricOrchestratorV1, id: str) -> 'DFOInstance':
        """Attempt to retrieve a particular DFOInstance by ID.

        If no instance by that ID currently exists, or you do not have authority to see it, a ResourceNotFoundError is raised.

        A DFOInstance is not created, if one is not found.

        If you use the IbmDataFabricOrchestratorV1Dummy service, a dummy DFOInstance is returned in all cases that can be used
        for further operations. IBM Data Fabric Orchestrator and the backend don't exist.
        """

        # This will throw an ApiException if there was a problem with the service or we couldn't find the id.
        # We'll just let that propogate
        try:
            rsp = service.get_instance(id)
        except ApiException as e:
            if e.code == 404:
                raise ResourceNotFoundError(e.http_response.url, "Instance not found.")
            else:
                raise
        dfi = cls(service, id, resource=rsp.result)
        return dfi

    def __init__(self, service: IbmDataFabricOrchestratorV1, id: str, *, resource = None):
        self._svc = service
        self.id = id
        if resource is not None:
            #self.href = resource["href"]
            self.creation_time = resource["creation_time"] if "creation_time" in resource else None
            self.context_type = resource["context_type"] if "context_type" in resource else None
            self.context_id = resource["context_id"] if "context_id" in resource else None
        # Load in the default location, if we can, from the runtime context.
        try:
            with open(APPLICATION_LOCATION_FILENAME, "r") as loc_file:
                self.default_location = loc_file.readline().rstrip('\n').lstrip().rstrip()
                if self.default_location == "":
                    self.default_location = DEFAULT_APPLICATION_LOCATION
        except FileNotFoundError:
            # This is fine, just use the default location
            self.default_location = DEFAULT_APPLICATION_LOCATION

    def _get(self) -> requests.Response:
        try:
            rsp = self._svc.get_instance(self.id)
        except ApiException as e:
            if e.code == 404:
                raise ResourceNotFoundError(e.http_response.url, "Instance not found.")
            else:
                raise
        return rsp.result

    def getStatus(self) -> str:
        """Retrieve the status of the DFOInstance.

        An API call to the service is made to get the status, every time.

        When you use the IbmDataFabricOrchestratorV1Dummy service, the instance status is reported as CREATED.
        """

        # Since status could change, we'll just go get it every time somebody asks
        rsp = self._get()
        return rsp["state"] if "state" in rsp else None

    def delete(self):
        """Request that this DFOInstance to be removed.

        When you use the IbmDataFabricOrchestratorV1Dummy service, this call is silently ignored, as nothing is
        removed on the backend.
        """
        self._svc.delete_instance(self.id)

    def findOrCreateApplication(self, intent: str, *, location: str = None) -> 'DFOApplication':
        """Attempt to find an existing DFOApplication in this DFOInstance for the specified intent and
        location, or create one if one does not exist.

        If location is not specified, attempts to use the location of the current Runtime context, e.g.
        When the SDK is invoked from within a Watson Studio notebook environment, the “location” attribute
        is automatically set, based on the location where the notebook runtime is running from.

        When you use the IbmDataFabricOrchestratorV1Dummy service, always finds the specified application
        and returns a DFOApplication object that can be used for further queries, without going to the backend
        IBM Data Fabric Orchestrator service, which doesn't exist.
        """

        # Determine the location if not passed in
        if location is None:
            location = self.default_location

        # Try to find the application first, and then create it if it doesn't exist.
        try:
            rsp = self._svc.list_application(self.id, intent, location)
        except ApiException as e:
            if e.code == 404:
                # Couldn't find an application for this intent/location.  We'll need to create one.
                # This could throw a new exception if we can't create an application, or the service is bad or whatever.
                # But we'll just let that one propogate, as we've done all we can here.
                rsp = self._svc.create_application(self.id, intent, location)
            else:
                # Some other error with the service.  Let it propogate.
                raise
        # If we've made it here, we've either found or created an application, and rsp should have the details.
        dfa = DFOApplication(self._svc, self.id, rsp.result["application_id"], resource=rsp.result)
        return dfa
    
    def createAsset(self,
        connection_id: str,
        connection_path: str,
        description: str = None,
        name: str = None,
    ) -> str:
        """Create an asset on WKC and start the profiling process when necessary (i.e. when the context 
        is not an auto-profile catalog). 

        Required parameters are the connection ID and the connection path of the remote data source asset.
        If a name is not provided, the connection path is used. If a description is not provided, the asset 
        description is blank. 
        
        Note: The format of the connection path varies based on data source type.
        """

        if connection_id is None:
            raise ValueError('connection_id must be provided')
        if connection_path is None:
            raise ValueError('connection_path must be provided')
        try:
            rsp = self._svc.create_wkc_asset(self.id, connection_id, connection_path, description = description, name = name)
        except ApiException as e:
            raise
        return rsp.result["asset_id"]
    
    def deleteAsset(self,
        asset_id: str,
    ):
        """Request that the asset on WKC to be removed. It will not affect the data source asset.
        """
        self._svc.delete_wkc_asset(self.id, asset_id)

    def getAsset(self,
        asset_id: str,
    ) -> WkcGetAssetResource:
        """Retrieve the profile status of the WKC asset.
        """
        try:
            rsp = self._svc.get_wkc_asset(self.id, asset_id)
        except ApiException as e:
            if e.code == 404:
                raise ResourceNotFoundError(e.http_response.url, "Asset not found.")
            else:
                # Some other error with the service.  Let it propogate.
                raise
        return rsp.result
    
    def updateAsset(self,
        asset_id: str,
        profile_status: str = None,
    ) -> WkcUpdateAssetResource:
        """Either create the profile if it doesn’t exist or recreate it if it already exists. 
        """
        try:
            rsp = self._svc.update_wkc_asset(self.id, asset_id, profile_status = profile_status)
        except ApiException:
            raise
        return rsp.result

    def waitForAssetProfile(self, asset_id: str, *, timeout=None, interval=0.1):
        """Periodically queries the WKC asset for the profiled status.

        Returns only when the WKC asset is in the profiled state.

        If the WKC asset never becomes profiled within the timeout period (in seconds), 
        the TimeoutError exception is raised.

        If the WKC asset changes to an Error or Disabled state, an WkcAssetError exception 
        is raised with more information.

        If the WKC asset has state not_profiled then will trigger profile.

        Status query frequency can be overridden by using the interval parameter (in seconds, defaults to 0.1 seconds).
        """
        start_time = time.monotonic()
        rsp = self.getAsset(asset_id)
        while "profile_status" not in rsp or rsp["profile_status"] != "profiled":
            if "profile_status" in rsp and rsp["profile_status"] == "not_profiled":
                self.updateAsset(asset_id)
            if "profile_status" in rsp and rsp["profile_status"] == "profile_disabled":
                raise WkcAssetError(rsp["message"] if "message" in rsp else "Profile is disabled")
            if "profile_status" in rsp and rsp["profile_status"] == "error":
                raise WkcAssetError(rsp["message"] if "message" in rsp else "Unknown profile Error")
            if timeout is not None and time.monotonic() - start_time >= timeout:
                raise TimeoutError
            time.sleep(interval)
            rsp  = self.getAsset(asset_id)

    def getApplication(self, application_id: str) -> 'DFOApplication':
        """Attempt to retrieve a particular DFOApplication from this DFOInstance by ID.

        If no application by that ID currently exists in this instance, or you do not have authority to see it, a ResourceNotFoundErroris raised.

        A DFOApplication is not created, if one is not found.

        If you use the IbmDataFabricOrchestratorV1Dummy service, a dummy DFOApplication is returned in all cases that can be used for further 
        operations. IBM Data Fabric Orchestrator and the backend don't exist.
        """

        # This will throw an ApiException if there was a problem with the service or we couldn't find the id.
        # We'll just let that propogate
        try:
            rsp = self._svc.get_application(self.id, application_id)
        except ApiException as e:
            if e.code == 404:
                raise ResourceNotFoundError(e.http_response.url, "Application not found.")
            else:
                raise
        dfa = DFOApplication(self._svc, self.id, application_id, resource=rsp.result)
        return dfa


class DFOApplication():
    """Represents a data fabric orchestrator application that can be used to find, create, and use data assets."""

    def __init__(self, service: IbmDataFabricOrchestratorV1, instance_id: str, id: str, *, resource=None):
        self._svc = service
        self._instance_id = instance_id
        self.id = id
        if resource is not None:
            # These should exist in the application response, but don't, currently.
            #self.href = resource["href"]
            #self.intent = resource["intent"]
            #self.location = resource["location"]
            #self.role = resource["role"]
            pass

    def _get(self) -> requests.Response:
        try:
            rsp = self._svc.get_application(self._instance_id, self.id)
        except ApiException as e:
            if e.code == 404:
                raise ResourceNotFoundError(e.http_response.url, "Application not found.")
            else:
                raise
        return rsp.result

    def _getAsset(self, asset_id: str ) -> requests.Response:
        try:
            rsp = self._svc.get_asset(self._instance_id, self.id, asset_id)
        except ApiException as e:
            if e.code == 404:
                raise ResourceNotFoundError(e.http_response.url, "Asset not found.")
            else:
                raise
        return rsp.result

    def getStatus(self) -> str:
        """Retrieve the status of the DFOApplication.

        An API call to the service is made to get the status, every time.

        When you use the IbmDataFabricOrchestratorV1Dummy service, the application status is reported as ready.
        """

        # Since status could change, we'll just go get it every time somebody asks
        rsp = self._get()
        return rsp["state"] if "state" in rsp else None

    def delete(self):
        """Request that this DFOApplication to be removed.

        When you use the IbmDataFabricOrchestratorV1Dummy service, this call is silently ignored, as nothing is
        removed on the backend.
        """
        self._svc.delete_application(self._instance_id, self.id)

    def getAssetStatus(self, asset_id: str) -> str:
        """Retrieve the status of the specified DataAsset in this DFOApplication.

        An API call to the service is made to get the status, every time.

        Returns None when no status for this DataAsset in the DFOApplication.

        When you use the IbmDataFabricOrchestratorV1Dummy service, all asset statuses are reported as ready.
        """

        # Since status could change, we'll just go get it every time somebody asks
        rsp = self._getAsset(asset_id)
        return rsp["state"] if "state" in rsp else None

    def getAssetErrorMessage(self, asset_id: str) -> str:
        """If the specified DataAsset is in the Error state, the DataAsset retrieve error message from
        the DFOApplication.

        An API call to the service is made to get the error message, every time.

        Return None if there is no error message for this DataAsset in the DFOApplication.

        When using the IbmDataFabricOrchestratorV1Dummy service, no assets have error messages, so None will always
        be returned, for all assets.
        """
        rsp = self._getAsset(asset_id)
        return rsp["message"] if "message" in rsp else None

    def getDataAccessEndpoint(self, asset_id: str) -> str:
        """Retrieve the data access endpoint URI for the specified DataAsset in the DFOApplication.

        An API call is made to the service to get the endpoint, every time.

        Returns None when no endpoint information for this DataAsset in the DFOApplication.

        When you use the IbmDataFabricOrchestratorV1Dummy service, all assets report the direct Flight
        endpoint URL that is specified when the dummy service is constructed.
        """

        rsp = self._getAsset(asset_id)
        return rsp["endpoint"] if "endpoint" in rsp else None

    def getAuthenticatedFlightClient(self, asset_id: str, *, skip_wait_for_available = False, wait_for_available_timeout = None, **kwargs) -> flight.FlightClient:
        """Using the data access endpoint for the specified asset, build a pre-authenticated Apache
        Arrow Flight client, ready for use, and return it.

        By default, waits for the Apache Arrow Flight endpoint to be available. To skip the wait, 
        pass in the skip_wait_for_available option, set to True. To control the wait timeout, 
        pass in the wait_for_available_timeout option, set to an integer number of seconds to wait.

        All other keyword arguments are passed to the FlightClient constructor as options.
        """

        auth = self._svc.get_authenticator()
        endpoint = self.getDataAccessEndpoint(asset_id)
        if endpoint is None:
            raise AssetError("Unable to determine asset endpoint: [%s]" % (self.getAssetErrorMessage(asset_id),))

        client = flight.FlightClient(endpoint, **kwargs)
        auth.validate()

        if not skip_wait_for_available:
            if wait_for_available_timeout is None:
                client.wait_for_available()
            else:
                client.wait_for_available(timeout = wait_for_available_timeout)

        # The python ibm_cloud_sdk_core changed this interface for 3.12, but rather than introduce version
        # parsing, just check to see if its a function (the new way) or else assume its a string (the old way).
        # Also, the nice constants to compare against weren't used initially either, so we have to use the bare
        # strings.
        auth_type = auth.authentication_type() if callable(auth.authentication_type) else auth.authentication_type
        if auth_type == "bearerToken":
            client.authenticate(TokenClientAuthHandler(auth.bearer_token))
        elif (auth_type == "iam" or auth_type == "cp4d"):
            # These use token managers to get the bearer token
            client.authenticate(TokenClientAuthHandler(auth.token_manager.get_token()))
        else:
            # For AUTHTYPE_NOAUTH, we wouldn't try to authenticate anyway (unlikely to work with most flight servers).
            # For AUTHTYPE_BASIC, I'm not sure flight supports that.  If needed, that would have to be figured out.
            #   Don't try to authenticate, which will likely fail when trying to use the flight server.
            # For AUTHTYPE_UNKNOWN, we won't know what to do.  Don't auth, and let the flight server reject us.
            pass

        return client

    def waitForAssetReady(self, asset_id: str, *, timeout=None, interval=0.1):
        """Periodically queries the DFOApplication for the status of the specified DataAsset.

        Returns only when the DataAsset is in the Ready state and can be used.

        If the DataAsset never becomes ready within the timeout period (in seconds), 
        the TimeoutError exception is raised.

        If the DataAsset changes to an Error or Deny state, an AssetError exception 
        is raised with more information.

        Status query frequency can be overridden by using the interval parameter (in seconds, defaults to 0.1 seconds).

        When you use the IbmDataFabricOrchestratorV1Dummy service, returns immediately, as assets 
        are always Ready when you have no IBM Data Fabric Orchestrator backend service.
        """

        start_time = time.monotonic()
        rsp = self._getAsset(asset_id)
        while "state" not in rsp or rsp["state"] != "Ready":
            if "state" in rsp and rsp["state"] != "ADDED":
                raise AssetError(rsp["message"] if "message" in rsp else "Unknown Asset Error")
            if timeout is not None and time.monotonic() - start_time >= timeout:
                raise TimeoutError
            time.sleep(interval)
            rsp  = self._getAsset(asset_id)

    def addAssets(self, assets: List['DataAsset']):
        """Add the specified list of DataAssets to the DFOApplication.

        For more information about DataAsset declaration, see the documentation for DataAsset 
        in ibm_data_fabric_orchestrator_v1.py.

        Returns a List[AssetResource] with state information about each asset that was 
        added (or attempted to be added).

        If the asset doesn't exist or would be denied, that asset is not added to the application, 
        and instead returns with a REJECTED state. Later queries for that state of the asset from 
        this application fails with a ResourceNotFoundError, since it is not in the application.

        Therefore, you must always check the results of the addAssets() call to ensure your assets were added.

        If you add a list of assets to an application, some might add fine, and others might be rejected. 
        You must go through the resulting list to check the state of each individually.

        However, if you use the IbmDataFabricOrchestratorV1Dummy service and no backend IBM Data Fabric
        Orchestrator add-on is running, addAssets() always add each asset, and none are REJECTED, 
        even if later when you try to use Apache Arrow Flight to access the asset, it might fail then, if it doesn't exist.
        """
        rsp = self._svc.add_assets(self._instance_id, self.id, assets).result
        return rsp["assets"] if "assets" in rsp else None

    def removeAssets(self, assets: List['DataAsset']):
        """Remove the specified list of DataAssets from the DFOApplication.

        For more information about DataAsset declaration, see the documentation for DataAsset in ibm_data_fabric_orchestrator_v1.py.
        Only the asset ID needs to match for the asset to be removed.

        When you use the IbmDataFabricOrchestratorV1Dummy service, this call is silently ignored, as nothing on 
        the backend is removed.
        """

        for a in assets:
            self._svc.remove_asset(self._instance_id, self.id, a.asset_id)

    def removeAsset(self, asset_id: str):
        """Remove the specified single DataAsset, defined by its asset_id, from the DFOApplication.

        When you use the IbmDataFabricOrchestratorV1Dummy service, this call is silently ignored, as nothing on 
        the backend is removed.
        """
        self._svc.remove_asset(self._instance_id, self.id, asset_id)

    def reconcileApplication(self):
        """Reconcile data fabric orchestrator application.

        Reconcile data fabric orchestrator application from the specified instance.

        When you use the IbmDataFabricOrchestratorV1Dummy service, this call is silently ignored, as nothing
        on the backend to reconciled.
        """
        self._svc.reconcile_application(self._instance_id, self.id)

    def listActiveAssets(self) -> requests.Response:
        """List active data assets from an application.

        List active data assets from an application.

        However, if you use the IbmDataFabricOrchestratorV1Dummy service and no backend IBM Data Fabric 
        Orchestrator add-on is running, listActiveAssets() return an empty list.
        """
        rsp = self._svc.list_active_assets(self._instance_id, self.id).result
        return rsp["assets"] if "assets" in rsp else None
