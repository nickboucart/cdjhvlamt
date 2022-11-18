export const ok = (data = {}) => {
	return {
		statusCode: 200,
		headers: {
			"Content-Type": "application/json",
			"Access-Control-Allow-Origin": "*"
		},
		body: JSON.stringify(data)
	};
}

export const error = (statusCode, data) => {
	return {
		statusCode: statusCode,
		headers: {
			"Content-Type": "application/json",
			"Access-Control-Allow-Origin": "*"
		},
		body: JSON.stringify(data)
	};
}