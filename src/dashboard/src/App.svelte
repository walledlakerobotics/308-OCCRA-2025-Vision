<script lang="ts">
  import Dashboard from "./Dashboard.svelte";

  let selected = $state("Dashboard");
</script>

<nav>
  <ul>
    <li>
      <button
        class:selected={selected == "Dashboard"}
        onclick={() => (selected = "Dashboard")}>Dashboard</button
      >
    </li>
    <li>
      <button
        class:selected={selected == "Calibration"}
        onclick={() => (selected = "Calibration")}>Calibration</button
      >
    </li>
    <li>
      <button
        class:selected={selected == "Cameras"}
        onclick={() => (selected = "Cameras")}>Cameras</button
      >
    </li>
    <li>
      <button
        class:selected={selected == "Settings"}
        onclick={() => (selected = "Settings")}>Settings</button
      >
    </li>
  </ul>
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
  :root {
    --backgroundColor: rgb(36, 33, 48);
    --foregroundColor: rgb(22, 15, 43);
    --borderColor: rgb(190, 179, 237);

    --borderColorUnhover: rgb(71, 60, 121);
    --buttonColor: rgb(23, 14, 48);
    --activeButton: rgb(190, 240, 255);
  }

  ul {
    padding-left: 0;
  }

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

  nav li {
    list-style-type: none;

    margin-bottom: 5px;
  }

  main {
    margin-left: 3.5rem;
    padding-left: 0.5rem;
  }
</style>
