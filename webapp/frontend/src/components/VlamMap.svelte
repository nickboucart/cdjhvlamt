<script>
	import { onMount, onDestroy } from "svelte";
	import { navigate } from "svelte-routing";
	import { bezochteVlammekes } from "../helpers/stores";
	import { isVlamGevonden } from "../helpers/gevondenHelper";

	export let vlammetjes;
	export let mapCenter = [50.7360524, 4.2374349];
	export let zoom = 12;

	let mapElement;
	let map;

	onMount(async () => {
		const leaflet = await import("leaflet");
		map = leaflet.map(mapElement).setView(mapCenter, zoom);

		leaflet
			.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
				attribution:
					'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
			})
			.addTo(map);

		vlammetjes.forEach((vlammetje) => {
			if (vlammetje.coord.lat) {
				const kleur = isVlamGevonden(vlammetje.naam) ? 'green' : 'blue';
				const c = leaflet
					.circle([vlammetje.coord.lat, vlammetje.coord.lng], {
						radius: 50,
					})
					.addTo(map)
					.on("click", (e) => {
						navigate(`/vlammetjes/${vlammetje.naam}`);
					});
				c.setStyle({color: kleur});

			}
		});
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
	main {
		text-align: center;
	}
	main div {
		margin:auto;
		width: 80%;
		height: 400px;
	}
</style>
