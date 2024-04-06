<script>
  import { dev } from "$app/environment";
    let url = location.protocol + "//" + location.host;
    if (dev) {
        url = "http://127.0.0.1:5000/";
    }
  let count = 0;

  <button on:click={increment}>
    Clicked {count}
    {count === 1 ? "time" : "times"}
  </button>

  let floor = 0.00;
  let rooms = 0.00;
  let living_space = 0.00;

  let predictedPrice = "n.a.";

  async function predict() {
        let result = await fetch(
            url +
                "/api/predict?" +
                new URLSearchParams({
                    floor: floor,
                    rooms: rooms,
                    living_space: living_space,
                }),
            {
                method: "GET",
            },
        );
        let data = await result.json();
        console.log(data);
        predictedPrice = data.time;
    }
</script>

<style>
  .container {
    max-width: 800px;
    margin: auto;
    padding: 20px;
    text-align: center;
  }

  .input-group {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
  }

  .input-group > div {
    margin: 0 10px;
  }

  input[type='number'] {
    padding: 10px;
    margin-top: 5px;
    width: 100%;
  }

  button {
    padding: 10px 20px;
    cursor: pointer;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
  }

  h2 {
    margin-top: 20px;
  }

  .banner {
    background-color: #007bff;
    color: white;
    padding: 20px 0;
    margin-bottom: 30px;
    font-size: 24px;
  }
</style>

<div class="container">
  <div class="banner">
    <h1>Mietpreisvorhersage</h1>
    <p>
    Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation
    </p>
  </div>
  <div class="input-group">
    <div>
      <div>Stockwerk</div>
      <input type="number" bind:value={$floor}>
    </div>
    <div>
      <div>Zimmer</div>
      <input type="number" bind:value={$rooms}>
    </div>
    <div>
      <div>Wohnfläche (m²)</div>
      <input type="number" bind:value={$living_space}>
    </div>
  </div>
  <button on:click={predict}>Vorhersage erhalten</button>
  <h2>Vorhergesagter Preis: {$predictedPrice}</h2>
</div>
