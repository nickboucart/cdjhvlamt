<script>
	import { useQuery } from "@sveltestack/svelte-query";
	import { navigate } from "svelte-routing";

	import { getDataForQuery } from "../helpers/APIHelpers";
	import { bezochteVlammekes } from "../helpers/stores";

	const queryResult = useQuery(
		"getVlam" + $$props.id,
		() => getDataForQuery("/vlammeke/" + $$props.id),
		{ staleTime: 3 * 60 * 1000 }
	);

	bezochteVlammekes.update((vlammen) => {
		vlammen.push($$props.id);
		return vlammen;
	});

	function onClick() {
		navigate(`/vlammetjes/${$$props.id}`);
	}
</script>

<div><p>Super cool!</p></div>
{#if $queryResult.isLoading}
	<p>Aan het laden...</p>
{:else if $queryResult.error}
	<span>An error has occurred: {$queryResult.error.message}</span>
{:else}
	<h2>Je hebt het vlammetje van {$queryResult.data.thingName} gevonden!!</h2>
	<button on:click={onClick}>Ok.</button>
{/if}
