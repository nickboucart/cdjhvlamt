<script>
	import { onMount, onDestroy } from "svelte";
	import Vlam from "../routes/Vlam.svelte";

	export let vlammetjes;
	let mapElement;
	let map;

	onMount(async () => {
		const leaflet = await import("leaflet");
		console.log(vlammetjes);

		map = leaflet.map(mapElement).setView([50.7360524, 4.2374349], 13);

		leaflet
			.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
				attribution:
					'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
			})
			.addTo(map);

		vlammetjes.forEach((vlammetje) => {
			if (vlammetje.attributes.lat) {
				leaflet
					.marker([vlammetje.attributes.lat, vlammetje.attributes.lng])
					.addTo(map);
			}
		});

		// leaflet.marker([51.5, -0.09]).addTo(map)
		// 		.bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
		// 		.openPopup();
	});

	onDestroy(async () => {
		if (map) {
			console.log("Unloading Leaflet map.");
			map.remove();
		}
	});
</script>

<main>
	<div bind:this={mapElement} />
</main>

<style>
	@import "leaflet/dist/leaflet.css";
	main div {
		width: 60%;
		height: 600px;
	}
</style>
