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
		<h2>Het vlammetje van {$queryResult.data.attributes.eigenaar}</h2>

		<VlamMap
			vlammetjes={[$queryResult.data]}
			mapCenter={[
				$queryResult.data.attributes.lat,
				$queryResult.data.attributes.lng,
			]}
			zoom={16}
		/>
		{#if isVlamGevonden($queryResult.data.thingName)}
			<p>
				Stuur het vlammetje aan:
				<!-- svelte-ignore a11y-invalid-attribute -->
				<a class="btn" href="#" title="Vlam Animatie" on:click|preventDefault={() => {onClick(e, $queryResult.data.thingName, "fire");return false;}}
					>vlam animatie</a
				>
				<!-- svelte-ignore a11y-invalid-attribute -->
				<a class="btn" href="#" title="Buiten naar binnen"
					on:click|preventDefault={() => onClick($queryResult.data.thingName, "conjunction")}
					>Buiten naar binnen</a
				>
				<!-- svelte-ignore a11y-invalid-attribute -->
				<a class="btn" href="#" title="Sidesweep"
					on:click|preventDefault={() => onClick($queryResult.data.thingName, "sidesweep")}
					>SideSweep</a
				>
				<!-- svelte-ignore a11y-invalid-attribute -->
				<a class="btn" href="#" title="Divergent"
				on:click|preventDefault={() => onClick($queryResult.data.thingName, "divergent")}
				>Divergent</a
			>
				<!-- svelte-ignore a11y-invalid-attribute -->
				<a class="btn" href="#" title="Jitter"
			on:click|preventDefault={() => onClick($queryResult.data.thingName, "jitter")}
			>Jitter</a
		>
			</p>
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

</style>