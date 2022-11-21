import { bezochteVlammekes } from "../helpers/stores";

let bezochteVlammekesValue;

bezochteVlammekes.subscribe((value) => {
		bezochteVlammekesValue = value;
	});

export const isVlamGevonden = (vlamNaam) => {
		return bezochteVlammekesValue.includes(vlamNaam);

}