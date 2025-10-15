# To test the Bedrock AgentCore invocation, run this script separately.

import boto3
import json

client = boto3.client("bedrock-agentcore", region_name="ap-south-1")
payload = json.dumps(
    {
        "prompt": """Target URL: https://keeratsachdeva.github.io/My-Dummy-Website/
                     Requested Action: Execute 'return digitalData' after 5 seconds
                  """
    }
)

response = client.invoke_agent_runtime(
    agentRuntimeArn="arn:aws:bedrock-agentcore:ap-south-1:501931553097:runtime/hosted_agent_mb5wa-JU4BeUCksB",
    runtimeSessionId="dfmeoagmreaklgmrkleafremoigrmtesogmtrskhmtkrlshmt",  # Must be 33+ chars
    payload=payload,
    qualifier="DEFAULT",  # Optional
)
response_body = response["response"].read()
response_data = json.loads(response_body)
print("Agent Response:", response_data)
