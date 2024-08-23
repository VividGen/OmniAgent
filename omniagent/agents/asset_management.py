from dotenv import load_dotenv

from omniagent.agents.agent_factory import create_agent
from omniagent.conf.env import settings
from omniagent.conf.llm_provider import get_current_llm
from omniagent.executors.nft_balance_executor import NFTBalanceExecutor
from omniagent.executors.swap_executor import SwapExecutor
from omniagent.executors.token_balance_executor import TokenBalanceExecutor
from omniagent.executors.transfer_executor import TransferExecutor

load_dotenv()

executors = [SwapExecutor(), TransferExecutor()]
if settings.COVALENT_API_KEY:
    executors.extend([TokenBalanceExecutor(), NFTBalanceExecutor()])

asset_management_agent = create_agent(
    get_current_llm(),
    executors,
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
- For privacy reasons, do not include address information when generating widgets

Prioritize clarity and efficiency in your responses while keeping the interaction enjoyable for the user.
""".strip(),
)
