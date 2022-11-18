import { Api, ViteStaticSite } from "@serverless-stack/resources";

export function MyStack({ stack }) {
  const api = new Api(stack, "api", {
    cors: true,
    routes: {
      "POST /vlammekes/{id}": {
        function: {
          handler: "functions/vlammetjes.update",
          permissions: ['iot']
        }
      },
      "GET /": "functions/lambda.handler",
      "GET /vlammekes": {
        function: {
          handler: "functions/vlammetjes.list",
          permissions: ['iot']
        }
      }
    }
  });


  // Deploy our Svelte app
  const site = new ViteStaticSite(stack, "SvelteJSSite", {
    path: "frontend",
    environment: {
      // Pass in the API endpoint to our app
      VITE_APP_API_URL: api.url,
    },
  });

  // Show the URLs in the output
  stack.addOutputs({
    SiteUrl: site.url,
    ApiEndpoint: api.url,
  });


}
