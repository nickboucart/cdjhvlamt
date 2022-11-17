export const list = async (event) => {
	const vlammekes = [{"naam": "florian", "vlamnaam":  "vlam-van-florian" }, {"naam": "arlieke", "vlamnaam":  "vlam-van-arlieke" }]
  return {
    statusCode: 200,
		headers: { 
			"Content-Type": "application/json",
			"Access-Control-Allow-Origin": "*" },
    body: JSON.stringify(vlammekes)
  };
};
