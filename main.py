from tqdm import tqdm
import sys
import os
import csv


# Function for finding all paths for different users.
def find_paths(path):
    paths = []  # Saving all paths here.

    try:
        # Loop through directory and save different paths to 'paths' variable.
        for folder in os.listdir(path):
            if folder.startswith("."):  # Ignore unrelevant files and folders.
                continue
            path1 = path + "/" + folder
            paths.append(path1)
    except IOError as e:
        print("An error ocurred in path: {}".format(path))
        print(e)

    return paths    # Return list of paths


# Function for fetching recipients from emails.
def fetch_recipients(path):
    sender = []     # Saving sender here.
    dataset = {}    # Saving recipients here with the number of mails. Key:Value = 'recipient':'count'.

    try:
        # Listing subfolders in 'maildir' folder.
        for subfolders in os.listdir(path):
            # Search folders 'sent' or 'sent_items' and pass them forward.
            if subfolders == "sent" or subfolders == "sent_items":
                path1 = path + "/" + subfolders
                try:
                    # Go through files in the folders and filter data.
                    for files in os.listdir(path1):
                        path2 = path1 + "/" + files
                        try:
                            # Open file and start going through lines.
                            data = open(path2,'r')
                            try:
                                # Get the sender from the data. We only need the sender once so we don't need to extract it several times.
                                if sender == []:
                                    for line in data:
                                        line = line.rstrip()    # Clean the line.
                                        line = line.lower()     # Setting the line to lowecase.
                                        # If line starts with 'from:' we pick the line and take the senders email.
                                        if line.startswith("from:"):
                                            try:
                                                a,b = line.split()  # Splitting the line to a = 'to:' and b = 'sender'. The variable 'a' is not needed. This also checks typos (whitespace) in emails. 
                                                b = b.rstrip()      # Clean the email address.
                                                sender.append(b)    # Add sender to the 'sender' variable.
                                                break               # Break from the loop once sender is added.
                                            except ValueError as e:
                                                print("Error in file formatting.\nFile: {}\nLine: {}".format(path2, line))
                                                print(e)
                                # Getting the recipients from emails. 
                                for line in data:
                                    line = line.rstrip()    # Clean the line.
                                    line = line.lower()     # Setting to lowercase.
                                    # Getting the recipients from 'to:', 'cc:' and 'bcc:' lines.
                                    if line.startswith("to:") or line.startswith("cc:") or line.startswith("bcc:"):
                                        l = line.split()    # Splitting the recipients.
                                        l.pop(0)            # Removing the 'to:', 'cc:' or 'bcc:' from the beginning.
                                        # Iterating through the recipients list.
                                        for rec in l:
                                            try:
                                                rec = rec.rstrip()  # Clean the address.
                                                # If the recipient is already in the dataset we add its value by one.
                                                if rec in dataset:
                                                    dataset[rec] += 1
                                                # If the recipient is not in the dataset we set its value to one.
                                                else:
                                                    dataset[rec] = 1
                                            except ValueError as e:
                                                print("Error in file formatting")
                                                print(e)
                                    # When we hit the line that starts with 'x-from' we can stop going through the email.
                                    if line.startswith("x-from"):
                                        break
                            except UnicodeDecodeError as e:
                                print("Error in file: {}".format(path2))
                                print(e)
                        except IOError as e:
                            print("Could not read file: {}".format(path2))
                            print(e)
                except IOError as e:
                    print("An error ocurred in path: {}".format(path1))
                    print(e)
    except IOError as e:
        print("An error ocurred in path: {}".format(path))
        print(e)

    return dataset, sender  # Return the dataset and the sender.


# Funtion for writing recipients to a .csv file.
def recipients_to_csv(sender,data):
    try:
        # Write to the initialized file all the fetched data.
        with open(os.path.dirname(os.path.realpath(__file__)) + '/emails_sent_total.csv', 'a', newline='') as file:
            writer = csv.writer(file)   # Initialize the writer.

            # Iterating through the data and writing it in the csv file.
            for rec in data:
                writer.writerow([sender[0], rec, data[rec]])
    except IOError as e:
        print("Error in writing file")
        print(e)
    return


# Function for fetching emails from inbox.
def fetch_inbox(path):
    employee = []   # Saving employee here.
    dataset = {}    # Saving emails per day here. Key:Value = 'day':'count'.
    pathcopy = path.split('/')      # Taking the shortname of the employee.
    employee.append(pathcopy[-1])   # Saving the shortname of the employee to variable employee.
    paths = []      # Saving all relevant paths here.
    
    try:
        # Listing subfolders in 'maildir' folder.
        for subfolders in os.listdir(path):
            # Search folder 'inbox' and pass it forward.
            if subfolders == "inbox":
                path1 = path + "/" + subfolders
                # Finding all the relevant paths from folders and subfolders.
                for root, dirs, files in os.walk(path1):
                    for name in files:
                        # Adding the correct file paths to 'paths' variable.
                        if name.endswith("."):
                            paths.append(os.path.join(root, name))
                    for name in dirs:
                        # Adding the correct file paths to 'paths' variable.
                        if name.endswith("."):
                            paths.append(os.path.join(root, name))

                # Go through files in the folders and filter data.
                for paths2 in paths:
                    try:
                        # Open file and start going through lines.
                        data = open(paths2,'r')
                        try:
                            # Getting the data from emails. 
                            for line in data:
                                line = line.rstrip()    # Clean the line.
                                line = line.lower()     # Setting to lowercase.
                                # Getting the date from 'date' line.
                                if line.startswith("date:"):
                                    l = line.split()    # Splitting the data.
                                    day = l.pop(1)      # Taking the day of the week from date.
                                    daynum = -1         # Initialize day number.
                                    # Compare the day variable to match any of the dates.
                                    if day.startswith("mon"):
                                        daynum = 0
                                    elif day.startswith("tue"):
                                        daynum = 1
                                    elif day.startswith("wed"):
                                        daynum = 2
                                    elif day.startswith("thu"):
                                        daynum = 3
                                    elif day.startswith("fri"):
                                        daynum = 4
                                    elif day.startswith("sat"):
                                        daynum = 5
                                    elif day.startswith("sun"):
                                        daynum = 6
                                    # If daynum is still -1 raise an error.
                                    if daynum == -1:
                                        raise ValueError("Error in date formatting. File: {}".format(paths2))
                                    # Adding the day to the dataset. If the day is already is in the dataset add its value by one.
                                    # Else set the days value to one.
                                    if daynum in dataset:
                                        dataset[daynum] += 1
                                    else:
                                        dataset[daynum] = 1
                                    # When day added to dataset we break and take the next file.
                                    break
                                # If we do not encounter line that starts with 'date:' before a line that starts with 'x-from:' 
                                # we can assume that the 'date:' line is missing.
                                if line.startswith("x-from"):
                                    raise ValueError("Date missing from file: {}".format(paths2))
                        except UnicodeDecodeError as e:
                            print("Error in file: {}".format(paths2))
                            print(e)
                    except IOError as e:
                        print("Could not read file: {}".format(paths2))
                        print(e)
    except IOError as e:
        print("An error ocurred in path: {}".format(path))
        print(e)

    return dataset, employee    # Return the dataset and the employee.


# Funtion for writing inbox to a .csv file.
def inbox_to_csv(employee, data):
    try:
        # Write to the initialized file all the fetched data.
        with open(os.path.dirname(os.path.realpath(__file__)) + '/emails_sent_average_per_weekday.csv', 'a', newline='') as file:
            writer = csv.writer(file)   # Initialize the writer.

            # Iterating through the data and writing it in the csv file.
            for rec in data:
                writer.writerow([employee[0], rec, data[rec]])
    except IOError as e:
        print("Error in writing file")
        print(e)
    return


# Subfunction for managing the recipients.
def emails_sent_total(path):
    # Initialize 'emails_sent_total.csv' file.
    try:
        # Generate a csv file and initialize it with the first row.
        with open(os.path.dirname(os.path.realpath(__file__)) + '/emails_sent_total.csv', 'w', newline='') as file:
            writer = csv.writer(file)                           # Initialize the writer.
            writer.writerow(["Sender", "Recipient", "Count"])   # Writing the first row.
    except IOError as e:
        print("Error in writing file.")
        print(e)

    # Finging different user paths.
    paths = find_paths(path)
    
    # Iterating through the files with a progress bar.
    for i in tqdm(paths):
        # Fetching recipient data.
        dataset, sender = fetch_recipients(i)
        # Write the data to the csv file. 
        recipients_to_csv(sender,dataset)

    print("Done with emails_sent_total.csv file!")
    return


# Subfunction for managing the employees inbox.
def emails_sent_average_per_weekday(path):
    # Initialize 'emails_sent_average_per_weekday.csv' file.
    try:
        # Generate a csv file and initialize it with the first row.
        with open(os.path.dirname(os.path.realpath(__file__)) + '/emails_sent_average_per_weekday.csv', 'w', newline='') as file:
            writer = csv.writer(file)                                   # Initialize the writer.
            writer.writerow(["Employee", "Day_of_week", "Avg_count"])   # Writing the first row.
    except IOError as e:
        print("Error in writing file.")
        print(e)

    # Finging different user paths.
    paths = find_paths(path)
    
    # Iterating through the files with a progress bar.
    for i in tqdm(paths):
        # Fetching recipient data.
        dataset, employee = fetch_inbox(i)
        # Write the data to the csv file. 
        inbox_to_csv(employee,dataset)

    print("Done with emails_sent_average_per_weekday.csv file!")
    return


# Main function for launcing the program.
def main():
    # Check if '/maildir' path exists in the root.
    path = os.path.dirname(os.path.realpath(__file__)) + "/maildir"
    if os.path.exists(path):    # Path OK.
        print("Path OK.\nStarting data management.")
        # Generate 'emails_sent_total.csv'.
        '''emails_sent_total(path)'''
        # Generate 'emails_sent_average_per_weekday.csv'.
        emails_sent_average_per_weekday(path)
        sys.exit()

    else:   # Path not found - exiting program.
        print("Path does not exist.\nProgram ends.")
        sys.exit()


if __name__ == '__main__':
    main()
