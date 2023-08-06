import type { PyodideInterface } from "pyodide";
import { showError } from "./utils";

export const runPython = async (pyodide: PyodideInterface, code: string) => {
	try {
		const result = await pyodide.runPythonAsync(code);
		return result;
	} catch (e) {
		return showError(e);
	}
};
