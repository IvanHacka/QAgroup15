const BASE_URL = '/api';

class BugAPI {
    static async getBugs(){
        const response = await fetch(`${BASE_URL}/bugs`);
        if(!response.ok) throw new Error("Failed to fetch.");
        return response.json();
    }

    static async createBug(bugData){
        const response = await fetch(`${BASE_URL}/bugs`,{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(bugData)
        });
        if(!response.ok){
            const error = await response.json();
            throw new Error(error.error || 'Failed to create bug');
        }
        return response.json()
    }

    static async assignBug(bug_id, assignedTo) {
        const response = await fetch(`${BASE_URL}/bugs/${bug_id}/assign`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({assigned_to: assignedTo})
        });

        if(!response.ok) throw new Error('Failed to assign bug');
        return response.json();
    }
}