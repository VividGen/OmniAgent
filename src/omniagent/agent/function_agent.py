import asyncio

from langchain.agents import (
    AgentExecutor,
    AgentType,
    create_tool_calling_agent,
    initialize_agent,
)
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from langchain_openai import ChatOpenAI
from toolz import memoize

from omniagent.agent.cache import init_cache
from omniagent.agent.system_prompt import (
    SYSTEM_PROMPT,
    SYSTEM_PROMPT_V2,
    custom_agent_kwargs,
)
from omniagent.conf.env import settings
from omniagent.experts.article_expert import ArticleExpert
from omniagent.experts.feed_expert import FeedExpert
from omniagent.experts.nft_expert import NFTExpert
from omniagent.experts.price_expert import PriceExpert
from omniagent.experts.search_expert import SearchExpert
from omniagent.experts.swap_expert import SwapExpert
from omniagent.experts.transfer_expert import TransferExpert

# Initialize cache
init_cache()


# Function to create a ReAct agent
def create_react_agent(session_id: str):
    # Define agent kwargs
    agent_kwargs = (
        {
            "system_message": SystemMessage(content=SYSTEM_PROMPT),
            "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
        }
        if settings.MODEL_NAME.startswith("gpt")
        else custom_agent_kwargs
    )

    # List of experts to be loaded
    experts = [
        SearchExpert(),
        FeedExpert(),
        PriceExpert(),
        ArticleExpert(),
        NFTExpert(),
        TransferExpert(),
        SwapExpert(),
    ]

    # Initialize interpreter
    interpreter = create_interpreter(settings.MODEL_NAME)

    # Initialize and return the agent
    return initialize_agent(
        experts,
        interpreter,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        agent_kwargs=agent_kwargs,
        handle_parsing_errors=True,
    )


# Function to create an interpreter based on model name
def create_interpreter(model_name):
    if model_name.startswith("gpt"):
        return ChatOpenAI(
            model=model_name,
            temperature=0.3,
            streaming=True,
        )
    elif model_name.startswith("gemini"):
        if settings.GOOGLE_GEMINI_API_KEY is not None:
            return ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=settings.GOOGLE_GEMINI_API_KEY,
                temperature=0.3,
                streaming=True,
            )
        else:
            return ChatVertexAI(
                model=settings.MODEL_NAME,
                project=settings.GOOGLE_CLOUD_PROJECT_ID,
                temperature=0.3,
                streaming=True,
                verbose=True,
            )
    else:
        return ChatOllama(
            model=model_name,
            base_url=settings.LLM_API_BASE,
        )


@memoize
def get_agent(session_id: str) -> AgentExecutor:
    if settings.MODEL_NAME.startswith("gemini") or settings.MODEL_NAME.startswith("gpt"):
        return create_tool_call_agent(session_id)
    return create_react_agent(session_id)


# Function to create a tool calling agent
def create_tool_call_agent(session_id: str):
    # Initialize language model
    interpreter = create_interpreter(settings.MODEL_NAME)

    # Define prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                SYSTEM_PROMPT_V2,
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    # List of experts
    experts = [
        SearchExpert(),
        FeedExpert(),
        PriceExpert(),
        ArticleExpert(),
        NFTExpert(),
        TransferExpert(),
        SwapExpert(),
    ]

    # Construct the Tools agent
    agent = create_tool_calling_agent(interpreter, experts, prompt)

    # Create an agent executor by passing in the agent and tools
    agent_executor = AgentExecutor(agent=agent, tools=experts, verbose=True)
    return agent_executor


# Function to get the chat history of a session from Postgres


async def main():
    # Create a tool call agent and use it to handle some inputs
    agent = get_agent("123")
    await agent.ainvoke({"input": "Swap 1 eth to usdt, from ethereum to arb"})
    await agent.ainvoke({"input": "What is the price of ETH?"})
    await agent.ainvoke({"input": "What did vitalik.eth do recently?"})


if __name__ == "__main__":
    asyncio.run(main())
