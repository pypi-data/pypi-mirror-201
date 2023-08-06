type CodeBlocks = Record<"R" | "PYTHON" | "SQL", string[]>;

export const getCodeFromBody = async (body: string) => {
	const bodyCleaned = body
		.split("\n")
		.filter((sentence) => sentence.trim() !== "");

	const codeBlocks: CodeBlocks = {
		R: [],
		PYTHON: [],
		SQL: [],
	};
	const allLangs = Object.keys(codeBlocks);

	let inBlock = false;
	let currentLang: keyof CodeBlocks | "" = "";
	let currentBlock = "";
	bodyCleaned.forEach((sentence) => {
		const match = sentence.match(/^```\s*(r|python|sql)/);
		if (match !== null) {
			if (match[1] && allLangs.includes(match[1].toUpperCase())) {
				currentLang = match[1].toUpperCase() as keyof CodeBlocks;
			}
			inBlock = true;
		}

		if (sentence === "```") {
			inBlock = false;
			if (currentLang) {
				codeBlocks[currentLang].push(currentBlock);
			}
			currentBlock = "";
		}

		if (!match && inBlock) {
			currentBlock += sentence + "\n";
		}
	});

	const code = {
		R: codeBlocks.R.join("\n"),
		PYTHON: codeBlocks.PYTHON.join("\n"),
		SQL: codeBlocks.SQL.join("\n"),
	};

	return code;
};
