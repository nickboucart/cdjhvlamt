<script>
	import { onMount } from "svelte";
	import { getData, postData } from "../helpers/APIHelpers";

	let vlam;

	async function getVlam() {
		vlam = await getData("/vlammeke/" + $$props.id);
		return vlam;
	}

	async function onClick(animatie) {
		await postData("/vlammekes/" + vlam.thingName, { animatie: animatie });
	}
</script>

<div>
	<h1>Individuele Vlam</h1>

	{#await getVlam()}
		Even geduld, we laden data...
	{:then vlam}
		<h2>Toon de details van {vlam.attributes.eigenaar}</h2>
		<p>
			Stuur het vlammetje aan:
			<button on:click={() => onClick("fire")}>vlam animatie</button>
			<button on:click={() => onClick("conjunction")}>andere animatie</button>
		</p>
	{/await}
</div>
