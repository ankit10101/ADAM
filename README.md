# ADAM (AI-Driven Analytics Manager)

ADAM is an AI-powered digital analytics automation tool designed to streamline the entire web analytics lifecycle. It leverages AWS Bedrock AgentCore, Google Analytics 4 (GA4), Google Tag Manager (GTM), and Selenium to automate tasks such as data collection, tagging, and reporting.

## Technology Stack

- **Programming Language**: Python 3.12
- **Frameworks and Libraries**:
  - [Streamlit](https://streamlit.io/) for the user interface
  - [Selenium](https://www.selenium.dev/) for browser automation
  - [Google Analytics Data API](https://developers.google.com/analytics/devguides/reporting/data/v1) for GA4 reporting
  - [Google Tag Manager API](https://developers.google.com/tag-platform/tag-manager) for GTM integration
  - [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) for AWS service integration
  - [CrewAI](https://github.com/crew-ai/crewai) for task orchestration
  - [Pandas](https://pandas.pydata.org/) for data manipulation
- **Cloud Services**:
  - AWS Bedrock AgentCore for AI model hosting and runtime
  - AWS ECR for container storage

## Project Architecture

The project is structured around modular components for analytics automation. Key components include:
- **Agent**: The `adam` agent, defined in [`src/adam/crew.py`](src/adam/crew.py), orchestrates tasks using tools and an LLM.
- **Tools**: A set of tools for specific tasks, such as running JavaScript on web pages, fetching network requests, and creating GA4 event tags.
- **Streamlit Application**: A user-friendly interface for interacting with ADAM, located in [`streamlit-application/app.py`](streamlit-application/app.py).

### Architecture Diagram

![ADAM Architecture Diagram](ADAM-Architecture%20Diagram.jpg)

## Getting Started

### Prerequisites

- Python 3.12
- Docker
- AWS CLI configured with appropriate permissions

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd adam
   ```

2. Install dependencies using `pyproject.toml`:
   ```bash
   pip install uv
   uv install
   ```

3. Set up environment variables:
   - Create a `.env` file with necessary credentials and configurations.

4. Run the Streamlit application:
   ```bash
   streamlit run streamlit-application/app.py
   ```

### Docker Setup

1. Build the Docker image:
   ```bash
   docker build -t adam .
   ```

2. Run the container:
   ```bash
   docker run -p 8080:8080 adam
   ```

## Project Structure

```
.
├── src/
│   ├── adam/
│   │   ├── tools/                # Tools for analytics automation
│   │   ├── config/               # Configuration files for agents and tasks
│   │   ├── local_testing/        # Scripts for local testing
│   │   ├── [`src/adam/crew.py`](src/adam/crew.py )               # Main agent and crew definition
│   │   ├── [`src/adam/utility_functions.py`](src/adam/utility_functions.py )  # Helper functions
├── streamlit-application/
│   ├── [`streamlit-application/app.py`](streamlit-application/app.py )                    # Streamlit application
│   ├── .streamlit/               # Streamlit configuration
├── .github/                      # GitHub-specific files
├── Dockerfile                    # Docker configuration
├── [`pyproject.toml`](pyproject.toml )                # Project metadata and dependencies
```

## Key Features

- **Chat Interface**: A conversational interface for user queries.
- **Automation Tools**:
  - Execute JavaScript on web pages.
  - Fetch network requests.
  - Create GA4 event tags.
  - Generate GA4 reports.
- **AWS Integration**: Uses AWS Bedrock AgentCore for AI-powered responses.

## Development Workflow

- **Branching Strategy**: Follow GitFlow for feature development.
- **Testing**: Use local testing scripts in `src/adam/local_testing/` to validate tools and agent behavior.

## Coding Standards

- Follow PEP 8 for Python code.
- Use type hints for function signatures.
- Modularize code for reusability and readability.

## Testing

- Local testing scripts are available in `src/adam/local_testing/`.
- Use `pytest` for unit tests (not included in the current setup).

## Contributing

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit changes and push to your fork.
4. Create a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.