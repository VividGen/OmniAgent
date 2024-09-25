import operator
from typing import Annotated, Sequence, TypedDict

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, StateGraph
from loguru import logger

from omniagent.agents.asset_management import build_asset_management_agent
from omniagent.agents.block_explore import build_block_explorer_agent
from omniagent.agents.fallback import build_fallback_agent
from omniagent.agents.feed_explore import build_feed_explorer_agent
from omniagent.agents.research_analyst import build_research_analyst_agent


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str


def create_node(agent, name):
    async def run(state):
        logger.info(f"Running {name} agent")
        result = await agent.ainvoke(state)
        return {"messages": [HumanMessage(content=result["output"], name=name)]}

    return run


def build_workflow(llm: BaseChatModel):
    from omniagent.agents.market_analysis import build_market_analysis_agent
    from omniagent.workflows.member import members
    from omniagent.workflows.supervisor_chain import build_supervisor_chain

    market_analysis_agent_node = create_node(build_market_analysis_agent(llm), "market_analysis_agent")
    asset_management_agent_node = create_node(build_asset_management_agent(llm), "asset_management_agent")
    block_explorer_agent_node = create_node(build_block_explorer_agent(llm), "block_explorer_agent")
    research_analyst_agent_node = create_node(build_research_analyst_agent(llm), "research_analyst_agent")
    feed_explorer_agent_node = create_node(build_feed_explorer_agent(llm), "feed_explorer_agent")

    workflow = StateGraph(AgentState)
    workflow.add_node("market_analysis_agent", market_analysis_agent_node)
    workflow.add_node("asset_management_agent", asset_management_agent_node)
    workflow.add_node("block_explorer_agent", block_explorer_agent_node)
    workflow.add_node("feed_explorer_agent", feed_explorer_agent_node)
    workflow.add_node("research_analyst_agent", research_analyst_agent_node)
    workflow.add_node("supervisor", build_supervisor_chain(llm))
    workflow.add_node("fallback_agent", build_fallback_agent(llm))

    member_names = list(map(lambda x: x["name"], members))

    for member in member_names:
        workflow.add_edge(member, END)

    conditional_map = {k: k for k in member_names}
    workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)
    workflow.set_entry_point("supervisor")
    return workflow.compile()
