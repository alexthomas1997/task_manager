# ====Importing libraries====
from datetime import date, datetime


# ====Functions====
def strip_split(arg):  # Used to process user info from files.
    arg = arg.strip()
    arg = arg.split(", ")
    return arg


def task_display(task):
    # Colour indication for 'Task complete?' to aid the user.
    if task[5] == "Yes":
        STATUS_COLOR = GREEN
    else:
        STATUS_COLOR = RED

    print(f'''Task:\t\t\t\t{YELLOW}{task[1]}{END}
Assigned to:\t\t{YELLOW}{task[0]}{END}
Date assigned:\t\t{YELLOW}{task[3]}{END}
Due date:\t\t\t{YELLOW}{task[4]}{END}
Task complete?\t\t{STATUS_COLOR}{task[5]}{END}
Task description:
\t{YELLOW}{task[2]}{END}''')


def overdue_dates(task):
    due_date = datetime.strptime(task[4], "%d %b %Y")
    due_date = due_date.strftime("%Y%m%d")  # formats date as a number

    current_date = datetime.today().strftime("%Y%m%d")

    return due_date, current_date


def file_read(arg):
    with open(f'{arg}.txt', 'r') as file:
        i = file.readlines()
        return i


def task_file_write(tasks):
    with open('tasks.txt', 'w') as task_file:
        for task in tasks:
            task_file.write(task)


def stats_print(stat_list):
    for i in stat_list:
        if len(i) == 1:  # If item is '\n', an empty line is printed.
            print()
        else:  # Prints each line of information with colour added for easy reading.
            i = i.strip("\n")
            i = i.split(":")
            print(f"{END}{i[0]}:{YELLOW}{i[1]}")


def reg_user():
    print("\n──────────────── Register a user ────────────────")

    new_username = input(f"{CYAN}Enter new username: ")

    users = file_read('user')

    # Checks if the username already exists in 'user.txt',
    # and gives the user the option to choose another if it does.
    while True:
        for user in users:
            user = strip_split(user)

            if new_username == user[0]:
                break
        if new_username != user[0]:  # Breaks while loop if the username is not already in 'user.txt'
            break
        new_username = input(f"{RED}That username already exists! {CYAN}Please enter a different one: ")

    new_password = input("\nEnter new password: ")
    password_confirm = input("Confirm new password: ")

    # Checks if both passwords match,
    # then adds the given username and password to 'user.txt'.
    while True:
        if new_password == password_confirm:
            with open('user.txt', 'a') as users:
                users.write(f"\n{new_username}, {new_password}")  # Writes to 'user.txt' in correct format

            print(f"\n{GREEN}New user registered successfully!")
            break

        else:
            new_password = input(f"{RED}Your passwords do not match! {CYAN}Enter new password: ")
            password_confirm = input("Confirm new password: ")


def gen_report():
    # ====Read files====
    tasks = file_read('tasks')

    users = file_read('user')

    # ====Write 'tasks overview'====
    total_tasks = len(tasks)
    complete_tasks = 0
    incomplete_tasks = 0
    overdue_tasks = 0

    for task in tasks:
        if len(task) == 1:
            continue

        else:
            task = strip_split(task)

            # Counts complete and incomplete tasks.
            if task[-1] == "Yes":
                complete_tasks += 1
            elif task[-1] == "No":
                incomplete_tasks += 1

            due_date, current_date = overdue_dates(task)  # Finds the due date and the current date as an integer.

            # Counts overdue tasks.
            if current_date > due_date and task[-1] == "No":  # Ensures only incomplete tasks are counted.
                overdue_tasks += 1

    # Fail-safe to avoid ZeroDivision Error.
    if total_tasks == 0:
        percentage_incomplete_tasks = 0
    else:
        percentage_incomplete_tasks = round((incomplete_tasks / total_tasks) * 100)

    if incomplete_tasks == 0:
        percentage_overdue_tasks = 0
    else:
        percentage_overdue_tasks = round((overdue_tasks / incomplete_tasks) * 100)

    # Writes the information to 'task_overview.txt'.
    with open('task_overview.txt', 'w') as task_overview:
        task_overview.write(f'''\t Total tasks: {total_tasks}
  Complete tasks: {complete_tasks}
Incomplete tasks: {incomplete_tasks}
   Overdue tasks: {overdue_tasks}

Percentage of incomplete tasks: {percentage_incomplete_tasks}%
   Percentage of overdue tasks: {percentage_overdue_tasks}%''')

    # ====Write 'user overview'====
    total_users = len(users)

    # Writes the total users and tasks to 'user_overview.txt', rewriting existing information.
    with open('user_overview.txt', 'w') as user_overview:
        user_overview.write(f'''Total users: {total_users}
Total tasks: {total_tasks}''')

    # Loops through each user to find information on the separate tasks for each user.
    for user in users:

        # Resets 'counts' to 0 for each user.
        user_tasks = 0
        user_completed_tasks = 0
        user_incomplete_tasks = 0
        user_overdue_tasks = 0

        user = strip_split(user)

        for task in tasks:
            task = strip_split(task)

            # Only counts tasks for the user in the current loop.
            if task[0] == user[0]:
                user_tasks += 1

                if task[-1] == "Yes":
                    user_completed_tasks += 1

                elif task[-1] == "No":
                    user_incomplete_tasks += 1

                    due_date, current_date = overdue_dates(task)

                    if current_date > due_date:
                        user_overdue_tasks += 1

        # Fail-safe to avoid ZeroDivision Error.
        if total_tasks == 0:
            percentage_total_tasks = 0
        else:
            percentage_total_tasks = round((user_tasks / total_tasks) * 100)

        if user_tasks == 0:
            percentage_completed_tasks = 0
        else:
            percentage_completed_tasks = round((user_completed_tasks / user_tasks) * 100)

        if user_tasks == 0:
            percentage_incomplete_tasks = 0
        else:
            percentage_incomplete_tasks = round((user_incomplete_tasks / user_tasks) * 100)

        if user_incomplete_tasks == 0:
            percentage_overdue_tasks = 0
        else:
            percentage_overdue_tasks = round((user_overdue_tasks / user_incomplete_tasks) * 100)

        # Writes the information to 'user_overview.txt' for each user.
        with open('user_overview.txt', 'a') as user_overview:
            user_overview.write(f'''\n\nTask overview for {user[0]}:
\tPercentage of total tasks in task manager assigned to user: \t\t{percentage_total_tasks}%

\tTotal tasks assigned to user: \t\t\t\t\t\t\t{user_tasks}
\tPercentage of completed tasks assigned to user: \t\t{percentage_completed_tasks}%
\tPercentage of incomplete tasks assigned to user: \t\t{percentage_incomplete_tasks}%
\tPercentage of overdue tasks assigned to user: \t\t\t{percentage_overdue_tasks}%''')

    print(f"\n{GREEN}Your report has been generated!")


def show_stats():
    print("\n──────────────── Statistics ────────────────")

    gen_report()

    # ====Read files====
    tasks = file_read('task_overview')

    users = file_read('user_overview')

    # ====Output information====
    print(f"\n{END}──────────────── Task Overview ────────────────")
    stats_print(tasks)

    print(f"\n{END}──────────────── User Overview ────────────────")
    stats_print(users)


def add_task():
    print("\n──────────────── Assign a task ────────────────")

    user_assign = input(f"{CYAN}Enter username to assign task to: ")

    users = file_read('user')

    # Fail-safe so that a task cannot be assigned to a user that does not exist.
    while True:
        for user in users:
            user = strip_split(user)

            if user_assign == user[0]:  # Breaks if the entered user is in 'user.txt'.
                break
        if user_assign == user[0]:  # Breaks while loop if user in 'user.txt'.
            break
        user_assign = input(f"{RED}That username does not exist! {CYAN}Please try again: ")

    # Requests information to write to 'tasks.txt'.
    task_assign_name = input(f"{CYAN}Name of task: ")
    task_assign_desc = input(f"{CYAN}Description of task: ")
    task_assign_due = input(f"{CYAN}Enter task due date: ")
    date_today = date.today().strftime("%d %b %Y")

    # writes information to 'tasks.txt' in correct order.
    with open('tasks.txt', 'a') as tasks:
        tasks.write(f"{user_assign}, {task_assign_name}, {task_assign_desc}, {date_today}, {task_assign_due}, No\n")

    print(f"\n{GREEN}The task has been assigned!")


def view_all():
    print("\n──────────────── All tasks ────────────────\n")

    tasks = file_read('tasks')

    # Loops and displays all tasks.
    for task in tasks:
        if len(task) == 1:
            continue

        else:
            task = strip_split(task)

            # Outputs tasks in an easy-to-read format.
            print("────────────────────────────────────────────────────────────────")
            task_display(task)


def view_mine():
    while True:
        print(f"\n{END}──────────────── My tasks ────────────────\n")

        tasks = file_read('tasks')

        task_count_program = 0  # Tracks number of tasks assigned to user.

        for task in tasks:
            if len(task) == 1:
                continue

            else:
                task = strip_split(task)

                # Displays only tasks for the user that is signed in.
                if task[0] == username:
                    print(f"────────────────────────────────[{task_count_program + 1}]────────────────────────────────")
                    task_display(task)
                    task_count_program += 1

        if task_count_program < 1:  # Lets the user know if they have no tasks.
            print(f"{GREEN}You have no tasks!{END}")
            break

        # lets the user select a task to edit or mark as complete.
        else:
            task_select = int(
                input(f"\n{CYAN}Enter a task number to edit it or enter '-1' to exit to the main menu:{END} "))

            # Selects the appropriate task as long as it is incomplete, and displays appropriate message if it is complete.
            while True:
                if task_select == -1:  # Exits to main menu.
                    break

                task_count_program = 0  # Tracks tasks assigned to the user.
                for task in tasks:
                    task = strip_split(task)

                    if task[0] == username:
                        task_count_program += 1

                # Ensures only a valid task number can be entered.
                if task_select < 1 or task_select > task_count_program:
                    task_select = int(input(f"{RED}Task not found! {CYAN}Try a different number:{END} "))
                    continue

                task_count_program = 0  # Tracks tasks assigned to the user.
                for task in tasks:
                    task = strip_split(task)

                    if task[0] == username:
                        if task_count_program + 1 == task_select:
                            if task[-1] == "No":  # Ensures only incomplete tasks can be edited.
                                print(f"\n────────────────────────────────"
                                      f"[{YELLOW}Edit task {task_count_program + 1}{END}]"
                                      f"────────────────────────────────")
                                task_display(task)
                                break
                            else:
                                task_select = int(input(f"{RED}Sorry, You can only edit tasks that have not yet "
                                                        f"been completed! {CYAN}Please enter a different number:{END} "))
                                break

                        task_count_program += 1

                if task[0] == username and task[-1] == "Yes":
                    continue

                if task[0] == username:
                    break

                if task[-1] == "No":  # Breaks out of while loop.
                    break

            if task_select == -1:  # Exits to main menu.
                break

            task_complete = input(f"\n{CYAN}Would you like to mark this task as complete? (Yes/No): ").lower()

            # Marks task as complete.
            if task_complete == "yes":
                tasks = file_read('tasks')

                task_count_file = -1  # Tracks total tasks in 'tasks.txt' so that rewritten task is on the correct line.
                task_count_program = 0

                for task in tasks:
                    task = strip_split(task)
                    task_count_file += 1

                    if task[0] == username:
                        task_count_program += 1
                        if task_count_program == task_select:
                            task[-1] = "Yes\n"

                            tasks[task_count_file] = ", ".join(task)

                task_file_write(tasks)

                print(f"\n{GREEN}Task updated successfully!\n")

            # Gives user the option to edit the task.
            else:
                task_edit = input(f"Would you like to edit the task? (Yes/No): ").lower()

                if task_edit == "yes":
                    new_user_assign = input("Enter username to assign task to: ")

                    users = file_read('user')

                    # Checks that the user exists in 'user.txt'.
                    while True:
                        for user in users:
                            user = strip_split(user)

                            if new_user_assign == user[0]:  # Breaks if the entered user is in 'user.txt'.
                                break
                        if new_user_assign == user[0]:  # Breaks while loop if user in 'user.txt'.
                            break
                        new_user_assign = input(f"{RED}That username does not exist! {CYAN}Please try again: ")

                    new_date_assign = input("Enter new due date for the task: ")

                    tasks = file_read('tasks')

                    task_count_file = -1
                    task_count_program = 0

                    # Writes the edited task into the correct position in 'tasks.txt'.
                    for task in tasks:
                        task = task.split(", ")
                        task_count_file += 1

                        if task[0] == username:
                            task_count_program += 1
                            if task_count_program == task_select:  # Ensures correct task is overwritten.
                                task[0] = new_user_assign
                                task[-2] = new_date_assign

                                tasks[task_count_file] = ", ".join(
                                    task)  # Ensures correct line in 'tasks.txt' is overwritten.

                    task_file_write(tasks)

                    print(f"\n{GREEN}Task updated successfully!\n")


# ====Console colours====
CYAN = "\033[0;36m"
YELLOW = "\033[1;33m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
END = "\033[0m"

# ====Login Section====
username = input(f"{CYAN}Enter username: ")

with open('user.txt', 'r') as users:
    users = users.readlines()

# Loops the username request until the username matches a user on the 'user.txt' file.
while True:
    for user in users:
        user = strip_split(user)

        if username == user[0]:
            password = input(f"{CYAN}Enter password: ")

            # Loops password request until input matches the password for that user.
            while True:
                if password == user[1]:  # Breaks password loop.
                    break

                password = input(f"{RED}Password incorrect! {CYAN}please try again: ")

            if username == user[0]:  # Breaks username loop.
                break
    if username == user[0]:  # Breaks original while loop.
        break

    username = input(f"{RED}No user by that username! {CYAN}Please try again: ")

while True:
    # Presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    print(f"\n{END}──────────────── Menu ────────────────")

    # ====Admin menu====
    if username == "admin":
        menu = input('''Select one of the following Options below:
r - Register a user
gr - Generate reports
s - Show statistics
a - Adding a task
va - View all tasks
vm - view my task
e - Exit
: ''').lower()

    # ====Other users menu====
    else:
        menu = input('''Select one of the following Options below:
a - Adding a task
va - View all tasks
vm - view my task
e - Exit
: ''').lower()

    # ====Registering a user (admin)====
    if menu == 'r' and username == "admin":
        reg_user()

    # ====Registering a user (other)====
    elif menu == 'r':  # Fail-safe incase non 'admin' user selects 'r'.
        print(f"\n{RED}Sorry, only the admin can register a new user!{END}")

    # ====Generate reports====
    elif menu == 'gr' and username == "admin":
        gen_report()

    # ====Generate reports (other)====
    elif menu == 'gr':
        print(f"\n{RED}Sorry, only the admin can generate reports!{END}")

    # ====Show statistics (admin)====
    elif menu == 's' and username == "admin":
        show_stats()

    # ====Show statistics (other)====
    elif menu == 's':  # Fail-safe incase non 'admin' user selects 's'.
        print(f"\n{RED}Sorry, only the admin can access statistics!{END}")

    # ====Adding a task====
    elif menu == 'a':
        add_task()

    # ====View all tasks====
    elif menu == 'va':
        view_all()

    # ====View my tasks====
    elif menu == 'vm':
        view_mine()

    # ====Exit====
    elif menu == 'e':
        print(f'\n{GREEN}Goodbye!!!')
        exit()

    # ====Loops if incorrect letter entered====
    else:
        print(f"{RED}You have made a wrong choice, Please Try again!{END}")
