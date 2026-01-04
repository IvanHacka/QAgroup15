# QAgroup15
# A Software Bug Tracking and Reporting Tool.
This software system allows users to record, track, assign and manage bugs. Backend focused and no need for GUI.

## Workflow
>OPEN → IN_PROGRESS → RESOLVED → CLOSED
Bugs that are created are automatically set as OPEN

## Features

1. Create and log software bugs
2. Automatically assign unique bug IDs
3. Track bug status 
4. Assign bugs
5. Prioritise bugs (LOW / MEDIUM / HIGH)
6. Reopen closed bugs
7. Search bugs by ID, title, status, priority, or user
8. Persistent storage using JSON files
9. User authentication with account lockout after failed attempts

## Prequisities
- python 3.0 or above

## Installation
```bash

# Clone the repository
git clone [https://github.com/IvanHacka/QAgroup15]

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Running software
python main.py

## Login Details (Will be locked after 3 failed attempts)
usernames: staff01
password: password123

username: staff02
password: password123

## Using software
Login in using one of the above details. 
You will now see a numbered menu in the terminal.

To create a bug press 3 then follow instructions.
To see bugs press 1 then follow instructions.

The main actions include:
-Searching bugs
-Updating bug details
-Updating bug status
-Assigning bugs
-Reopening bugs
-Logging out

## Data storage
All the bug data is stored in a json file.
data/Bugs.json

The json file is automatically created and updated though the system. 

## Project Structure
QAgroup15/
├── backend/
│   ├── controllers/
│   ├── models/
│   ├── repo/
│   ├── services/
│   └── utils/
├── data/
│   └── Bugs.json
├── main.py
└── README.md

