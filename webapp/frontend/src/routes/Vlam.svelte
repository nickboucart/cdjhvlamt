<script>
	import { useQuery } from "@sveltestack/svelte-query";

	import { postData, getDataForQuery } from "../helpers/APIHelpers";
	import VlamMap from "../components/VlamMap.svelte";
	import { isVlamGevonden } from "../helpers/gevondenHelper";

	const queryResult = useQuery(
		"getVlam" + $$props.id,
		() => getDataForQuery("/vlammeke/" + $$props.id),
		{ staleTime: 3 * 60 * 1000 }
	);

	async function onClick(thingName, animatie) {
		await postData("/vlammekes/" + thingName, { animatie: animatie });
		return false;
	}
</script>

<div>
	{#if $queryResult.isLoading}
		<span>Loading...</span>
	{:else if $queryResult.error}
		<span>An error has occurred: {$queryResult.error.message}</span>
	{:else}
		<h2>Vlammetje {$queryResult.data.naam}</h2>

		<VlamMap
			vlammetjes={[$queryResult.data]}
			mapCenter={[$queryResult.data.coord.lat, $queryResult.data.coord.lng]}
			zoom={16}
		/>
		{#if isVlamGevonden($queryResult.data.naam)}
			<p>Stuur het vlammetje aan:</p>
			<ul class="vlamcommandos">
				<li>
					<!-- svelte-ignore a11y-invalid-attribute -->
					<a
						class="btn"
						href="#"
						title="Vlam Animatie"
						on:click|preventDefault={() => {
							onClick($queryResult.data.thingName, "fire");
						}}>vlam animatie</a
					>
				</li>
				<li>
					<!-- svelte-ignore a11y-invalid-attribute -->
					<a
						class="btn"
						href="#"
						title="Buiten naar binnen"
						on:click|preventDefault={() =>
							onClick($queryResult.data.naam, "conjunction")}
						>Buiten naar binnen</a
					>
				</li>
				<li>
					<!-- svelte-ignore a11y-invalid-attribute -->
					<a
						class="btn"
						href="#"
						title="Sidesweep"
						on:click|preventDefault={() =>
							onClick($queryResult.data.naam, "sidesweep")}>Een kant naar de andere</a
					>
				</li>
				<li>
					<!-- svelte-ignore a11y-invalid-attribute -->
					<a
						class="btn"
						href="#"
						title="Divergent"
						on:click|preventDefault={() =>
							onClick($queryResult.data.naam, "divergent")}>Binnen naar buiten</a
					>
				</li>
				<li>
					<!-- svelte-ignore a11y-invalid-attribute -->
					<a
						class="btn"
						href="#"
						title="Jitter"
						on:click|preventDefault={() =>
							onClick($queryResult.data.naam, "jitter")}>Witte flikkering</a
					>
				</li>
			</ul>
		{:else}
			<p>
				Ga op zoek naar het vlammetje, scan de QR code op het raam en unlock de
				besturing van het vlammetje
			</p>
		{/if}
	{/if}
</div>

<style>
	.btn {
		background: var(--cd-yellow);
		color: var(--cd-blue);
		border: solid 2px var(--cd-yellow);
		border-radius: 10px;
		padding: 5px 5px;
	}

	ul.vlamcommandos {
		list-style: none;
	}

	ul.vlamcommandos li {
		display: block;
		margin: 20px;
	}
</style>
