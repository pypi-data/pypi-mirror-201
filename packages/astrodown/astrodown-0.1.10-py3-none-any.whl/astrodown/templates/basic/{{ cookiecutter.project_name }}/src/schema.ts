import { z } from "astro:content";

const ExportData = z.union([
	z.string(),
	z.number(),
	z.boolean(),
	z.object({
		name: z.string(),
		type: z.enum(["raw", "pandas", "s3"]),
		value: z.union([
			z.string(),
			z.number(),
			z.boolean(),
			z.array(z.string()),
			z.array(z.number()),
			z.array(z.boolean()),
		]),
	}),
]);

const Relationship = z.union([
	z.string(),
	z.object({
		id: z.string(),
		label: z.string().optional(),
	}),
]);

export type ExportData = z.infer<typeof ExportData>;

export const analysisSchema = z.object({
	title: z.string(),
	author: z.union([z.string(), z.array(z.string())]),
	id: z.string().optional(),
	label: z.string().optional(),
	date: z.string().transform((str) => new Date(str)),
	description: z.string().optional(),
	tags: z.array(z.string()).default([]),
	exports: z.array(ExportData).default([]),
	relationships: z.array(Relationship).default([]),
});

export const dataSchema = z.object({
	title: z.string(),
	id: z.string().optional(),
	label: z.string().optional(),
	previewURL: z.string().optional(),
	description: z.string().optional(),
	exports: z.array(ExportData).default([]),
	relationships: z.array(Relationship).default([]),
});
