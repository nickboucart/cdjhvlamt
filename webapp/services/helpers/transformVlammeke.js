export const transform = (vlam) => {
	return {naam: vlam.thingName, coord: {lng: vlam.attributes.lng, lat: vlam.attributes.lat}}
}