<script>
	import { Link } from "svelte-routing";
	import { useQuery } from "@sveltestack/svelte-query";
	import VlamMap from "../components/VlamMap.svelte";
	import { getDataForQuery } from "../helpers/APIHelpers";

	const queryResult = useQuery("getVlammetjes", () =>
		getDataForQuery('/vlammekes'), {staleTime: 3*60*1000});

</script>

{#if $queryResult.isLoading}
<span>Loading...</span>
{:else if $queryResult.error}
<span>An error has occurred: {$queryResult.error.message}</span>
{:else}
<ul>
	{#each $queryResult.data as vlam }
	<li>
		<Link to={"/vlammetjes/" + vlam.thingName}
			>Vlam van {vlam.attributes.eigenaar}</Link
		>
	</li>
	{/each}
</ul>

<VlamMap vlammetjes={$queryResult.data} />
{/if}