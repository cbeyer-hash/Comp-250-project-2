#we are building a terminal tool for a security operations center.
# critical alerts skip to the front
# analyst can resolve alerts, undo resolutions doine by mistake, and search for specifics
# brings together functions, recursion, a stack and a queue

from collections import deque

# this is the only global variable
next_Id = 1


# the input validation

def get_int(prompt, low, high):  # each of these are parameters for the argument
    while True:
        try:
            number = int(input(prompt))

            # check here to see input is int
            if low <= number <= high:  # checks to see if the numbers are less or equal to or greater than or equal to, also calls parameters
                return number
            else:
                print("hey pal! enter a number for the alert between", low, "and", high)
        except ValueError:
            print("please enter a number")


def get_text(prompt):
    text = input(prompt)

    while text == "":
        print("hey buddy, this cannot be empty, PUT SOMETHING IN")
        text = input(prompt)

    return text


# next up is to make alerts

def create_alerts(alert_queue, source_ip, description, severity):
    global next_Id

    alert = {"Id": next_Id,
             "source_ip": source_ip,
             "Description": description,
             "Severity": severity}

    # increase id for the next alert
    next_Id += 1

    # criticals go to front
    if severity == 5:
        alert_queue.appendleft(alert)
    else:  # incase it os not critical
        alert_queue.append(alert)
    return alert


# recursive stuff OH BOY

def get_alerts(alerts, target_id, index):
    # the base case is next
    if index >= len(alerts):
        return None

    if alerts[index]["Id"] == target_id:
        return alerts[index]
    # recursive calls to next
    return get_alerts(alerts, target_id, index + 1)


def total_severity(alerts, index):
    # next is the base for is we reach the list's end
    if index >= len(alerts):
        return 0
    # add the severity
    return alerts[index]["Severity"] + total_severity(alerts, index + 1)


# display the alert itself

def display_the_alert(alert):
    print("Alert Id:", alert["Id"])
    print("Alert Description:", alert["Description"])
    print("Alert Severity:", alert["Severity"])
    print("Alert Source IP:", alert["source_ip"])


# now for the options

def add_new_alert(alert_queue):
    source_ip = get_text("Enter Source IP:")
    description = get_text("Enter Alert Description:")
    severity = get_int("Enter Alert Severity(1-5):", 1, 5)

    alert = create_alerts(alert_queue, source_ip, description, severity)
    print("Alert:", alert["Id"], "Was added to the list")


# now to view the next alert, FUN

def view_the_next_one(alert_queue):
    if len(alert_queue) == 0:
        print("No more alerts to display")
    else:
        print("\nNext alert:")
        display_the_alert(alert_queue[0])


# next up is to resolve the next one
def resolution(alert_queue, resolution_stack):
    if len(alert_queue) == 0:
        print("No more alerts to resolve")
    else:
        alert = alert_queue.popleft()
        resolution_stack.append(alert)

        print("Alert Id:", alert["Id"], "has been resolved, your welcome")


# now for undoing previous resolutions

def undo(alert_queue, resolution_stack):
    if len(resolution_stack) == 0:
        print("No more alerts to undo")
    else:
        alert = resolution_stack.pop()

        # next puts alert back at the FRONT

        alert_queue.appendleft(alert)

        print("resolution of alert:", alert["Id"], "was undoed")


# now to view all current alerts
def view_pending(alert_queue):
    if len(alert_queue) == 0:
        print("No more alerts to view")
        return
    print("\nPending alert:")

    # display each one
    for alert in alert_queue:
        display_the_alert(alert)

    alert_list = list(alert_queue)

    severity_total = total_severity(alert_list, 0)

    print("Total severity is", severity_total)

    # to view all the history


def view_history(resolution_stack):
    if len(resolution_stack) == 0:
        print("No more resolutions")
        return
    print("\nHistory:")
    # to work backwards
    index = len(resolution_stack) - 1
    while index >= 0:
        display_the_alert(resolution_stack[index])
        index -= 1


# option 7, SEARCH

def search(alert_queue):
    if len(alert_queue) == 0:
        print("No more alerts to search")
        return
    highest_id = next_Id - 1

    target = get_int("Enter target:", 1, highest_id)

    # convert the queue into regular lists for recursion
    alert_list = list(alert_queue)

    found_alerts = get_alerts(alert_list, target, 0)
    if isinstance(found_alerts, dict): #tried everything in the book but this is what worked.
        print("found alerts")
        display_the_alert(found_alerts)
    else:
        print("\nAlerts not found:")
#samples
def load_samples(alert_queue):
    create_alerts(alert_queue, "10.0.0.5",
                  "Port scan detected", 2)
    create_alerts(alert_queue, "104.40.60.3","Multiple failed logins", 4)

    create_alerts(alert_queue, "10.440.670.653","Ransomeware detected", 5)

#THE ACTUAL F@&#ING PROGRAM

def main():

    alert_queue=deque()

    resolution_stack=[]

    load_samples(alert_queue)

    while True:

        print("\n Welcome to the fuck off alert scanner!:")
        print("1. Add a new alert")
        print("2. View next one")
        print("3. resolve next one")
        print("4. Undo")
        print("5. View all pending")
        print("6. View resolutions")
        print("7. Search alert by id")
        print("8. Exit")
#now for the choices
        choice=get_int("Enter choice:", 1, 8)

        if choice==1:
            add_new_alert(alert_queue)
        elif choice==2:
            view_the_next_one(alert_queue)
        elif choice==3:
            resolution(alert_queue, resolution_stack)
        elif choice==4:
            undo(alert_queue, resolution_stack)
        elif choice==5:
            view_pending(alert_queue)
        elif choice==6:
            view_history(resolution_stack)
        elif choice==7:
            search(alert_queue)
        elif choice==8:
            print("G'DAY YA F@^*ING B#&CH")
            break
main()