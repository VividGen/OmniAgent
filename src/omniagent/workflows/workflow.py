import operator
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import BaseMessage
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph
from loguru import logger




class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str


def create_node(agent, name):
    def run(state):
        logger.info(f"Running {name} agent")
        result = agent.invoke(state)
        return {"messages": [HumanMessage(content=result["output"], name=name)]}

    return run


def build_workflow():
    from omniagent.agents.asset_management import asset_management_agent
    from omniagent.agents.block_explore import block_explorer_agent
    from omniagent.agents.fallback import fallback
    from omniagent.agents.market_analysis import market_analysis_agent
    from omniagent.agents.project_management import research_analyst_agent
    from omniagent.agents.social_track import social_track_agent
    from omniagent.workflows.member import members
    from omniagent.workflows.supervisor_chain import supervisor_chain
    market_analysis_agent_node = create_node(
        market_analysis_agent, "market_analysis_agent"
    )
    social_track_agent_node = create_node(social_track_agent, "social_track_agent")
    asset_management_agent_node = create_node(
        asset_management_agent, "asset_management_agent"
    )
    block_explorer_agent_node = create_node(
        block_explorer_agent, "block_explorer_agent"
    )
    research_analyst_agent_node = create_node(
        research_analyst_agent, "research_analyst_agent"
    )

    workflow = StateGraph(AgentState)
    workflow.add_node("market_analysis_agent", market_analysis_agent_node)
    workflow.add_node("social_track_agent", social_track_agent_node)
    workflow.add_node("asset_management_agent", asset_management_agent_node)
    workflow.add_node("block_explorer_agent", block_explorer_agent_node)
    workflow.add_node("research_analyst_agent", research_analyst_agent_node)
    workflow.add_node("supervisor", supervisor_chain)
    workflow.add_node("fallback_agent", fallback)

    member_names = list(map(lambda x: x["name"], members))

    for member in member_names:
        if member == "fallback_agent":
            workflow.add_edge(member, END)
            continue
        workflow.add_edge(member, "supervisor")

    conditional_map = {k: k for k in member_names}
    conditional_map["FINISH"] = END
    workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)
    workflow.set_entry_point("supervisor")
    return workflow.compile()
