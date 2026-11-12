
from app.tools.job_search import search_jobs
from app.tools.job_details import get_job_details
from app.tools.job_shortlist import (
    add_to_shortlist,
    view_shortlist,
    remove_from_shortlist
)


def display_menu():
    print("\n==============================")
    print("        CAREERPILOT")
    print("==============================")
    print("1. Search jobs")
    print("2. View job details")
    print("3. Add job to shortlist")
    print("4. View shortlist")
    print("5. Remove job from shortlist")
    print("6. Exit")


def handle_job_search():
    role = input("Enter job role: ")
    location = input("Enter preferred location: ")

    try:
        results = search_jobs(role, location)

        if not results:
            print("No matching jobs found.")
            return

        print("\nMatching Jobs:")

        for job in results:
            print("------------------------------")
            print(f"Job ID: {job['id']}")
            print(f"Role: {job['role']}")
            print(f"Company: {job['company']}")
            print(f"Location: {job['location']}")
            print(f"Experience: {job['experience']}")
            print(f"Skills: {', '.join(job['skills'])}")
            print(f"Remote: {job['remote']}")

    except ValueError as error:
        print(f"Error: {error}")


def handle_job_details():
    job_id = input("Enter Job ID: ")

    try:
        job = get_job_details(int(job_id))

        print("\nJob Details:")
        print("------------------------------")
        print(f"Job ID: {job['id']}")
        print(f"Role: {job['role']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['location']}")
        print(f"Experience: {job['experience']}")
        print(f"Skills: {', '.join(job['skills'])}")
        print(f"Remote: {job['remote']}")

    except ValueError as error:
        print(f"Error: {error}")


def handle_add_to_shortlist():
    job_id = input("Enter Job ID to shortlist: ")

    try:
        result = add_to_shortlist(int(job_id))
        print(result)

    except ValueError as error:
        print(f"Error: {error}")


def handle_view_shortlist():
    results = view_shortlist()

    if not results:
        print("Your shortlist is empty.")
        return

    print("\nYour Shortlisted Jobs:")

    for job in results:
        print("------------------------------")
        print(f"Job ID: {job['id']}")
        print(f"Role: {job['role']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['location']}")
        print(f"Experience: {job['experience']}")
        print(f"Skills: {', '.join(job['skills'])}")
        print(f"Remote: {job['remote']}")


def handle_remove_from_shortlist():
    job_id = input("Enter Job ID to remove: ")

    try:
        result = remove_from_shortlist(int(job_id))
        print(result)

    except ValueError as error:
        print(f"Error: {error}")


def main():
    while True:
        display_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            handle_job_search()

        elif choice == "2":
            handle_job_details()

        elif choice == "3":
            handle_add_to_shortlist()

        elif choice == "4":
            handle_view_shortlist()

        elif choice == "5":
            handle_remove_from_shortlist()

        elif choice == "6":
            print("Thank you for using CareerPilot!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
