import pandas as pd

# Read our list of friends from the CSV file
df = pd.read_csv(r"c:\Users\MEET\OneDrive\Desktop\microsoft project\friends.csv")

# Print it out to make sure it worked
print("Here is the data we loaded:")
print(df)