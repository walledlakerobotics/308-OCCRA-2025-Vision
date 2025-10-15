<script lang="ts">
  import Dashboard from "./Dashboard.svelte";
  import Calibration from "./Calibration.svelte";
  import Cameras from "./Cameras.svelte";
  import Settings from "./Settings.svelte";
    import { expoOut } from "svelte/easing";

  function getTabWithId(id: string) {
    return tabs.filter((tab) => tab.id === id)[0];
  }

  function setTabAndPushState(tab: {
    id: string;
    name: string;
    icon: string;
    component: any;
  }) {
    if (selected.id == tab.id) return;

    selected = tab;
    history.pushState({ tabId: selected.id }, "", `#${selected.id}`);
  }

  function getURLHash() {
    return window.location.hash.replace("#", "");
  }

  const tabs = [
    {
      id: "dashboard",
      name: "Dashboard",
      icon: "dashboard",
      component: Dashboard,
  
    },
    {
      id: "calibration",
      name: "Calibration",
      icon: "tune",
      component: Calibration,
    },
    {
      id: "cameras",
      name: "Cameras",
      icon: "videocam",
      component: Cameras,
    },
    {
      id: "settings",
      name: "Settings",
      icon: "settings",
      component: Settings,
    },
  ];

  let startTab = getTabWithId(getURLHash());
  if (!startTab) {
    startTab = tabs[0];
    history.replaceState({ tabId: startTab.id }, "", `#${startTab.id}`);
  }

  let selected = $state(startTab);
  let expanded = $state(false);

  $effect(() => {
    document.title = selected.name;
  });

  window.addEventListener("popstate", (e) => {
    if (!e.state || !e.state.tabId) return;

    const tab = getTabWithId(e.state.tabId);
    if (tab) selected = tab;
  });

  window.addEventListener("hashchange", (e) => {
    const tab = getTabWithId(getURLHash());
    if (tab) selected = tab;
    else history.replaceState({ tabId: selected.id }, "", `#${selected.id}`);
  });
</script>

<nav class:expanded={expanded}>
  {#each tabs as tab}
    <button
      class:selected={selected.id == tab.id}
      onclick={() => setTabAndPushState(tab)}
      title={tab.name}
    >
      {tab.name}
    </button>
  {/each}
</nav>

<main>
  {#each tabs as tab}
    {#if selected.id == tab.id}
      <tab.component />
    {/if}
  {/each}
</main>

<style>
  nav {
    background-color: var(--foregroundColor);
    border-right: 1.5px solid var(--borderColor);
    box-shadow: 5px 5px 5px 5px rgba(0, 0, 0, 0.2);
    
    position: fixed;
    z-index: 2;


    margin: 0;
    padding: 0.5rem;

    height: 100%;
    width: 2.5rem;

    transition: 0.5s;
  }

  /* nav.expanded {
    padding-left: 1rem;
    padding-right: 1rem;
    width: 15rem;

    button {
      color: var(--borderColorUnhover);
      border-radius: 5px;
      transition: 0.2s;
    } 
  } */

  nav button {
    background-color: var(--buttonColor);

    border: solid;
    border-color: var(--borderColorUnhover);
    border-width: 1.5px;
    border-radius: 100%;

    margin-top: 5px;
    margin-bottom: 5px;

    width: 100%;
    padding: 10px;

    color: rgba(0, 0, 0, 0);

    transition: 0.5s;
  }

  nav button:hover {
    border-color: var(--borderColor)
  }

  
  /* nav button.expanded {
    color: var(--borderColor);
    border-color: var(--borderColor);
    margin-top: 10px;
  } */

  /* nav button:hover {
      border-color: var(--borderColor);
      color: rgb(190, 179, 237, 1);
    } */

  nav button:active,
  nav button.selected {
    border-color: var(--activeButton);
  }

  nav.expanded button:active,
  nav.expanded button.selected {
    color: var(--activeButton);
  }

  main {
    margin-left: 3.5rem;
    padding-left: 0.5rem;
  }

</style>
