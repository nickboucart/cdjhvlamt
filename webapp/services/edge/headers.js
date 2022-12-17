function handler(event) {
	var response = event.response;
	var headers = response.headers;

	// Set HTTP security headers
	// Since JavaScript doesn't allow for hyphens in variable names, we use the dict["key"] notation 
	headers['strict-transport-security'] = { value: 'max-age=63072000; includeSubdomains; preload'}; 
	headers['content-security-policy'] = { value: "default-src 'none'; connect-src: 'self' *.cdjhvlamt.be;img-src 'self'; script-src 'self';font-src fonts.gstatic.com; style-src 'self' fonts.googleapis.com; object-src 'none'; frame-src scratch.mit.edu"}; 
	headers['x-content-type-options'] = { value: 'nosniff'}; 
	headers['x-frame-options'] = {value: 'DENY'}; 

	// Return the response to viewers 
	return response;
}