import { defineCollection } from "astro:content";
import { analysisSchema, dataSchema } from "../schema";

export const analysis = defineCollection({
	schema: analysisSchema,
});

export const data = defineCollection({
	schema: dataSchema,
});

export const collections = {
	analysis,
	data,
};
