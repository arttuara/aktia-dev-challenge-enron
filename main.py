from tqdm import tqdm
import sys
import os
import csv

# Function for finding all paths for different users.
def find_paths(path):
    paths = []
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

def main():
    # Check if '/maildir' path exists.
    path = os.path.dirname(os.path.realpath(__file__)) + "/maildir"
    if os.path.exists(path):    # Path OK.
        print("Path OK. Starting data management.")

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
        print(paths) #test print

        sys.exit()

    else:   # Path not found - exiting program.
        print("Path does not exist.\nProgram ends.")
        sys.exit()

if __name__ == '__main__':
    main()