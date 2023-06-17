import pandas as pd
from icici_chat2 import inputdata
import time
# df = pd.read_excel("5.xlsx")
df = pd.read_csv("5.csv")
output_df = pd.DataFrame(columns=["Question", "Response"])

# Process each question and store the result in the output DataFrame
for index, row in df.iterrows():
    question = row["question"]
    response = inputdata(question)
    time.sleep(6)
    output_df = output_df.append({"Question": question, "Response": response}, ignore_index=True)

# Write the output DataFrame to a CSV file
output_csv = "responses.csv"
output_df.to_csv(output_csv, index=False)

print("Responses have been written to", output_csv)


    