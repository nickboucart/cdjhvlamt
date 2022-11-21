<script>

console.log($$props);
const encodedURL = encodeURI($$props.location.origin + "/gevonden/" + $$props.id);
</script>


<h1>Print deze QR code af, kleef hem op de affiche en hang je affiche goed zichtbaar aan het raam!</h1>

<div>
	<img src="https://api.qrserver.com/v1/create-qr-code/?data={encodedURL}&size=400x400" alt="" title="" />

</div>


