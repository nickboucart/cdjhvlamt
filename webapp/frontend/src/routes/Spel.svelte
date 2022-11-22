<script>
	import { Link } from "svelte-routing";
	import { useQuery } from "@sveltestack/svelte-query";
	import VlamMap from "../components/VlamMap.svelte";
	import { getDataForQuery } from "../helpers/APIHelpers";

	const queryResult = useQuery(
		"getVlammetjes",
		() => getDataForQuery("/vlammekes"),
		{ staleTime: 3 * 60 * 1000 }
	);
</script>

<div class="spel">
	<h1>De VlammetjesKaart</h1>
	<p>
		Kan jij zoveel mogelijk vlammetjes vinden in Halle en omstreken? Ga ter
		plaatse, scan de QR code in die je daar vindt en unlock de besturing van de
		vlammetjes
	</p>
	<p>
		Blauwe cirkels op de kaart tonen vlammetjes die je nog niet gevonde hebt, de
		groene heb je al wel gezien.
	</p>
	<p>Klik op de cirkels om meer details over het vlammetje te zien.</p>
	{#if $queryResult.isLoading}
		<span>Loading...</span>
	{:else if $queryResult.error}
		<span>An error has occurred: {$queryResult.error.message}</span>
	{:else}
		<VlamMap vlammetjes={$queryResult.data} />
	{/if}
</div>

<style>
	.spel {
		margin: auto;
		width: 90%;
	}

	.spel p {
		margin: auto;
		width: 60%;
		margin-bottom: 10px;
	}
</style>
