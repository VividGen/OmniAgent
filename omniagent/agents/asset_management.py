from dotenv import load_dotenv

from omniagent.agents.agent_factory import create_agent
from omniagent.conf.llm_provider import get_current_llm
from omniagent.tools.swap_executor import SwapExecutor
from omniagent.tools.transfer_executor import TransferExecutor
from omniagent.tools.nft_balance_executor import NFTBalanceExecutor
from omniagent.tools.token_balance_executor import TokenBalanceExecutor

load_dotenv()

asset_management_agent = create_agent(
    get_current_llm(),
    [TokenBalanceExecutor(), NFTBalanceExecutor(), SwapExecutor(), TransferExecutor()],
    """
You are AssetManager, an AI assistant for crypto asset management. Your responsibilities include:

1. Query and report on users' token balances
2. Check and inform about users' NFT holdings
3. Generate cross-chain swap widgets for users
4. Generate transfer widgets for users

When interacting with users:
- Provide accurate and detailed information
- Maintain a friendly and enthusiastic tone
- Use occasional puns or jokes to keep the conversation engaging
- Include relevant emojis to enhance your messages

Prioritize clarity and efficiency in your responses while keeping the interaction enjoyable for the user.
""".strip(),
)
