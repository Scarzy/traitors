document.addEventListener("DOMContentLoaded", () => {
  const navbarHTML = `
    <nav class="navbar navbar-dark" aria-label="First navbar example" style="background-color:#4f0518">
      <div class="container-fluid">
        <a class="navbar-brand" href="#"></a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarsExample01" aria-controls="navbarsExample01" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarsExample01">
          <ul class="navbar-nav me-auto mb-2">
            <li class="nav-item">
              <a class="nav-link" id="homeoption" href="/user">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" id="banishoption" href="/banish">Banish</a>
            </li>
            <li class="nav-item">
              <a class="nav-link disabled" id="murderoption" href="/murder" tabindex="-1" aria-disabled="true">Murder</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" id="rulesoption" href="/rules">Rules</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" id="scoreboardoption" href="/scoreboard">Scoreboard</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" id="scheduleoption" href="/schedule">Schedule</a>
            </li>
          </ul>
          <form>
            <input class="form-control" type="text" placeholder="Search" aria-label="Search">
          </form>
        </div>
      </div>
    </nav>
  `;

  const placeholder = document.getElementById("navbar-placeholder");
  if (placeholder) {
    placeholder.innerHTML = navbarHTML;

    // Automatically highlight the active page link
    const currentPath = window.location.pathname;
    placeholder.querySelectorAll(".nav-link").forEach(link => {
      if (link.getAttribute("href") === currentPath) {
        link.classList.add("active");
        link.setAttribute("aria-current", "page");
      }
    });
  }
});
