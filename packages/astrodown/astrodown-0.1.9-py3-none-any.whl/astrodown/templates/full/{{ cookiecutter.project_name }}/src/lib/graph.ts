import { getCollection, CollectionEntry } from "astro:content";
import type { IUserNode, IUserEdge } from "@astrodown/graph";

export const colorConfig: Record<string, string> = {
	analysis: "#a991f7",
	data: "#3b82f6",
	accent: "#eab308",
};

const getMetadata = (
	entry: CollectionEntry<"data"> | CollectionEntry<"analysis">,
) => {
	return {
		id: entry.data.id || entry.id,
		label: entry.data.label || entry.data.title,
		type: entry.collection,
	};
};

export const getNode = (
	entry: CollectionEntry<"analysis"> | CollectionEntry<"data">,
	highlightId?: string,
): IUserNode => {
	const { id, label, type } = getMetadata(entry);
	const color = highlightId === id ? colorConfig.accent : colorConfig[type];
	return {
		id,
		data: {
			type,
			slug: entry.slug,
			title: entry.data.title,
			description: entry.data.description,
		},
		style: {
			label: {
				value: label,
				fontSize: 18,
			},
			keyshape: {
				size: 60,
				stroke: color,
				fill: color,
				fillOpacity: 0.2,
			},
		},
	};
};

export const getEdges = (
	entry: CollectionEntry<"analysis"> | CollectionEntry<"data">,
	highlightId?: string,
): IUserEdge[] => {
	const { id, label, type } = getMetadata(entry);
	const relationships = entry.data.relationships;
	const color = highlightId === id ? colorConfig.accent : colorConfig[type];
	if (typeof relationships === "string") {
		return [
			{
				source: id,
				target: relationships,
				style: { label: { value: "", fill: color, fontSize: 14 } },
			},
		];
	}
	return relationships.map((r) => {
		const targetId = typeof r === "string" ? r : r.id;
		const edgeLabel = typeof r === "string" ? "" : r.label;
		return {
			source: id,
			target: targetId,
			style: {
				label: {
					value: edgeLabel,
					fill: color,
					stroke: color,
					fontSize: 14,
				},
				keyshape: {
					stroke: color,
				},
			},
		};
	});
};

export const getGraphData = async (
	entryToHighlight?: CollectionEntry<"analysis"> | CollectionEntry<"data">,
) => {
	let highlightId: string | undefined;
	if (entryToHighlight) {
		highlightId = entryToHighlight.data.id || entryToHighlight.id;
	}
	const nodes: IUserNode[] = [];
	const edges: IUserEdge[] = [];
	const allNodes = (
		await Promise.all([getCollection("data"), getCollection("analysis")])
	).flat();
	allNodes.forEach((entry) => {
		const node = getNode(entry, highlightId);
		const nodeEdges = getEdges(entry, highlightId);
		nodes.push(node);
		edges.push(...nodeEdges);
	});

	return { nodes, edges };
};
