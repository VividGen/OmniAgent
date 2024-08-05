from dotenv import load_dotenv

from omniagent.agents.agent_factory import create_agent
from omniagent.conf.llm_provider import get_current_llm
from omniagent.tools.coin_market_executor import CoinMarketExecutor
from omniagent.tools.funding_rate_executor import FundingRateExecutor
from omniagent.tools.nft_rank_executor import NFTRankingExecutor
from omniagent.tools.nft_search_executor import NFTSearchExecutor
from omniagent.tools.price_executor import PriceExecutor
from omniagent.tools.tavily_executor import tavily_executor

load_dotenv()
llm = get_current_llm()

market_analysis_agent = create_agent(
    llm,
    [tavily_executor, PriceExecutor(), FundingRateExecutor(), NFTSearchExecutor(), NFTRankingExecutor(), CoinMarketExecutor()],
    """
You are MarketAnalyst, responsible for providing market data analysis.
Help users understand market dynamics and trends by retrieving real-time price information of tokens.

Your answer should be detailed and include puns or jokes where possible \
And keep a lively, enthusiastic, and energetic tone, maybe include some emojis.
""".strip(),
)
