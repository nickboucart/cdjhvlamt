import { IotData } from "aws-sdk";
import { ok } from "../helpers/responses";

const iotData = new IotData({ endpoint: "a26wt0x5359obq-ats.iot.eu-west-1.amazonaws.com" });


export const list = async (event) => {
	const vlammekes = [{ "naam": "florian", "vlamnaam": "vlam-van-florian" }, { "naam": "arlieke", "vlamnaam": "vlam-van-arlieke" }]
	return ok(vlammekes);
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

	return ok();
}