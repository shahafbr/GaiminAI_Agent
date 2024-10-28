# GaiminAI_Agent:
## Setup:

1. **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Environment Variables**:
    - Create a `.env` file with your API key and model settings:
      ```plaintext
      API_KEY=your_api_key
      MODEL_NAME=your_model_name
      ```

## Usage

- Run the chatbot:
```bash
python Agent_Final.py
```
- Type your questions to chat with the assistant.
- Enter E to end the conversation.

## File Overview:
- Agent_Final.py: Main script to run the chatbot.
- .env: Stores environment variables.

## Requirements:
- langchain
- pydantic
- python-dotenv
- langchain-gaimin
```bash
pip install -r requirements.txt
```
