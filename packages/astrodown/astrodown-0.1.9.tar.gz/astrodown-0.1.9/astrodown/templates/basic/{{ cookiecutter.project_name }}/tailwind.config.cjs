/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ["./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}"],
	theme: {
		extend: {
			fontFamily: {
				sans: "Roboto, sans-serif;",
				mono: "Fira Code, monospace;",
				serif: "'Roboto Slab', serif;",
			},
		},
	},
	plugins: [require("@tailwindcss/typography")],
};
