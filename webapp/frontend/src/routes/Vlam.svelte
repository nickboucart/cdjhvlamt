<script>
	import { useQuery } from "@sveltestack/svelte-query";

	import { postData, getDataForQuery } from "../helpers/APIHelpers";
	import VlamMap from "../components/VlamMap.svelte";

	const queryResult = useQuery(
		"getVlam" + $$props.id,
		() => getDataForQuery("/vlammeke/" + $$props.id),
		{ staleTime: 3 * 60 * 1000 }
	);

	async function onClick(thingName, animatie) {
		await postData("/vlammekes/" + thingName, { animatie: animatie });
	}
</script>

<div>
	{#if $queryResult.isLoading}
		<span>Loading...</span>
	{:else if $queryResult.error}
		<span>An error has occurred: {$queryResult.error.message}</span>
	{:else}
		<h2>Het vlammetje van {$queryResult.data.attributes.eigenaar}</h2>
		<p>
			Stuur het vlammetje aan:
			<button on:click={() => onClick($queryResult.data.thingName, "fire")}
				>vlam animatie</button
			>
			<button
				on:click={() => onClick($queryResult.data.thingName, "conjunction")}
				>andere animatie</button
			>
		</p>
		<VlamMap vlammetjes={[$queryResult.data]} mapCenter={[$queryResult.data.attributes.lat, $queryResult.data.attributes.lng]} zoom={16}/>
	{/if}
</div>
