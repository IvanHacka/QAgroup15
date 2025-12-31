from backend.controllers.BugController import BugController
from backend.repo.BugRepo import BugRepo
from backend.services.BugService import BugService

from backend.controllers.UserController import UserController
from backend.services.UserService import UserService

from backend.models.Bug import BugStatus


def print_menu(current_user):
    print("\n=== Bug Tracking System ===")
    print(f"You are currently logged in as {current_user.username}")
    print("1. List all bugs")
    print("2. Search bugs")
    print("3. Create bug")
    print("4. Update bug details")
    print("5. Update bug status")
    print("6. Assign bug")
    print("7. Delete bug")
    print("8. Logout")
    print("9. Reopen bug")
    print("10. Mark bug as duplicate")
    print("11. Comment bug")
    print("0. Exit")


def print_bug_with_creator(bug):
    d = bug.to_dict()
    print(d)
    print("------------------------------")

def main():
    bug_repo = BugRepo()
    bug_service = BugService(bug_repo)
    bug_controller = BugController(bug_service)

    user_service = UserService()
    user_controller = UserController(user_service)

    print("Bug Tracking System started")

    current_user = None

    while True:
        if not current_user:
            current_user = login(user_controller)

        print_menu(current_user)
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":#List Bugs
                print("=========List Bugs=========")
                print("0. List Number of Open & Closed Bugs")
                print("1. List All Bugs(No Order)")
                print("2. List By Priority(Descending)")
                print("3. List in alphabetical order(Title A-Z)")

                ListChoice = input("Choose an option: ").strip()
                bugs = bug_controller.get_all()

                if ListChoice == "0":
                    active_bugs = 0
                    closed_bugs = 0

                    for bug in bugs:
                        if bug.status in (
                            BugStatus.OPEN,
                            BugStatus.IN_PROGRESS,
                            BugStatus.REOPEN
                        ):
                            active_bugs += 1
                        elif bug.status in (
                            BugStatus.CLOSED,
                            BugStatus.COMPLETED
                        ):
                            closed_bugs += 1

                    print("Active Bugs:", active_bugs)
                    print("Closed Bugs:", closed_bugs)

                elif ListChoice == "1":
                    for bug in bugs:
                        print_bug_with_creator(bug)

                elif ListChoice == "2":
                    print("-High Priority-")
                    for bug in bugs:
                        if bug.to_dict()["priority"] == "HIGH":
                            print_bug_with_creator(bug)

                    print("-Medium Priority-")
                    for bug in bugs:
                        if bug.to_dict()["priority"] == "MEDIUM":
                            print_bug_with_creator(bug)

                    print("-Low Priority-")
                    for bug in bugs:
                        if bug.to_dict()["priority"] == "LOW":
                            print_bug_with_creator(bug)

                elif ListChoice == "3":
                    BugsAlphabetical = sorted(bugs, key=lambda bug: bug.title.lower())
                    for bug in BugsAlphabetical:
                        print_bug_with_creator(bug)

            elif choice == "2":
                mode = input(
                    "Search mode (id / title / status / priority / person): "
                ).strip().lower()

                if mode != "person":
                    query = input("Search query: ").strip()
                    bugs = bug_controller.get_all(mode, query)
                    for bug in bugs:
                        print_bug_with_creator(bug)
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
                        query["include_unassigned"] = (
                            input("Include unassigned bugs? (y/n): ").lower() == "y"
                        )
                    elif sub_choice == "2":
                        query["created_by"] = staff
                        query["exclude_closed"] = (
                            input("Exclude CLOSED / COMPLETED bugs? (y/n): ").lower() == "y"
                        )
                    else:
                        print("Invalid person search option")
                        continue

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
                            print_bug_with_creator(bug)

            elif choice == "3":
                bug = bug_controller.create(
                    title=input("Title: "),
                    description=input("Description: "),
                    priority=input("Priority (LOW / MEDIUM / HIGH): ").upper(),
                    status=input("Status (OPEN / IN_PROGRESS / CLOSED): ").upper(),
                    tester_id=current_user.username
                )
                print("Bug created:")
                print_bug_with_creator(bug)

            elif choice == "4":
                bug = bug_controller.update(
                    input("Bug ID: "),
                    input("New title (leave blank to skip): ") or None,
                    input("New description (leave blank to skip): ") or None
                )
                print("Bug updated:")
                print_bug_with_creator(bug)

            elif choice == "5":
                bug = bug_controller.update_status(
                    input("Bug ID: "),
                    input("New status: ").strip().upper()
                )
                print("Status updated:")
                print_bug_with_creator(bug)

            elif choice == "6":
                bug_id = input("Bug ID: ").strip()
                print("1.Change who is assigned(replace currently assigned)")
                print("2.Assign another stuff member(Add to currently assigned)")
                AssignChoice=input("Choose an option: ")

                if AssignChoice == "1":
                    raw_data = input("Assign to: ").strip()
                    assigned_to = [d.strip() for d in raw_data.split(",") if d.strip()]
                    bug = bug_controller.assign(bug_id, assigned_to)
                elif AssignChoice == "2":
                    NewAssignment=input("Please enter the username of the staff you would like to add: ")
                    CurrentBug=bug_controller.get_bug(bug_id)
                    CurrentlyAssigned=CurrentBug.to_dict()["assigned_to"]
                    assigned_to=CurrentlyAssigned+[NewAssignment]
                    bug=bug_controller.assign(bug_id, assigned_to)

                print(type(bug.assigned_to), assigned_to)
                print("Bug assigned successful")
                print("Bug assigned to", ", ".join(bug.assigned_to))
                print("Bug assigned:", bug.to_dict())
                print("Bug assigned:")
                print_bug_with_creator(bug)

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
                bugs = bug_controller.get_all()
                closed_bugs = [
                    bug for bug in bugs
                    if bug.status in (BugStatus.CLOSED, BugStatus.COMPLETED)
                ]

                if not closed_bugs:
                    print("No closed or completed bugs available to reopen.")
                    continue

                print("Which closed / completed bug do you want to reopen?")
                for i, bug in enumerate(closed_bugs):
                    print(f"{i + 1}. {bug.id} | {bug.title} | {bug.status.value}")

                idx = int(input("Choose bug number: ")) - 1
                reason = input("Enter reopen reason (min 10 characters): ").strip()

                reopened_bug = bug_controller.reopen(
                    bug_id=closed_bugs[idx].id,
                    user=current_user.username,
                    reason=reason
                )

                print("Bug reopened successfully:")
                print_bug_with_creator(reopened_bug)

            elif choice == "10":
                bug_id = input("Duplicate Bug ID: ").strip()
                original_id = input("Original Bug ID: ").strip()
                bug = bug_controller.mark_duplicate(bug_id, original_id)
                print("Bug marked as duplicate:", bug.to_dict())


            elif choice == "11":
                bug_id = input("Bug ID: ").strip()
                text = input("Comment: ").strip()

                bug = bug_controller.add_comment(
                    bug_id=bug_id,
                    user=current_user.username,
                    text=text
                )

                print("Comment added successfully.")
                print(bug.to_dict())


            elif choice == "0":
                print("Exiting...")
                break

        except Exception as e:
            print("Error:", e)


def login(user):
    print("Login Required")
    while True:
        try:
            user1 = user.login(
                input("Username: ").strip(),
                input("Password: ").strip()
            )
            print(f"Welcome, {user1.username}!")
            return user1
        except Exception as e:
            print(f"Failed to login: {e}")


if __name__ == "__main__":
    main()
