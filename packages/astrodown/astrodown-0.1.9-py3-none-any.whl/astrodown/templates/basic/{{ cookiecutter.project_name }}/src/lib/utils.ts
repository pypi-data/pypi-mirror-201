export const objectToBase64 = (obj: Object) => {
	return Buffer.from(JSON.stringify(obj)).toString("base64");
};

export const showError = (error: unknown): string => {
	return error instanceof Error ? error.message : String(error);
};

export const classNames = (...classes: string[]) => {
	return classes.filter(Boolean).join(" ");
};

export const showArray = (x: string | string[]) => {
	if (x instanceof Array) {
		return x.join(", ");
	}

	return x;
};
