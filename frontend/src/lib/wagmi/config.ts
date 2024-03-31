import { env } from "@/env.mjs";
import { getDefaultConfig } from "@rainbow-me/rainbowkit";
import { mainnet, sepolia } from "wagmi/chains";

export const config = getDefaultConfig({
	appName: "OmniAgent",
	chains: [mainnet, sepolia],
	projectId: env.NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID,
	ssr: true, // If your dApp uses server side rendering (SSR)
});

export const chainId = env.NEXT_PUBLIC_CHAIN_ID;
