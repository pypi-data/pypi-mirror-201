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
The service finder for IBM Data Fabric Orchestrator control plane.

Functions to create an Authenticator and an IbmDataFabricOrchestratorV1 service object.

In IBM Watson™ Studio notebook runtime environments, several environment variables are set:

    The location of the base service URL for the Cloud Pak for Data instance.
    The direct Apache Arrow Flight service URL.
    (Optional) A bearer token to use for authentication.

When these values are available, an Authenticator can be built. To help determine the backend
service endpoints to use, including query to see whether IBM Data Fabric Orchestrator is installed,
and weather on-premises Cloud Pak for Data instance is used. However, parameters passed directly to
get_service() override anything in the environment. For more information about which parameters
override which environment variables, see the Parameters section.

*** Remember ***
If you are running in an on-premises Cloud Pak for Data instance that does not have the IBM Data 
Fabric Orchestrator add-on installed, get_service() returns a dummy shim service IbmDataFabricOrchestratorV1Dummy,
which can be used exactly like the real IbmDataFabricOrchestratorV1 service. But all results that would 
typically use the backend Data Fabric Orchestrator service, are synthesized locally with good results, 
even for assets and contexts that might not exist. The Apache Arrow Flight endpoint that is returned 
is the direct Watson™ Studio notebook Flight endpoint for the Cloud Pak for Data instance that is being 
used. You might get an error first when you try to use the Flight client to query an asset, when the 
asset has problems.

In addition, when you use the dummy service, no data enforcement is done on the governance policies 
because the IBM Data Fabric Orchestrator add-on is not installed. The common client SDK is only used 
for convenience and client code commonality.

If the IBM Data Fabric Orchestrator add-on is installed in the Cloud Pak for Data instance, but is 
shutdown for maintenance or unavailable for some other reason, the normal IbmDataFabricOrchestratorV1 
service remains created and used here, but calls to use it might fail. This scenario avoids bypassing
data governance when a backend problem occurs, where the client would expect data enforcement because
Data Fabric Orchestrator is installed. To troubleshoot the errors returned:

    If the add-on was shutdown intentionally for servicing, you can try again later as the service is temporarily unavailable.
    If you use on-premises Cloud Pak for Data, report to your Cloud Pak for Data administrator
    If you use Cloud Pak for Data as a Service on IBM Cloud, open an IBM Cloud support case.


"""

import os
import sys
import requests
import logging
from .ibm_data_fabric_orchestrator_v1 import IbmDataFabricOrchestratorV1
from .ibm_data_fabric_orchestrator_v1_dummy import IbmDataFabricOrchestratorV1Dummy
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator, BearerTokenAuthenticator, CloudPakForDataAuthenticator, BasicAuthenticator, NoAuthAuthenticator

# Environment variables that may be set in Watson Studio notebook environments
SVC_BASE_URL_ENV_VAR = "RUNTIME_ENV_APSX_URL"
FLIGHT_URL_ENV_VAR = "RUNTIME_FLIGHT_SERVICE_URL"
# These two are only set in on-prem CPD notebooks (that is, not on CPDaaS notebooks on IBM Cloud)
USER_TOKEN_ENV_VAR = "USER_ACCESS_TOKEN"
USER_ID_ENV_VAR = "USER_ID"
ADDON_API_PATH = "/zen-data/v1/addOn/query"
CP4D_AUTH_API_PATH = "/icp4d-api"

logger = logging.getLogger(__name__)

def get_service(*,
                authenticator = None,
                token = None,
                apikey = None,
                user = None,
                password = None,
                auth_url = None,
                svc_base_url = None,
                svc_url = None,
                addon_url = None,
                flight_url = None,
                service_disable_ssl_verification = False,
                auth_disable_ssl_verification = False,
                addon_disable_ssl_verification = False):
    """Examine the environment and build an appropriate ibm_data_fabric_orchestrator service object.

    Authentication-related keyword arguments:
        authenticator: A pre-built authenticator object for use by the service, and a get_service() to query
                       the add-on service. If specified, the other authentication-related parameters are ignored.
        token:         A pre-generated bearer token that is used with a BearerTokenAuthenticator and added to each request.
                       If the token is not specified, but a USER_ACCESS_TOKEN is specified in the environment, that value is used.
                       Setting to an empty string forces no token to be used, even when a token is specified in the environment.
        apikey:        Either an IAM or Cloud Pak for Data API key is used to authenticate with an IAMAuthenticator or CloudPakForDataAuthenticator.
        user:          A username used to authenticate with a CloudPakForDataAuthenticator or BasicAuthenticator.
        password:      The password used to authenticate with a CloudPakForDataAuthenticator or BasicAuthenticator.
        auth_url:      The IAM or Cloud Pak for Data authorization endpoint URL to use when authenticating with an IAMAuthenticator or
                       CloudPakForDataAuthenticator. If an auth_url is not specified, you can generate the URL by the svc_base_url. You can specify the URL with 
                       the RUNTIME_ENV_APSX_URL environment variable. Or the URL defaults to the IBM Cloud IAM service.
        auth_disable_ssl_verification:  Disables SSL verification when you communicate with an IAM or CP4D authentication service.

    Other Keyword Arguments:
        svc_base_url:  The base URL to determine service endpoints, such as data fabric orchestrator, authentication, add-on, or Apache Arrow Flight.
                       If the svc_base url is not specified, the RUNTIME_ENV_APSX_URL environment variable is used.  If the URL cannot be determined,
                       other service endpoints use their defaults.
        svc_url:       Specify the data fabric orchestrator service endpoint URL.  If the svc_url is not specified, uses the svc_base_url or
                       RUNTIME_ENV_APSX_URL in the environment, or uses the IBM Data Fabric Orchestrator service default for IBM Cloud.
        service_disable_ssl_verification:  Disables SSL verification when you communicate with the ibm_data_fabric_orchestrator service.
        addon_url:     Specify the add-on endpoint URL to determine whether IBM Data Fabric Orchestrator is installed and enabled in a Cloud Pak for Data instance.
                       If the addon_url is not specified, you can generate the URL by svc_base_url or RUNTIME_ENV_APSX_URL in the environment.
        addon_disable_ssl_verification:  Disables SSL verification when you communicate with the add-on service.
        flight_url:    Specify the Apache Arrow Flight endpoint URL used for all Flight requests when IBM Data Fabric Orchestrator is not installed by using the "dummy"
                       ibm_data_fabric_orchestrator service.  If the flight_url is not specified, the RUNTIME_FLIGHT_SERVICE_URL environment
                       variable value is used.  The Flight URL is only used if IBM Data Fabric Orchestrator add-on is not installed in the
                       Cloud Pak for Data instance, as a result an IbmDataFabricOrchestratorV1Dummy service is created.

    Returns either an IbmDataFabricOrchestratorV1 or IbmDataFabricOrchestratorV1Dummy service, both of which can be used with the extended_api functions
    equivalently.


    """
    # Interpret overrides and environment to set local variables to initial attempts

    # Bearer token can be overriden on the call, or grabbed from the environment, if set there.  Passing in an empty string causes the environment to be ignored as well.
    use_token = None
    if token is not None:
        use_token = token
    elif USER_TOKEN_ENV_VAR in os.environ:
        use_token = os.environ[USER_TOKEN_ENV_VAR]
    if use_token == "":
        use_token = None
    logger.info("Determined potential bearer token to use [%s].", "xxxx" if use_token is not None else None)

    # Base service URL can be overriden on the call, or grabbed from the environment, if set there.  Passing in an empty string causes the environment to be ignored as well.
    use_svc_base_url = None
    if svc_base_url is not None:
        use_svc_base_url = svc_base_url
    elif SVC_BASE_URL_ENV_VAR in os.environ:
        use_svc_base_url = os.environ[SVC_BASE_URL_ENV_VAR]
    if use_svc_base_url == "":
        use_svc_base_url = None
    # If no base service url is specified, we're going to have to assume public cloud, but we'll let the service default pick the service endpoint, we don't need an addon
    # endpoint or a flight endpoint, and the auth url will default to the standard IBM Public Cloud IAM endpoint, below.
    logger.info("Determined potential service base URL [%s].", use_svc_base_url)

    use_svc_url = None
    if svc_url is not None:
        use_svc_url = svc_url
    elif use_svc_base_url is not None:
        use_svc_url = use_svc_base_url
    if use_svc_url == "":
        use_svc_url = None
    # If we can't come up with the service url from the options given, we'll have to assume public cloud, but we'll let the service default pick the service endpoint.
    logger.info("Determined potential IBM Data Fabric Orchestrator service URL [%s].", use_svc_url)

    # Flight url can be overriden on the call or grabbed from the environment, if set there.  Passing in an empty string causes the environment to be ignored as well.
    use_flight_url = None
    if flight_url is not None:
        use_flight_url = flight_url
    elif FLIGHT_URL_ENV_VAR in os.environ:
        use_flight_url = os.environ[FLIGHT_URL_ENV_VAR]
    if use_flight_url == "":
        use_flight_url = None
    # If we can't come up with the flight endpoint from the options given, we'd have to assume public cloud,
    # but in that case, we don't need a flight url at all here, since we'll always be using a real DFO service.
    # If we can't come up with a flight_url but are actually using CPD (and svc_base_url could be determined), and DFO is installed/enabled,
    # we'll be fine, since we'll be using the real service.  If DFO is not installed/enabled, we'll run in to a problem when constructing the
    # dummy service.
    logger.info("Determined potential Apache Arrow Flight service URL [%s].", use_flight_url)

    # Addon url can be overriden on the call or computed from the svc_base_url
    use_addon_url = None
    if addon_url is not None:
        use_addon_url = addon_url
    elif use_svc_base_url is not None:
        use_addon_url = use_svc_base_url + ADDON_API_PATH
    # If we can't come up with an addon_url from the options given, we have to assume public cloud,
    # in which case we don't need the addon service anyway, which doesn't exist in public cloud.
    logger.info("Determined potential add-on service URL [%s].", use_addon_url)

    # Auth url can be overriden on the call, or computed from the service base url, if we know that.  Sensible defaults can be computed if we're on the cloud or if we know we're using CPD authentication and have a good base service url.
    use_auth_url = None
    if auth_url is not None:
        use_auth_url = auth_url
    elif use_svc_base_url is not None:
        if use_svc_base_url.endswith(".dev.cloud.ibm.com"):
            use_auth_url = "https://iam.test.cloud.ibm.com"
        elif use_svc_base_url.endswith(".cloud.ibm.com"):
            use_auth_url = "https://iam.cloud.ibm.com"
        elif use_svc_base_url.endswith(".appdomain.cloud"):
            use_auth_url = "https://iam.cloud.ibm.com"
        elif user is not None:
            # Presumably a CP4D authenticator?
            use_auth_url = use_svc_base_url + CP4D_AUTH_API_PATH
        elif apikey is not None:
            # Presumably it's an IAM authenticator directly?
            use_auth_url = use_svc_base_url
        else:
            # No idea what kind of authenticator we have here.  We don't have a user or apikey, so we won't be able to authenticate, if it comes down to that.
            # We might have a bearer token, or a pre-created authenticator, so don't abort just yet.
            use_auth_url = None
    else:
        # If no service base url could be computed, we're going to let the service default pick the service endpoint, but for the authenticator, we can assume public cloud (if we need to build our own authenticator).
        use_auth_url = "https://iam.cloud.ibm.com"
    logger.info("Determined potential authentication service URL [%s].", use_auth_url)

    # Figure out if we're on a CPDaaS instance by looking at the service base url (if we were given one) or we just assume CPDaaS if we don't know our service url.
    # In the future, there may be CPDaaS instances on other clouds, so we'd probably need a better way to determine this.
    is_cpdaas = None
    if use_svc_base_url is None:
        is_cpdaas = True
        logger.info("Assuming Cloud Pak for Data as a Service with default service base URL.")
    elif use_svc_base_url.endswith(".cloud.ibm.com"):
        is_cpdaas = True
        logger.info("Assuming Cloud Pak for Data as a Service with IBM Cloud URL.")
    elif use_svc_base_url.endswith(".appdomain.cloud"):
        is_cpdaas = True
        logger.info("Assuming Cloud Pak for Data as a Service with IBM Cloud appdomain URL.")
    else:
        # Assume everything else is on-prem CPD
        is_cpdaas = False
        logger.info("Assuming on-premises Cloud Pak for Data instance.")

    # Figure out if we need to build an authenticator
    # Calling with authenticator already set bypasses a lot of heuristics...
    auth = authenticator
    if auth is None:
        # Need to build an authenticator of some kind.
        if use_token is not None:
            # If we have a token, use it. This is the easiest way to go.
            logger.info("Building a BearerTokenAuthenticator with the specified token.")
            auth = BearerTokenAuthenticator(bearer_token = use_token)
        elif use_auth_url is not None:
            if use_auth_url.endswith(".cloud.ibm.com") and apikey is not None:
                # Assume if we're authorizing to the public cloud, and apikey is set, we should be able to do IAM.
                logger.info("Building an IAMAuthenticator for the IBM Cloud with an API key.")
                auth = IAMAuthenticator(apikey = apikey, url = use_auth_url, disable_ssl_verification = auth_disable_ssl_verification)
            elif use_auth_url.endswith(CP4D_AUTH_API_PATH) and user is not None:
                # If internally connecting to a icp4d-api auth service directly, and we do have a username, assume its some form of CP4D authenticator.
                # If we don't have a password or apikey, this will fail.
                logger.info("Building a CloudPakForDataAuthenticator for a standard Cloud Pak for Data authentication endpoint with a username.")
                auth = CloudPakForDataAuthenticator(username = user, password = password, url = use_auth_url, apikey = apikey, disable_ssl_verification = auth_disable_ssl_verification)
            elif apikey is not None:
                # If we have an apikey, even if its not on the public cloud, it may be an IAM authenticator after all.
                logger.info("Building an IAMAuthenticator with an API key.")
                auth = IAMAuthenticator(apikey = apikey, url = use_auth_url, disable_ssl_verification = auth_disable_ssl_verification)
            elif user is not None:
                # Otherwise, if we do have a user set, assume some sort of CP4D authenticator?
                # If we don't have a password or apikey, this will fail.
                logger.info("Building a CloudPakForDataAuthenticator with a username.")
                auth = CloudPakForDataAuthenticator(username = user, password = password, url = use_auth_url, apikey = apikey, disable_ssl_verification = auth_disable_ssl_verification)
            else:
                # No apikey or user, so IAM and CPD won't work at all.  Go with a NoAuthAuthenticator.  That will let us get through and create the service, though if something actually needs to use it,
                # we won't really be able to do much.
                logger.info("NoAuthAuthenticator is set. An authentication URL was specified, but missing details.")
                auth = NoAuthAuthenticator()
        elif user is not None and password is not None:
            # Otherwise, we might not be able to authenticate.  If we have a username and password, maybe BasicAuthenticator will work ...
            logger.info("Building a BasicAuthenticator with specified username and password as no authentication URL was specified.")
            auth = BasicAuthenticator(username = user, passsword = password)
        else:
            # I guess we have to go with the NoAuthAuthenticator here.  Likely won't work for real use of the service, but will let us get through construction.
            logger.info("NoAuthAuthenticator is set as no authentication URL was specified and missing details.")
            auth = NoAuthAuthenticator()
    else:
        logger.info("Using a previously created authenticator.")

    # Figure out if DFO should be available, and build a service to match, either the real V1 DFO service (if DFO should be available) or a dummy V1 DFO service that passes through
    # to flight, if DFO isn't really available.
    svc = None
    if is_cpdaas:
        # For public cloud cpdaas instances, DFO should always be around, so just build the normal V1 service.
        logger.info("Building an IbmDataFabricOrchestratorV1 service, on a Cloud Pak for Data as a Service instance, where IBM Data Fabric Orchestrator is installed and enabled. Using IBM Data Fabric Orchestrator service URL [%s]", use_svc_url)
        svc = IbmDataFabricOrchestratorV1(authenticator = auth)

        # set the SSL verification disablement correctly
        svc.set_disable_ssl_verification(service_disable_ssl_verification)

        # set the service url correctly, if we need to override from the default
        if use_svc_url is not None:
            svc.set_service_url(use_svc_url)

    else:
        # Must be a CPD onprem instance.  Need to call off to the addon api to determine if DFO is installed.
        # If its installed, but disabled (shutdown), we'll still want to use the normal DFO V1 service, since the shutdown is probably due to maintenance,
        # and we'll just want the client's use to fail until the service is back up, rather than just bypass DFO.
        # If we decide this isn't right, it should be easy to change here. (other options would be: (1) raise an exception right here to alert the user the service is currently shutdown, or (2) silently bypass directly to flight, so things at least work to get data.)
        logger.info("Calling the add-on service on an on-premises Cloud Pak for Data instance to determine whether IBM Data Fabric Orchestrator is installed and enabled.")
        request = {
            "method": "POST",
            "url": use_addon_url,
            "params": {"show_all": "true"},
            "headers": {"Content-Type": "application/json"},
            "json": {
                "type": "dfo",
                "add_on_type": "component"
            }
            }

        if addon_disable_ssl_verification:
            request["verify"] = False

        logger.info("Using the authenticator to authenticate your add-on request.")
        auth.authenticate(request)

        logger.info("Querying the add-on service [%s] for information about the IBM Data Fabric Orchestrator component.", use_addon_url)
        rsp = requests.request(**request)
        logger.info("Add-on service response: %d %s", rsp.status_code, rsp.reason)
        if rsp.status_code == requests.codes.ok:
            rsp_dict = rsp.json()
            if "requestObj" in rsp_dict and rsp_dict["requestObj"] is not None:
                for x in rsp_dict["requestObj"]:
                    if x["Type"] == "dfo":
                        logger.info("State of IBM Data Fabric Orchestrator component: [%s]", x["State"])
                        if x["State"] == "enabled" or x["State"] == "shutdown":
                            # Ok, great, dfo is installed at least.  Use the full normal V1 service.
                            # If dfo is shutdown, later requests won't work (until the component is started again),
                            # but we shouldn't bypass DFO in this case.
                            logger.info("Building an IbmDataFabricOrchestratorV1 service as the IBM Data Fabric Orchestrator is installed in this Cloud Pak for Data instance. Using IBM Data Fabric Orchestrator service URL [%s]", use_svc_url)
                            svc = IbmDataFabricOrchestratorV1(authenticator = auth)

                            # set the SSL verification disablement correctly
                            svc.set_disable_ssl_verification(service_disable_ssl_verification)

                            # set the service url correctly
                            # Note that in this case, use_svc_base_url better be set to something,
                            # since we are clearly not on public cloud, which would be the default.
                            svc.set_service_url(use_svc_url)
                            break
                        else:
                            # DFO came back in the results, but must be disabled?
                            break

            # Check if we already created the DFO service, implying it was found, and installed, and either enabled or shutdown.
            # If not, we'll create the dummy service.
            if svc is None:
                # DFO not installed
                # Create the Dummy service to go directly to flight.
                # This may fail if we weren't able to come up with a flight url.
                logger.info("Building an IbmDataFabricOrchestratorV1Dummy service as the IBM Data Fabric Orchestrator is not installed in this Cloud Pak for Data instance. Using the Apache Arrow Flight URL [%s]", use_flight_url)
                svc = IbmDataFabricOrchestratorV1Dummy(authenticator = auth, flight_url = use_flight_url)
        else:
            # Some problem contacting the addon service? Not sure of the safe thing to do here, other than abort.
            logger.error("Unexpected problem with the add-on service.")
            rsp.raise_for_status()

    # Return whatever we created for a service
    return svc
