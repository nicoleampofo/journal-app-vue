<template>
  <div class="app-shell">
    <header class="app-header">
      <div>
        <p class="eyebrow">Personal reflection</p>
        <h1>Journal Flow</h1>
      </div>
      <nav class="nav-links">
        <router-link to="/">Entries</router-link>
        <router-link to="/new">New Entry</router-link>
        <router-link to="/calendar">Calendar</router-link>
      </nav>
    </header>

    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
:global(body) {
  margin: 0;
  font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: #f4f2ff;
  color: #221f39;
}

* {
  box-sizing: border-box;
}

.app-shell {
  min-height: 100vh;
  padding: 24px;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding: 16px 20px;
  border-radius: 16px;
  background: white;
  box-shadow: 0 10px 30px rgba(45, 39, 96, 0.08);
}

.eyebrow {
  margin: 0 0 4px;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-size: 0.75rem;
  color: #6b62a8;
}

h1 {
  margin: 0;
  font-size: 1.5rem;
}

.nav-links {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.nav-links a {
  text-decoration: none;
  color: #4d3f9a;
  font-weight: 600;
  padding: 8px 12px;
  border-radius: 999px;
}

.nav-links a.router-link-active {
  background: #6c63ff;
  color: white;
}

.content {
  max-width: 900px;
  margin: 0 auto;
}
</style>
