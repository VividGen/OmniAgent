import { TypographyStylesProvider } from "@mantine/core";

export default function Page() {
	return (
		<TypographyStylesProvider>
			<div
				dangerouslySetInnerHTML={{
					__html: `
					<h1>OmniAgent Executor</h1>
					<h2>What is OmniAgent Executor?</h2>
`,
				}}
			></div>
		</TypographyStylesProvider>
	);
}
