
def main():
    print("===================================")
    print("   AUTONOMOUS SEO AGENCY")
    print("===================================")

    employees = [
        "Project Manager",
        "SEO Researcher",
        "Keyword Analyst",
        "Technical SEO Auditor",
        "Content Writer",
        "On-Page SEO Specialist",
        "Competitor Analyst",
        "Performance Analyst"
    ]

    print("\nAgency Employees:")

    for number, employee in enumerate(employees, start=1):
        print(f"{number}. {employee}")

    print("\nAgency system started successfully!")


if __name__ == "__main__":
    main()
