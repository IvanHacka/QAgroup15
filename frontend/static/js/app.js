class BugTracker {
    constructor() {
        this.bugs = [];
        this.allBugs = [];
        this.currentUser = null;      //login state
        this.editingBugId = null;     // edit mode
        this.init();
    }

    init() {
        this.setupLogin();            // login first must need la
        this.attachEventListeners();
    }

    /*LOGIN (DO NOT TOUCH) */

    setupLogin() {
        const loginModal = document.getElementById('loginModal');
        const loginForm = document.getElementById('loginForm');
        const loginError = document.getElementById('loginError');

        loginModal.classList.add('show');

        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            loginError.innerText = "";

            const username = document.getElementById('loginUsername').value.trim();
            const password = document.getElementById('loginPassword').value;

            try {
                const res = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });

                const data = await res.json();
                if (!res.ok) throw new Error(data.error || 'Login failed');

                this.currentUser = data.user;
                loginModal.classList.remove('show');
                await this.loadBugs();

            } catch (err) {
                loginError.innerText = err.message;
            }
        });
    }

    /*
       EVENT LISTENERS */

    attachEventListeners() {
        document.getElementById('newBugButton').addEventListener('click', () => {
            if (!this.currentUser) {
                alert("Please login first");
                return;
            }
            this.openBugModal();
        });

        document.getElementById('bugForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveBug();
        });

        document.querySelectorAll('.close').forEach(btn => {
            btn.addEventListener('click', e => {
                e.target.closest('.modal').classList.remove('show');
            });
        });
    }

    /*
       LOAD & RENDER*/

    async loadBugs() {
        this.allBugs = await BugAPI.getBugs();
        this.bugs = [...this.allBugs];
        this.renderBugs(this.bugs);
    }

    renderBugs(bugs) {
        const bugList = document.getElementById('bugList');

        if (bugs.length === 0) {
            bugList.innerHTML = `
                <div class="empty-state">
                    <h3>Bugs</h3>
                    <p>No bugs found. Click "New Bug" to create one!</p>
                </div>
            `;
            return;
        }

        bugList.innerHTML = bugs.map(bug => `
            <div class="bug-card" data-bug-id="${bug.id}">
                <div class="bug-title">${bug.title}</div>
                <div class="bug-meta">
                    #${bug.id.substring(0,8)} |
                    ${this.formatDate(bug.created_at)} |
                    ${bug.priority} |
                    ${bug.status}
                </div>
            </div>
        `).join('');

        document.querySelectorAll('.bug-card').forEach(card => {
            card.addEventListener('click', () => {
                this.viewBug(card.dataset.bugId);
            });
        });
    }

    /* 
       CREATE / EDIT BUG */

    openBugModal() {
        const modal = document.getElementById('bugModal');
        const form = document.getElementById('bugForm');

        form.reset();
        document.getElementById('bugStatus').value = 'OPEN';
        document.getElementById('bugPriority').value = 'LOW';

        this.editingBugId = null; //new bug
        modal.querySelector('.modal-title').innerText = 'New Bug';
        modal.classList.add('show');
    }

    //open edit mode
    openEditBugModal(bug) {
        const modal = document.getElementById('bugModal');
        const form = document.getElementById('bugForm');

        form.title.value = bug.title;
        form.description.value = bug.description;
        form.priority.value = bug.priority;
        form.status.value = bug.status;

        this.editingBugId = bug.id;
        modal.querySelector('.modal-title').innerText = 'Edit Bug';
        modal.classList.add('show');
    }

    async saveBug() {
        if (!this.currentUser) {
            alert("Please login first");
            return;
        }

        const fd = new FormData(document.getElementById('bugForm'));

        const bugData = {
    title: fd.get('title').trim(),
    description: fd.get('description').trim(),
    priority: fd.get('priority'),
    status: fd.get('status'),
    tester_id: this.currentUser.username,
    assigned_to: fd.get('assigned_to') || null
};


        try {
            if (this.editingBugId) {
                // UPDATE
                await BugAPI.updateBug(this.editingBugId, bugData);
                alert("Bug updated");
            } else {
                //CREATE
                await BugAPI.createBug(bugData);
                alert("Bug created");
            }

            this.editingBugId = null;
            document.getElementById('bugModal').classList.remove('show');
            await this.loadBugs();

        } catch (err) {
            alert(err.message);
        }
    }

    /* 
       VIEW BUG*/

    viewBug(bugId) {
    const bug = this.allBugs.find(b => b.id === bugId);
    if (!bug) return;

    document.getElementById('viewContent').innerHTML = `
        <h2>${bug.title}</h2>
        <p>${bug.description || ''}</p>

        <p><strong>Status:</strong> ${bug.status}</p>
        <p><strong>Priority:</strong> ${bug.priority}</p>
        <p><strong>Created:</strong> ${this.formatDate(bug.created_at)}</p>

        <div style="display:flex; gap:10px; margin-top:16px;">
            <button id="editBugBtn">Edit</button>
            <button id="deleteBugBtn" style="background:#dc3545; color:white;">
                Delete
            </button>
        </div>
    `;

    document.getElementById('viewModal').classList.add('show');

    // Edit button
    document.getElementById('editBugBtn').onclick = () => {
        document.getElementById('viewModal').classList.remove('show');
        this.openEditBugModal(bug);
    };

    //Delete button
    document.getElementById('deleteBugBtn').onclick = async () => {
        const confirmed = confirm('Are you sure you want to delete this bug?');
        if (!confirmed) return;

        try {
            await BugAPI.deleteBug(bug.id);

            // close modal
            document.getElementById('viewModal').classList.remove('show');

            // re load bugs
            await this.loadBugs();

            alert('Bug deleted successfully');
        } catch (err) {
            alert(err.message || 'Failed to delete bug');
        }
    };
}


    /* 
       UTIL*/

    formatDate(iso) {
        return iso ? new Date(iso).toLocaleString() : 'N/A';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new BugTracker();
});
