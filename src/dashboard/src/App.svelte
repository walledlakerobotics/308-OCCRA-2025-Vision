<script lang="ts">
  import Dashboard from "./Dashboard.svelte";

  let selected = $state("Dashboard");
</script>

<nav>
  <button
    class:selected={selected == "Dashboard"}
    onclick={() => (selected = "Dashboard")}>Dashboard</button
  >
  <button
    class:selected={selected == "Calibration"}
    onclick={() => (selected = "Calibration")}>Calibration</button
  >
  <button
    class:selected={selected == "Cameras"}
    onclick={() => (selected = "Cameras")}>Cameras</button
  >
  <button
    class:selected={selected == "Settings"}
    onclick={() => (selected = "Settings")}>Settings</button
  >
</nav>

<main>
  {#if selected == "Dashboard"}
    <Dashboard />
  {:else if selected == "Calibration"}
    <h1>Calibration</h1>
  {:else if selected == "Cameras"}
    <h1>Cameras</h1>
  {:else if selected == "Settings"}
    <h1>Settings</h1>
  {/if}
</main>

<style>
  nav {
    background-color: var(--foregroundColor);
    border-right: 1.5px solid var(--borderColor);
    box-shadow: 5px 5px 5px 5px rgba(0, 0, 0, 0.2);

    position: fixed;

    margin: 0;
    padding: 0.5rem;

    height: 100%;
    width: 2.5rem;

    transition: 0.5s;
  }

  nav:hover {
    padding-left: 1rem;
    padding-right: 1rem;
    width: 15rem;

    button {
      color: var(--borderColorUnhover);
      border-radius: 5px;
      transition: 0.2s;
    }
  }

  nav button {
    background-color: var(--buttonColor);

    border: solid;
    border-color: var(--borderColorUnhover);
    border-width: 1.5px;
    border-radius: 100%;

    margin-top: 2.5px;
    margin-bottom: 2.5px;

    width: 100%;
    padding: 10px;

    color: rgba(0, 0, 0, 0);

    transition: 0.5s;
  }

  nav button:hover {
    color: var(--borderColor);
    border-color: var(--borderColor);
  }

  nav button:active,
  nav button.selected {
    border-color: var(--activeButton);
  }

  nav:hover button:active,
  nav:hover button.selected {
    color: var(--activeButton);
  }

  main {
    margin-left: 3.5rem;
    padding-left: 0.5rem;
  }
</style>
