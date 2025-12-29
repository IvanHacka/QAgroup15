from backend.controllers.BugController import BugController
from backend.repo.BugRepo import BugRepo
from backend.services.BugService import BugService

from backend.controllers.UserController import UserController
from backend.services.UserService import UserService


def print_menu():
    print("\n=== Bug Tracking System ===")
    print("1. List all bugs")
    print("2. Search bugs")
    print("3. Create bug")
    print("4. Update bug details")
    print("5. Update bug status")
    print("6. Assign bug")
    print("7. Delete bug")
    print("8. Login")
    print("0. Exit")

# I have done
def main():
    bug_repo = BugRepo()
    bug_service = BugService(bug_repo)
    bug_controller = BugController(bug_service)

    user_service = UserService()
    user_controller = UserController(user_service)

    print("Bug Tracking System started (CLI mode)")


    # print menu after every entry to wait for next input
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":#List Bugs
                print("List Bugs")
                print("0. List Number of Open & Closed Bugs")
                print("1. List All Bugs(No Order)")
                print("2. List By Priority(Descending)")
                print("3. List in Alphabetical order(Title A-Z)")

                ListChoice=input("Choose an option: ").strip()

                bugs = bug_controller.get_all()
                if ListChoice == "0":
                    OpenBugs=0
                    ClosedBugs=0
                    for bug in bugs:
                        if bug.to_dict()["status"] =="OPEN":
                            OpenBugs+=1
                        elif bug.to_dict()["status"] =="CLOSED":
                            ClosedBugs+=1
                    print("Open Bugs: " + str(OpenBugs))
                    print("Closed Bugs: " + str(ClosedBugs))
                elif ListChoice == "1":
                    for bug in bugs:
                        print(bug.to_dict())
                elif ListChoice == "2":
                    # print high priority bugs first
                    print("-High Priority-")
                    for bug in bugs:
                        if bug.to_dict()["priority"] == "HIGH":
                            print(bug.to_dict())
                    # then print medium priority
                    print("-Medium Priority-")
                    for bug in bugs:
                        if bug.to_dict()["priority"] == "MEDIUM":
                            print(bug.to_dict())
                    # then low priority
                    print("-Low Priority-")
                    for bug in bugs:
                        if bug.to_dict()["priority"] == "LOW":
                             print(bug.to_dict())
                elif ListChoice == "3":
                    BugsAlphabetical=sorted(bugs, key=lambda bug: bug.title.lower())#new dict of bugs but sorted alphabetically
                    for bug in BugsAlphabetical:
                        print(bug.to_dict())

            elif choice == "2":
                mode = input("Search mode (title / id): ").strip()
                query = input("Search query: ").strip()
                bugs = bug_controller.get_all(mode, query)
                for bug in bugs:
                    print(bug.to_dict())

            elif choice == "3":
                title = input("Title: ")
                description = input("Description: ")
                priority = input("Priority (LOW / MEDIUM / HIGH): ").upper()
                status = input("Status (OPEN / IN_PROGRESS / CLOSED): ").upper()

                bug = bug_controller.create(
                    title=title,
                    description=description,
                    priority=priority,
                    status=status
                )
                print("Bug created:", bug.to_dict())

            elif choice == "4":
                bug_id = input("Bug ID: ")
                title = input("New title (leave blank to skip): ")
                description = input("New description (leave blank to skip): ")

                title = title if title else None
                description = description if description else None

                bug = bug_controller.update(bug_id, title, description)
                print("Bug updated:", bug.to_dict())

            elif choice == "5":
                bug_id = input("Bug ID: ")
                status = input("New status: ")
                bug = bug_controller.update_status(bug_id, status)
                print("Status updated:", bug.to_dict())

            elif choice == "6":
                bug_id = input("Bug ID: ")
                assigned_to = input("Assign to: ")
                bug = bug_controller.assign(bug_id, assigned_to)
                print("Bug assigned:", bug.to_dict())


            elif choice == "7":
                bug_id = input("Bug ID: ")
                confirm = input("Are you sure to delete this bug? (y/n): ").lower == "y"
                deleted = bug_controller.delete(bug_id, confirm)

                if deleted:
                    print(f"Bug {bug_id} deleted successfully.")
                else:
                    print(f"Bug {bug_id} could not be deleted.")

            elif choice == "8":
                username = input("Username: ")
                password = input("Password: ")
                success = user_controller.login(username, password)

                if success:
                    print("Login successful")
                else:
                    print("Login failed")

            elif choice == "0":
                print("Exiting system...")
                break

            else:
                print("Invalid option. Please try again.")

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
