import { defineConfig } from "astro/config";
import yaml from "@rollup/plugin-yaml";

// https://astro.build/config
import tailwind from "@astrojs/tailwind";

// https://astro.build/config
import react from "@astrojs/react";

// https://astro.build/config
export default defineConfig({
	integrations: [tailwind(), react()],
	vite: {
		plguins: [yaml()],
	},
});
