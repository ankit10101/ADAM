from crew import WebAnalyticsAutomationCrew
from datetime import datetime

# use for local testing
import argparse
import json

# ---------- Agentcore imports --------------------
from bedrock_agentcore.runtime import BedrockAgentCoreApp

app = BedrockAgentCoreApp()
# ------------------------------------------------


@app.entrypoint
def agent_invocation(payload):
    """Handler for agent invocation"""
    print(f"Payload: {payload}")
    try:
        # Extract user message from payload with default
        user_message = payload.get("prompt", "Artificial Intelligence in Healthcare")
        print(f"Processing topic: {user_message}")

        # Use synchronous kickoff instead of async - this avoids all event loop issues
        result = (
            WebAnalyticsAutomationCrew()
            .crew()
            .kickoff(
                inputs={
                    "user_query": user_message,
                    "current_date": datetime.now().strftime(r"%d/%m/%Y"),
                }
            )
        )

        print("Result Raw:\n*******\n", result.raw)

        # Safely access json_dict if it exists
        if hasattr(result, "json_dict"):
            print("Result JSON:\n*******\n", result.json_dict)

        return {"result": result.raw}

    except Exception as e:
        print(f"Exception occurred: {e}")
        return {"error": f"An error occurred: {str(e)}"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("payload", type=str)
    args = parser.parse_args()
    response = agent_invocation(json.loads(args.payload))
    print(response)
    
# "{\"prompt\":\"Hello!\"}"
