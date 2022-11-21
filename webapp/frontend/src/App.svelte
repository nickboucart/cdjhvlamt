<script>
  import { Router, Link, Route } from "svelte-routing";
  import { QueryClient, QueryClientProvider } from '@sveltestack/svelte-query';


  import Home from "./routes/Home.svelte";
  import Vlam from "./routes/Vlam.svelte";
  import Spel from "./routes/Spel.svelte";
  import OverOns from "./routes/OverOns.svelte";
  import Footer from "./components/Footer.svelte";
  import Privacy from "./routes/Privacy.svelte";
  
  export let url = "";
  const queryClient = new QueryClient();
  </script>
  
  <QueryClientProvider client={queryClient}>
  <Router url="{url}">
    <nav>
      <Link to="/">Home</Link>
      <Link to="/het-spel">Speel het spel</Link>
      <Link to="/about">Over Ons</Link>
    </nav>
    <div>
      <Route path="het-spel" component="{Spel}" />
      <Route path="vlammetjes/:id" component="{Vlam}" />
      <Route path="about" component="{OverOns}" />
      <Route path="privacy" component="{Privacy}" />
      <Route path="/"><Home /></Route>
    </div>
    <Footer />
  </Router>
</QueryClientProvider>