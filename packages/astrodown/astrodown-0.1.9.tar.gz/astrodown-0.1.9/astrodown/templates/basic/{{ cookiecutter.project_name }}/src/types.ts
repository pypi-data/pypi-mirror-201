export type DataPreviewConfig = {
	data: Record<string, string>[];
	nrow: number;
	ncol: number;
	headers: string[];
	title?: string;
	description?: string;
};
