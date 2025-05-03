# Docs: https://python.langchain.com/v0.1/docs/modules/tools/custom_tools/

# Import necessary libraries
import os
from typing import Type

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()
print("API KEY:", os.getenv("TAVILY_API_KEY"))

# Pydantic models for tool arguments


class SimpleSearchInput(BaseModel):
    query: str = Field(description="should be a search query")


class MultiplyNumbersArgs(BaseModel):
    x: float = Field(description="First number to multiply")
    y: float = Field(description="Second number to multiply")


# Custom tool with only custom input


class SimpleSearchTool(BaseTool):
    name: str = "simple_search"
    description: str = (
        "useful for when you need to answer questions about current events"
    )
    args_schema: Type[BaseModel] = SimpleSearchInput  # type: ignore

    def _run(
        self,
        query: str,
    ) -> str:
        """Use the tool."""
        from tavily import TavilyClient

        api_key = os.getenv("TAVILY_API_KEY")
        client = TavilyClient(api_key=api_key)
        results = client.search(query=query)
        return f"Search results for: {query}\n\n\n{results}\n"


# Custom tool with custom input and output
class MultiplyNumbersTool(BaseTool):
    name: str = "multiply_numbers"
    description: str = "useful for multiplying two numbers"
    args_schema: Type[BaseModel] = MultiplyNumbersArgs  # type: ignore

    def _run(
        self,
        x: float,
        y: float,
    ) -> str:
        """Use the tool."""
        result = x * y
        return f"The product of {x} and {y} is {result}"


# Create tools using the Pydantic subclass approach
tools = [
    SimpleSearchTool(),  # type: ignore
    MultiplyNumbersTool(),  # type: ignore
]

# Initialize a ChatGoogleGenerativeAI model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Pull the prompt template from the hub
prompt = hub.pull("hwchase17/openai-tools-agent")

# Create the ReAct agent using the create_tool_calling_agent function
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

# Create the agent executor
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
)

# Test the agent with sample queries
response = agent_executor.invoke({"input": "Search for Apple Intelligence"})
print("Response for 'Search for LangChain updates':", response)

response = agent_executor.invoke({"input": "Multiply 10 and 20"})
print("Response for 'Multiply 10 and 20':", response)
