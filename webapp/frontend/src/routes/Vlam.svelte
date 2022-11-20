<script>
	import { useQuery } from "@sveltestack/svelte-query";

	import { postData, getDataForQuery } from "../helpers/APIHelpers";

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
	<h1>Individuele Vlam</h1>

	{#if $queryResult.isLoading}
		<span>Loading...</span>
	{:else if $queryResult.error}
		<span>An error has occurred: {$queryResult.error.message}</span>
	{:else}
		<h2>Toon de details van {$queryResult.data.attributes.eigenaar}</h2>
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
	{/if}
	<!-- {#await getVlam()}
		Even geduld, we laden data...
	{:then vlam}
		<h2>Toon de details van {vlam.attributes.eigenaar}</h2>
		<p>
			Stuur het vlammetje aan:
			<button on:click={() => onClick("fire")}>vlam animatie</button>
			<button on:click={() => onClick("conjunction")}>andere animatie</button>
		</p>
	{/await} -->
</div>
