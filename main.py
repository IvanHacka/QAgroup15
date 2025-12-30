from backend.controllers.BugController import BugController
from backend.repo.BugRepo import BugRepo
from backend.services.BugService import BugService

from backend.controllers.UserController import UserController
from backend.services.UserService import UserService

from backend.models.Bug import BugStatus



def print_menu():
    print("\n=== Bug Tracking System ===")
    print("1. List all bugs")
    print("2. Search bugs")
    print("3. Create bug")
    print("4. Update bug details")
    print("5. Update bug status")
    print("6. Assign bug")
    print("7. Delete bug")
    print("8. Logout")
    print("9. Reopen bug")   # 30 reopen
    print("0. Exit")



# I have done
def main():
    bug_repo = BugRepo()
    bug_service = BugService(bug_repo)
    bug_controller = BugController(bug_service)

    user_service = UserService()
    user_controller = UserController(user_service)


    print("Bug Tracking System started")

    current_user = None

    # print menu after every entry to wait for next input
    while True:
        if not current_user:
            current_user = login(user_controller)
        print_menu()
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":#List Bugs
                print("List Bugs")
                print("0.List Number of Open & Closed Bugs")
                print("1. List All Bugs(No Order)")
                print("2.List By Priority(Descending)")
                print("3.List in alphabetical order(Title A-Z)")

                ListChoice=input("Choose an option: ").strip()

                bugs = bug_controller.get_all()
                if ListChoice == "0":
                    active_bugs = 0
                    closed_bugs = 0

                    for bug in bugs:
                        status = bug.status  # BugStatus enum

                        if status in (
                            BugStatus.OPEN,
                            BugStatus.IN_PROGRESS,
                            BugStatus.REOPEN
                        ):
                            active_bugs += 1

                        elif status in (
                            BugStatus.CLOSED,
                            BugStatus.COMPLETED
                        ):
                            closed_bugs += 1

                    print("Active Bugs:", active_bugs)
                    print("Closed Bugs:", closed_bugs)

                elif ListChoice == "1":
                    for bug in bugs:
                        print(bug.to_dict())
                elif ListChoice == "2":
                    # print high priority bugs first
                    print("-High Priority-")
                    for bug in bugs:
                        if bug.to_dict()["priority"] == "HIGH":
                            print(bug.to_dict())
                    # then medium
                    print("-Medium Priority-")
                    for bug in bugs:
                        if bug.to_dict()["priority"] == "MEDIUM":
                            print(bug.to_dict())
                    # then low
                    print("-Low Priority-")
                    for bug in bugs:
                        if bug.to_dict()["priority"] == "LOW":
                             print(bug.to_dict())

                elif ListChoice == "3":#print in alphabetical order
                    BugsAlphabetical=sorted(bugs, key=lambda bug: bug.title.lower())#orders list of bugs
                    for bug in BugsAlphabetical:
                        print(bug.to_dict())


            elif choice == "2":
                mode = input(
                    "Search mode (id / title / status / priority / person): "
                ).strip().lower()

                # noramal search
                if mode != "person":
                    query = input("Search query: ").strip()
                    bugs = bug_controller.get_all(mode, query)

                    for bug in bugs:
                        print(bug.to_dict())

                # ppl search (story 21)
                else:
                    print("\nPerson search:")
                    print("1. assigned_to")
                    print("2. created_by")

                    sub_choice = input("Choose search type: ").strip()

                    staff = input("Enter staff username: ").strip()

                    query = {
                        "created_by": None,
                        "assigned_to": None,
                        "include_unassigned": False,
                        "exclude_closed": False,
                        "same_person": False,
                        "keyword": None
                    }

                    if sub_choice == "1":
                        query["assigned_to"] = staff

                        include = input(
                            "Include unassigned bugs? (y/n): "
                        ).lower() == "y"
                        query["include_unassigned"] = include

                    elif sub_choice == "2":
                        query["created_by"] = staff


                        exclude = input(
                            "Exclude CLOSED / COMPLETED bugs? (y/n): "
                        ).lower() == "y"
                        query["exclude_closed"] = exclude

                    else:
                        print("Invalid person search option")
                        continue

                    # keywords
                    keyword = input(
                        "Optional keyword (press enter to skip): "
                    ).strip()
                    if keyword:
                        query["keyword"] = keyword

                    bugs = bug_controller.get_all("person", query)

                    if not bugs:
                        print("No bugs found.")
                    else:
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
                    status=status,
                    tester_id=current_user.username 
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
                status = input("New status: ").strip().upper()
                bug = bug_controller.update_status(bug_id, status)
                print("Status updated:", bug.to_dict())

            elif choice == "6":
                bug_id = input("Bug ID: ").strip()
                assigned_to = input("Assign to: ").strip()
                bug = bug_controller.assign(bug_id, assigned_to)
                print("Bug assigned successful")
                print(f"Bug assigned to {bug.assigned_to}")
                print("Bug assigned:", bug.to_dict())


            elif choice == "7":
                bug_id = input("Bug ID: ")
                confirm = input("Are you sure to delete this bug? (y/n): ").lower() == "y"
                deleted = bug_controller.delete(bug_id, confirm)

                if deleted:
                    print(f"Bug {bug_id} deleted successfully.")
                else:
                    print(f"Bug {bug_id} could not be deleted.")

            elif choice == "8":
                print("Logging out...")
                current_user = None
                continue

            elif choice == "9":
                # 1. find out all the closd or completed bugs !
                bugs = bug_controller.get_all()
                closed_bugs = [
                    bug for bug in bugs
                    if bug.status in (BugStatus.CLOSED, BugStatus.COMPLETED)
                ]

                if not closed_bugs:
                    print("No closed or completed bugs available to reopen.")
                    continue

                # 2. list out all the reopen bugs
                print("Which closed / completed bug do you want to reopen?")
                for i, bug in enumerate(closed_bugs):
                    print(f"{i + 1}. {bug.id} | {bug.title} | {bug.status.value}")

                # 3. user choice la
                try:
                    idx = int(input("Choose bug number: ")) - 1
                    selected_bug = closed_bugs[idx]
                except (ValueError, IndexError):
                    print("Invalid selection.")
                    continue

                # 4. enter reopen reason
                reason = input("Enter reopen reason (min 10 characters): ").strip()

                # 5. call controller to survice
                reopened_bug = bug_controller.reopen(
                    bug_id=selected_bug.id,
                    user=current_user.username,
                    reason=reason
                )

                print("Bug reopened successfully:")
                print(reopened_bug.to_dict())


            elif choice == "0":
                print("Exiting...")
                break

        except Exception as e:
            print("Error:", e)


def login(user):
    print("Login Required")

    while True:
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        try:
            user1 = user.login(username, password)
            print(f"Welcome, {user1.username}!")
            return user1

        except Exception as e:
            print(f"Failed to login: {e}")


if __name__ == "__main__":
    main()
