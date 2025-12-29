class BugTracker {
  constructor() {
    this.bugs = [];
    this.allBugs = [];
    this.currentUser = null;

    // search state
    this.searchMode = "ID"; // "ID" | "TITLE"
    this.searchQuery = "";

    this.init();
  }

  init() {
    this.setupLogin(); // must login first
    this.attachEventListeners();
  }

  /*
     Login*/

  setupLogin() {
    const loginModal = document.getElementById("loginModal");
    const loginForm = document.getElementById("loginForm");
    const loginError = document.getElementById("loginError");

    loginModal.classList.add("show");

    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      loginError.innerText = "";

      const username = document.getElementById("loginUsername").value.trim();
      const password = document.getElementById("loginPassword").value;

      try {
        const res = await fetch("/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        });

        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.error || "Login failed");
        }

        this.currentUser = data.user;
        loginModal.classList.remove("show");

        await this.loadBugs();
      } catch (err) {
        loginError.innerText = err.message;
      }
    });
  }

  /* 
     EVENT LISTENER */

  attachEventListeners() {
    // New Bug button (blocked if not login)
    document.getElementById("newBugButton").addEventListener("click", () => {
      if (!this.currentUser) {
        alert("Please login first");
        return;
      }
      this.openBugModal();
    });

    // Bug form submission
    document.getElementById("bugForm").addEventListener("submit", (e) => {
      e.preventDefault();
      this.saveBug();
    });

    // close modal buttons
    document.querySelectorAll(".close").forEach((closeBtn) => {
      closeBtn.addEventListener("click", (e) => {
        e.target.closest(".modal").classList.remove("show");
      });
    });

    // Search bar 
    const searchInput = document.getElementById("searchInput");
    const searchModeBtn = document.getElementById("searchModeBtn");
    const searchClearBtn = document.getElementById("searchClearBtn");

    if (searchInput && searchModeBtn && searchClearBtn) {
      // type to search (((live)
      searchInput.addEventListener("input", () => {
        this.searchQuery = searchInput.value.trim();
        this.applySearchAndRender();
      });

      // press Enter to search 
      searchInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
          e.preventDefault();
          this.searchQuery = searchInput.value.trim();
          this.applySearchAndRender();
        }
      });

      // toggle mode: ID or TITLE
      searchModeBtn.addEventListener("click", () => {
        this.searchMode = this.searchMode === "ID" ? "TITLE" : "ID";
        searchModeBtn.textContent = this.searchMode === "ID" ? "ID" : "Name";
        searchInput.placeholder =
          this.searchMode === "ID" ? "Search by Bug ID…" : "Search by Bug name…";

        // re apply search
        this.searchQuery = searchInput.value.trim();
        this.applySearchAndRender();
      });

      // clear
      searchClearBtn.addEventListener("click", () => {
        searchInput.value = "";
        this.searchQuery = "";
        this.applySearchAndRender();
      });
    }
  }

  /* 
     Lload and render */

  async loadBugs() {
    try {
      this.allBugs = await BugAPI.getBugs();

      // use search if any
      this.applySearchAndRender();
    } catch (error) {
      console.error("Failed to load bugs:", error);
      document.getElementById("bugList").innerHTML = `
        <div class="empty-state">
          <h3>Error</h3>
          <p>${error.message}</p>
        </div>
      `;
    }
  }

  applySearchAndRender() {
  const q = (this.searchQuery || "").trim();

  if (!q) {
    this.bugs = [...this.allBugs];
    this.renderBugs(this.bugs);
    return;
  }

  const qLower = q.toLowerCase();

  if (this.searchMode === "ID") {
    this.bugs = this.allBugs.filter((b) => {
      const shortId = ((b.id || "").substring(0, 8)).toLowerCase();
      return shortId.startsWith(qLower); 
    });
  } else {
    // Tittle or name mode
    this.bugs = this.allBugs.filter((b) => {
      const title = (b.title || "").toLowerCase();
      return title.includes(qLower);
    });
  }

  this.renderBugs(this.bugs);
}


  renderBugs(bugs) {
    const bugList = document.getElementById("bugList");

    if (!bugs || bugs.length === 0) {
      const modeText = this.searchQuery
        ? `No results for "${this.searchQuery}"`
        : 'No bugs found. Click "New Bug" to create one!';
      bugList.innerHTML = `
        <div class="empty-state">
          <h3>Bugs</h3>
          <p>${modeText}</p>
        </div>
      `;
      return;
    }

    bugList.innerHTML = bugs
      .map(
        (bug) => `
        <div class="bug-card" data-bug-id="${bug.id}">
          <div class="bug-header">
            <div>
              <div class="bug-title">${bug.title}</div>
              <div class="bug-id">#${(bug.id || "").substring(0, 8)}</div>
            </div>
          </div>

          <div class="bug-card-meta">
            <span>Created: ${this.formatDate(bug.created_at)}</span>
            <span>Priority: ${bug.priority}</span>
            <span>Status: ${bug.status}</span>
          </div>
        </div>
      `
      )
      .join("");

    document.querySelectorAll(".bug-card").forEach((card) => {
      card.addEventListener("click", () => {
        this.viewBug(card.dataset.bugId);
      });
    });
  }

  /* 
     CREATE / EDIT */

  openBugModal() {
    const modal = document.getElementById("bugModal");
    const form = document.getElementById("bugForm");

    form.reset();
    document.getElementById("bugStatus").value = "OPEN";
    document.getElementById("bugPriority").value = "LOW";
    const assignEl = document.getElementById("bugAssignedTo");
    if (assignEl) assignEl.value = "";

    // clear edit id
    const idEl = document.getElementById("bugId");
    if (idEl) idEl.value = "";

    modal.classList.add("show");
  }

  async saveBug() {
    try {
      if (!this.currentUser) {
        alert("Please login first");
        return;
      }

      const fd = new FormData(document.getElementById("bugForm"));
      const editingId = (fd.get("id") || "").trim();

      const bugData = {
        title: (fd.get("title") || "").trim(),
        description: (fd.get("description") || "").trim(),
        priority: fd.get("priority"),
        status: fd.get("status"),
        tester_id: this.currentUser.username,
        assigned_to: fd.get("assigned_to") || "",
      };

      // create vs update (depends on your existing API)
      let saved;
      if (editingId) {
        saved = await BugAPI.updateBug(editingId, bugData);
        alert(`Bug updated! #${editingId.substring(0, 8)}`);
      } else {
        saved = await BugAPI.createBug(bugData);
        alert(`Bug created! #${saved.id.substring(0, 8)}`);
      }

      document.getElementById("bugModal").classList.remove("show");
      await this.loadBugs();
    } catch (error) {
      alert(error.message || "Server error");
    }
  }

  /*
     VIEW BUG */

  viewBug(bugId) {
    const bug = this.allBugs.find((b) => b.id === bugId);
    if (!bug) return;

    document.getElementById("viewContent").innerHTML = `
      <h2>${bug.title}</h2>
      <p>${bug.description}</p>
      <p><strong>Status:</strong> ${bug.status}</p>
      <p><strong>Priority:</strong> ${bug.priority}</p>
      <p><strong>Assigned To:</strong> ${bug.assigned_to || "Unassigned"}</p>
      <p><strong>Created:</strong> ${this.formatDate(bug.created_at)}</p>

      <div style="display:flex; gap:10px; margin-top:12px;">
        <button id="editBugBtn">Edit</button>
        <button id="deleteBugBtn" style="background:#c0392b; color:#fff;">Delete</button>
      </div>
    `;

    document.getElementById("viewModal").classList.add("show");

    // Edit
    setTimeout(() => {
      const editBtn = document.getElementById("editBugBtn");
      if (editBtn) {
        editBtn.onclick = () => {
          document.getElementById("viewModal").classList.remove("show");
          this.openEditBugModal(bug);
        };
      }

      // Delete
      const delBtn = document.getElementById("deleteBugBtn");
      if (delBtn) {
        delBtn.onclick = async () => {
          const ok = confirm("Delete this bug?");
          if (!ok) return;
          try {
            await BugAPI.deleteBug(bug.id);
            document.getElementById("viewModal").classList.remove("show");
            await this.loadBugs();
          } catch (e) {
            alert(e.message || "Failed to delete bug");
          }
        };
      }
    }, 0);
  }

  openEditBugModal(bug) {
    const modal = document.getElementById("bugModal");
    const titleEl = document.getElementById("bugTitle");
    const descEl = document.getElementById("bugDescription");
    const priEl = document.getElementById("bugPriority");
    const statusEl = document.getElementById("bugStatus");
    const idEl = document.getElementById("bugId");
    const assignEl = document.getElementById("bugAssignedTo");

    // set modal title
    const modalTitle = modal.querySelector(".modal-title");
    if (modalTitle) modalTitle.textContent = "Edit Bug";

    if (idEl) idEl.value = bug.id;
    if (titleEl) titleEl.value = bug.title || "";
    if (descEl) descEl.value = bug.description || "";
    if (priEl) priEl.value = bug.priority || "LOW";
    if (statusEl) statusEl.value = bug.status || "OPEN";
    if (assignEl) assignEl.value = bug.assigned_to || "";

    modal.classList.add("show");
  }

  /* 
     UTIL*/

  formatDate(isoString) {
    if (!isoString) return "N/A";
    return new Date(isoString).toLocaleString();
  }
}

document.addEventListener("DOMContentLoaded", () => {
  new BugTracker();
});
