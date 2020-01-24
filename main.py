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
                        print(path2) #test print
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

        sys.exit()

    else:   # Path not found - exiting program.
        print("Path does not exist.\nProgram ends.")
        sys.exit()

if __name__ == '__main__':
    main()