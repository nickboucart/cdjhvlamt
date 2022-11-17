<script>
  	import { onMount } from 'svelte';
  import { Router, Link, Route } from "svelte-routing";
  import Home from "./routes/Home.svelte";
  import Vlammetjes from "./routes/Vlammetjes.svelte";
  import Vlam from "./routes/Vlam.svelte";
  // import VlamMap from "./components/VlamMap.svelte";
  
  export let url = "";

  let response = "";
  let vlammetjes = [];

  onMount(async () => {
		const res = await fetch(import.meta.env.VITE_APP_API_URL + '/vlammekes');
		vlammetjes = await res.json();
	});

  function onClick() {
    fetch(import.meta.env.VITE_APP_API_URL, {
      method: "GET",
    })
      .then((response) => response.text())
      .then((data) => {
        response = data;
    });
  }


  </script>
  
  
  <Router url="{url}">
    <nav>
      <Link to="/">Home</Link>
      <Link to="/vlammetjes">De Vlammetjes</Link>
      <!-- <Link to="about">About</Link>
      <Link to="blog">Blog</Link> -->
    </nav>
    <div>
      <!-- <Route path="blog/:id" component="{BlogPost}" />
      <Route path="blog" component="{Blog}" />
      <Route path="about" component="{About}" /> -->
      <Route path="vlammetjes/:id" component="{Vlam}" />
      <Route path="vlammetjes" component="{Vlammetjes}" />
      <Route path="/"><Home /></Route>
    </div>
    <div>
     <button on:click={onClick}>Click Me to test our api</button>
     <p>API response: {response}</p>

     <ul>
      {#each vlammetjes as { naam, vlamnaam }, i }
      <li> Vlam van {naam}</li>
      {/each}
     </ul>
      <!-- <VlamMap /> -->
    </div>
  </Router>