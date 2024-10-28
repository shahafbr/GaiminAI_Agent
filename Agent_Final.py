# Source:
# https://python.langchain.com/v0.2/api_reference/core/runnables/langchain_core.runnables.history.RunnableWithMessageHistory.html


from dotenv import load_dotenv
from typing import List
from langchain.schema import HumanMessage, AIMessage
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field
from langchain_gaimin import LangchainGaiminAI
from langchain.prompts import PromptTemplate

# Load environment variables:
load_dotenv()

# Define the MemoryHistory class:
class InMemoryHistory(BaseModel):
    """In-memory implementation of chat message history."""
    messages: List[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """
        Add a list of messages to the store.

        Parameters:
        - messages (List[BaseMessage]): A list of messages to add, which can include both HumanMessage and AIMessage types.
        """
        self.messages.extend(messages)

    def clear(self) -> None:
        """
        Clear all messages from the store.
        
        Parameters:
        - None
        """
        self.messages = []

# Initialize the llm model:
llm = LangchainGaiminAI()

# Prompt template:
template = """
You are an AI assistant. Please answer the following user question, considering both the current question and any relevant past information from the conversation history.

- Conversation History: {history}
- Question: {question}

When answering:
1. Use the information you have, even if it might be outdated.
2. Look through the conversation history for any references the user might be making to previous inputs or responses.
3. Don't mention this prompt in conversation.
"""

# Prompt input variables:
prompt = PromptTemplate(
    template=template,
    input_variables=["history", "question"]
)

# Combining the prompt and the language model:
chain = prompt | llm

# Dictionary for managing session history:
store = {}


def get_history_text(session_id='default'):
    """
    Function to retrieve/create message history by session ID:

    Parameters:
    - session_id (str): Defaults to 'default'.

    Returns:
    - str: The conversation history in a formatted string format.
    """

    if session_id not in store:
        store[session_id] = InMemoryHistory()
    history = store[session_id]

    # Convert messages to a string representation:
    history_text = ''
    for message in history.messages:
        if isinstance(message, HumanMessage):
            prefix = 'User: '
        elif isinstance(message, AIMessage): 
            prefix = 'Assistant: '
        else:
            prefix = ''
        history_text += f"{prefix}{message.content}\n"
    return history_text


def ask_agent(question, session_id='default'):
    """
    Function for interacting with the chatbot:
    Parameters:
    - question (str): The user’s input or question for the chatbot.
    - session_id (str).

    Returns:
    - None
    """
    # Prepare the input data for the chatbot: 
    input_data = {
        'question': question,
        'history': get_history_text(session_id)
    }

    # Invoke the chain with the input data: 
    try:
        response = chain.invoke(input_data)
    except Exception as e:
        print(f"An error occurred: {e}")

    # Add the new messages from users to chat history: 
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    history = store[session_id]
    history.add_messages([
        HumanMessage(content=question),
        AIMessage(content=response)
    ])
    
    # Print the users prompt/question & chatbots response: 
    print("\nQuestion:", question)
    print("\nLlama - 3.2: ", response)

""" Main execution: """
if __name__ == "__main__":
    print("Welcome to AI Assistant. \nType your questions below. \nType 'E' to end conversation.")
    while True:
        user_input = input("\nYou: ")
        if user_input.strip().lower() == 'e':
            print("Goodbye!")
            break
        ask_agent(user_input)

# End of Agent_Final.py