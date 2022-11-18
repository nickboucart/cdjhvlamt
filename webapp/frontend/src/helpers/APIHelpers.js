const BASE_URL = import.meta.env.VITE_APP_API_URL

export const getData = async (url = "") => {
	const response = await fetch(BASE_URL + url);
	const data = await response.json();
	return data;
}


export const postData = async (url = "", data = {}) => {
	const response = await fetch(BASE_URL +  url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(data)
	});
	data = await response.json();
	return data;
}