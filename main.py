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


def fetch_recipients(path):
    sender = []     # Saving sender here.
    dataset = {}    # Saving recipients here with the number of mails. Key:Value = 'recipient':'count'.

    try:
        # Listing subfolders in users folder.
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
                                                print("Error in file formatting.\nFile: {}\n Line: {}".format(path2, line))
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

    return dataset, sender  # Return the dataset and sender


def main():
    # Check if '/maildir' path exists.
    path = os.path.dirname(os.path.realpath(__file__)) + "/maildir"
    if os.path.exists(path):    # Path OK.
        print("Path OK.\nStarting data management.")

        # Initialize csv file.
        try:
            # Generate a csv file and initialize it with the first row.
            with open('emails_sent_totals.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Sender", "Recipient", "Count"])
        except IOError as e:
            print("Error in writing file.")
            print(e)

        # Finging different user paths.
        paths = find_paths(path)
        # Fetching recipient data
        dataset, sender = fetch_recipients(paths[0])
        print(dataset) #test prints
        print(sender)

        sys.exit()

    else:   # Path not found - exiting program.
        print("Path does not exist.\nProgram ends.")
        sys.exit()

if __name__ == '__main__':
    main()