<script>
import { Router, Link, Route } from "svelte-routing";
import Home from "./routes/Home.svelte";
import Vlammetjes from "./routes/Vlammetjes.svelte";
import Vlam from "./routes/Vlam.svelte";

export let url = "";
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
</Router>