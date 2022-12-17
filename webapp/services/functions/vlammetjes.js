import { IotData, Iot } from "aws-sdk";
import { ok } from "../helpers/responses";
import { transform } from "../helpers/transformVlammeke";

const IOTENDPOINT = "a26wt0x5359obq-ats.iot.eu-west-1.amazonaws.com"

const iotData = new IotData({ endpoint: IOTENDPOINT });
const iot = new Iot();



export const list = async (event) => {

	const vlammekes = await iot.listThings(
		{
			"maxResults": 100,
			"thingTypeName": "CDJHVlam"
		}
	).promise();

	return ok(vlammekes.things.map(transform));
};

export const get = async (event) => {
	const vlam = await iot.describeThing({ "thingName": event.pathParameters.id }).promise();
	return ok(transform(vlam));
};


export const update = async (event) => {
	const vlamNaam = event.pathParameters.id;
	const data = JSON.parse(event.body);
	const animation = data.animatie || 'fire';

	const payLoad = { "state": { "reported": { "animation": animation } } };

	const response = await iotData.updateThingShadow({
		thingName: vlamNaam,
		payload: JSON.stringify(payLoad)
	}).promise();

	console.log(response);

	return ok();
}