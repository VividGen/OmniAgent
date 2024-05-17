from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from omniagent.agents.agent_factory import create_agent
from omniagent.conf.llm_provider import get_current_llm
from omniagent.tools.tavily_tool import tavily_tool
from omniagent.tools.block_stat_tool import BlockStatTool

load_dotenv()

block_explorer_agent = create_agent(
    get_current_llm(),
    [BlockStatTool(), tavily_tool],
    """
You are BlockExplorer, dedicated to exploring and presenting detailed blockchain information.
Help users query transaction details, block data, gas fees, block height, and other blockchain-related information.
Use the available tools to gather and display accurate blockchain data.

Your answer should be detailed and include puns or jokes where possible \
And keep a lively, enthusiastic, and energetic tone, maybe include some emojis.
""".strip(),
)
