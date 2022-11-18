<script>
  import { Router, Link, Route } from "svelte-routing";
  import Home from "./routes/Home.svelte";
  import Vlammetjes from "./routes/Vlammetjes.svelte";
  import Vlam from "./routes/Vlam.svelte";
  // import VlamMap from "./components/VlamMap.svelte";
  
  export let url = "";

  </script>
  
  
  <Router url="{url}">
    <nav>
      <Link to="/">Home</Link>
      <Link to="/vlammetjes">De Vlammetjes</Link>
    </nav>
    <div>
      <Route path="vlammetjes/:id" component="{Vlam}" />
      <Route path="vlammetjes" component="{Vlammetjes}" />
      <Route path="/"><Home /></Route>
    </div>
  </Router>