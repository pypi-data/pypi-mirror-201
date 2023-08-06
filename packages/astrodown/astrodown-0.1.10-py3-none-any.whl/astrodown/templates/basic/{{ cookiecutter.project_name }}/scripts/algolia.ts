import fs from "fs";
import path from "path";
import matter from "gray-matter";
import removeMd from "remove-markdown";
import glob from "glob";
import algoliasearch from "algoliasearch";
import * as dotenv from "dotenv";

dotenv.config();

const contentDir = path.join(process.cwd(), "src/content");
glob(`${contentDir}/**/*.md`, async (err, files) => {
	const allFiles = files.map((f) => {
		return { name: path.basename(f), path: f };
	});
	const data = allFiles.map(({ name, path }) => {
		try {
			const markdownWithMeta = fs.readFileSync(path);
			const { data: frontmatter, content } = matter(markdownWithMeta);
			return {
				objectID: frontmatter.slug || name,
				slug: frontmatter.slug || name,
				title: frontmatter.title,
				content: removeMd(content).replace(/\n/g, ""),
			};
		} catch (e) {
			// console.log(e.message)
		}
	});
	saveToAlgolia(data);
});

async function saveToAlgolia(data: Record<string, unknown>[]) {
	const client = algoliasearch(
		process.env.ALGOLIA_APP_ID!,
		process.env.ALGOLIA_WRITE_API_KEY!,
	);
	try {
		const response = await client.initIndex("Index name").saveObjects(data);
		console.log("save to algolia success with response", response);
	} catch (e) {
		console.log("save to algolia failed with error", e);
	}
}
