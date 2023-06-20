import csv
import os
from icici_chat2 import inputdata
def process_csv_with_responses(input_csv_path, output_csv_path, progress_file_path):
    file_exists = os.path.isfile(output_csv_path)

    # Check if progress file exists and retrieve the last processed index
    start_index = 0
    if os.path.exists(progress_file_path):
        with open(progress_file_path, "r") as progress_file:
            start_index = int(progress_file.read().strip())

    # Open the input CSV file
    with open(input_csv_path, "r") as input_file:
        csv_reader = csv.DictReader(input_file)

        # Open the output CSV file in append mode
        with open(output_csv_path, "a", newline="", encoding="utf-8") as output_file:
            fieldnames = ["Question", "Plan_text", "MLAI_GPT_Response"]
            csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            if not file_exists:
                csv_writer.writeheader()

            # Iterate over each row in the input CSV file
            skipped_ans = []
            for i, row in enumerate(csv_reader):
                if i >= start_index:
                    print(row)
                    question = row["ï»¿Question"]
                    plain_text = row["PlainTextAnswer"]
                    print(question)
                    
                    # Process the question and get the response
                    response = inputdata(question)

                    if response is not None:
                        print("Response obtained")
                        csv_writer.writerow(
                            {"Question": str(question), "Plan_text": str(plain_text), "MLAI_GPT_Response": str(response)}
                        )
                        output_file.flush()  # Flush the output file buffer
                        os.fsync(output_file.fileno())  # Ensure the file is written to disk

                        # Update the progress file with the current index
                        with open(progress_file_path, "w") as progress_file:
                            progress_file.write(str(i + 1))
                    else:
                        print("Already got response")
                        skipped_ans.append()
                else:
                    print("Already got response")
                    
    # Close the output file
    output_file.close()

input_csv_path = "FAQ16.csv"
output_csv_path = "ans2.csv"
progress_file_path = "progress.txt"

process_csv_with_responses(input_csv_path, output_csv_path, progress_file_path)