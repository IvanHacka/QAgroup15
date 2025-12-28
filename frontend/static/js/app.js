class BugTracker {
    constructor() {
        this.bugs = [];
        this.allBugs = [];

        this.init();
    }

    init() {
        this.attachEventListeners();
        this.loadBugs();
    }

    attachEventListeners() {
        // New Bug button
        document.getElementById('newBugButton').addEventListener('click', () => {
            this.openBugModal();
        });

        // Bug form submission
        document.getElementById('bugForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveBug();
        });

        // Close buttons
        document.querySelectorAll('.close').forEach(closeBtn => {
            closeBtn.addEventListener('click', (e) => {
                e.target.closest('.modal').classList.remove('show');
            });
        });
    }

    async loadBugs() {
        try {
            this.allBugs = await BugAPI.getBugs();
            this.bugs = [...this.allBugs];
            this.renderBugs(this.bugs);
        } catch (error) {
            console.error('Failed to load bugs:', error);
            document.getElementById('bugList').innerHTML = `
                <div class="empty-state">
                    <div class="">Error</div>
                    <p>Failed to load bugs: ${error.message}</p>
                </div>
            `;
        }
    }

    renderBugs(bugs) {
        const bugList = document.getElementById('bugList');

        if (bugs.length === 0) {
            bugList.innerHTML = `
                <div class="empty-state">
                    <div class="">Bugs</div>
                    <p>No bugs found. Click "New Bug" to create one!</p>
                </div>
            `;
            return;
        }

        bugList.innerHTML = bugs.map(bug => `
            <div class="bug-item" data-bug-id="${bug.id}" style="cursor: pointer; padding: 20px; border: 2px solid #ddd; margin: 10px 0; border-radius: 8px; transition: all 0.2s;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 1.2em; font-weight: bold; color: #333;">
                            Bug ID: #${bug.id.substring(0, 8)}
                        </div>
                        <div style="font-size: 0.9em; color: #666; margin-top: 5px;">
                            Created: ${this.formatDate(bug.created_at)}
                        </div>
                    </div>
                    <div style="font-size: 2em;"></div>
                </div>
            </div>
        `).join('');


        // Attach click listeners
        bugList.querySelectorAll('.bug-item').forEach(card => {
            card.addEventListener('click', () => {
                const bugId = card.dataset.bugId;
                this.viewBug(bugId);
            });
        });
    }

    openBugModal() {
        const modal = document.getElementById('bugModal');
        const form = document.getElementById('bugForm');

        form.reset();
        modal.classList.add('show');
    }

    async saveBug() {
        try {
            // Create bug with empty object - ID will be auto-generated
            const bugData = {};

            const createdBug = await BugAPI.createBug(bugData);

            console.log('Bug created:', createdBug);
            alert(` Bug created!\nID: ${createdBug.id.substring(0, 8)}`);

            // Close modal and reload
            document.getElementById('bugModal').classList.remove('show');
            await this.loadBugs();

        } catch (error) {
            console.error('Error creating bug:', error);
            alert(' Error: ' + error.message);
        }
    }

    viewBug(bugId) {
        const bug = this.allBugs.find(b => b.id === bugId);
        if (!bug) {
            console.error('Bug not found:', bugId);
            return;
        }

        const modal = document.getElementById('viewModal');
        const content = document.getElementById('viewContent');

        modal.dataset.bugId = bugId;

        content.innerHTML = `
            <div style="padding: 20px;">
                <div style="margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px;">
                    <div style="font-weight: bold; color: #666; margin-bottom: 5px;">Bug ID</div>
                    <div style="font-size: 1.1em; font-family: monospace; color: #333;">${bug.id}</div>
                </div>

                <div style="margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px;">
                    <div style="font-weight: bold; color: #666; margin-bottom: 5px;">Created At</div>
                    <div style="color: #333;">${this.formatDate(bug.created_at)}</div>
                </div>
            </div>
        `;

        modal.classList.add('show');
    }

    formatDate(isoString) {
        if (!isoString) return 'N/A';
        try {
            const date = new Date(isoString);
            return date.toLocaleString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
        } catch (e) {
            return 'Invalid Date';
        }
    }
}

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    console.log('Bug Tracker Initialized');
    new BugTracker();
});