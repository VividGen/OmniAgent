import asyncio
import time

from omniagent.agent.function_agent import get_agent

question_list = [
    "Hello?",
    "What is the price of ETH?",
    "What did vitalik.eth do recently?",
    "Send 0.01 eth to vitalik.eth",
    "Swap 1 eth to usdt",
    "What is MODE chain?",
    "Give me the bitcoin price chart",
    "List some popular NFTs?",
    "Can you recommend me some articles about web3",
    "What's the largest dex with highest trading volume on Solana?",
    "When ETH ETF 19b-4 forms approved?",
    "Who are the main investors of EigenLayer?",
]


async def dummy(_) -> None:
    pass


async def init():
    # langchain.debug=True
    start = time.time()
    agent = get_agent("")
    for question in question_list:
        print(f"Question: {question}")
        try:
            await agent.arun(question)
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(1)

        print("--------------")

    end = time.time()

    print(f"Time elapsed: {end - start}")


if __name__ == "__main__":
    asyncio.run(init())
