from typing import Optional
from googleapiclient.discovery import build
from src.adam.utility_functions import get_gcp_service_account_credentials
from crewai.tools import tool


@tool
def create_a_gtm_ga4_event_tag(
    account_id: str,
    container_id: str,
    workspace_id: str,
    name: str,
    ga4_event_name: str,
    ga4_event_parameters: list[dict[str, str]],
    ga4_measurement_id: str,
    trigger_ids: Optional[list[str]] = None,
    notes: Optional[str] = None,
) -> str:
    """
    Use this tool to create/add a new "GA4 Event Tag" in a GTM (Google Tag Manager) configuration (account/container/workspace). It will help you create a GTM tag that sends specific events to a GA4 property.

    Note that this tool is only for the GA4 Event Tags. It can't create other GTM tags (Google Ads, Google Tag, etc.)

    It takes in the following parameters:
    * account_id (str): The Google Tag Manager account ID to create the tag in
    * container_id (str): The Google Tag Manager container ID to create the tag in
    * workspace_id (str): The Google Tag Manager workspace ID to create the tag in
    * name (str): The name of the tag
    * ga4_event_name (str): The event name to send/pass to GA4
    * ga4_event_parameters (list[dict[str, str]]): A list of Python dictionaries of size one. Each dictionary represents an event parameter to capture along with the GA4 event. The keys represent the parameter name, and the values represent the parameter value.
    * ga4_measurement_id (str): The GA4 Measurement ID to send the event data to
    * The following parameters are optional:
        * trigger_ids ([list[str]]): It represents a list of the various existing GTM triggers that decide the tag firing conditions. The default value here is None
        * notes (str): Any user-specific notes for the tag

    It returns a string specifying whether the tool ran successfully or encountered an exception. You should stop in either scenario and respond accordingly.
    """
    service = build(
        "tagmanager",
        "v2",
        credentials=get_gcp_service_account_credentials(
            "../ga4-apis-practice@ga4-apis-practice.json",
            ["https://www.googleapis.com/auth/tagmanager.edit.containers"],
        ),
    )
    request = (
        service.accounts()
        .containers()
        .workspaces()
        .tags()
        .create(
            parent=f"accounts/{account_id}/containers/{container_id}/workspaces/{workspace_id}",
            body={
                "accountId": account_id,
                "containerId": container_id,
                "workspaceId": workspace_id,
                "name": name,
                "type": "gaawe",
                "parameter": [
                    {"type": "boolean", "key": "sendEcommerceData", "value": "false"},
                    {"type": "boolean", "key": "enhancedUserId", "value": "false"},
                    {
                        "type": "list",
                        "key": "eventSettingsTable",
                        "list": [
                            {
                                "type": "map",
                                "map": [
                                    {
                                        "type": "template",
                                        "key": "parameter",
                                        "value": list(parameter.keys())[0],
                                    },
                                    {
                                        "type": "template",
                                        "key": "parameterValue",
                                        "value": list(parameter.values())[0],
                                    },
                                ],
                            }
                            for parameter in ga4_event_parameters
                        ],
                    },
                    {"type": "template", "key": "eventName", "value": ga4_event_name},
                    {
                        "type": "template",
                        "key": "measurementIdOverride",
                        "value": ga4_measurement_id,
                    },
                ],
                "firingTriggerId": trigger_ids,
                "tagFiringOption": "oncePerEvent",
                "monitoringMetadata": {"type": "map"},
                "consentSettings": {"consentStatus": "notSet"},
                "notes": notes,
            },
        )
    )

    try:
        response = request.execute()
        return f"Congratulations! The GA4 Event Tag creation was successful.\n\nStop here and confirm successful task completion."
    except Exception as e:
        return f"An exception occurred while using the tool!\nHere it is. {e}\n\nStop here and respond with the exception summary."
