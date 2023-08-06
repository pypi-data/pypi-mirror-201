import json
import csv
def polish_file(input_file, output_file, exceptions=''):
    if input_file.endswith(".json") and output_file.endswith(".json") or input_file.endswith(".txt") and output_file.endswith(".txt") or input_file.endswith(".csv") and output_file.endswith(".csv"):
        if input_file.endswith('.csv'):
            # Handle CSV files
            with open(input_file, newline='') as csvfile:
                # Create a CSV reader object
                reader = csv.reader(csvfile)
                # Create a new list to hold the cleaned data
                cleaned_data = []
                # Loop through each row in the file
                for row in reader:
                    # Create a new list to hold the cleaned row data
                    cleaned_row = []
                    # Loop through each column in the row
                    for col in row:
                        # Remove impurities, except for those in the exceptions list
                        cleaned_col = ''.join(c for c in col if c.isalpha() or c.isdigit() or c.isspace() or c in exceptions)
                        # Add cleaned column to cleaned row list
                        cleaned_row.append(cleaned_col)
                    # Add cleaned row to cleaned data list
                    cleaned_data.append(cleaned_row)

            # Write cleaned data to output CSV file
            with open(output_file, 'w', newline='') as csvfile:
                # Create a CSV writer object
                writer = csv.writer(csvfile)
                # Write cleaned data to file
                writer.writerows(cleaned_data)
        elif input_file.endswith('.json'):
            # Handle JSON files
            with open(input_file) as json_file:
                # Load JSON data
                data = json.load(json_file)
                # Clean JSON data
                cleaned_data = []
                for item in data:
                    cleaned_item = {}
                    for key, value in item.items():
                        if isinstance(value, str):
                            # Remove impurities, except for those in the exceptions list
                            cleaned_value = ''.join(c for c in value if c.isalpha() or c.isdigit() or c.isspace() or c in exceptions)
                        else:
                            cleaned_value = value
                        cleaned_item[key] = cleaned_value
                    cleaned_data.append(cleaned_item)

            # Write cleaned data to output JSON file
            with open(output_file, 'w') as json_file:
                json.dump(cleaned_data, json_file)
        elif input_file.endswith('.txt'):
            # Handle TXT files
            with open(input_file, 'r') as txt_file:
                # Read TXT data
                data = txt_file.read()
                # Remove impurities, except for those in the exceptions list
                cleaned_data = ''.join(c for c in data if c.isalpha() or c.isdigit() or c.isspace() or c in exceptions)

            # Write cleaned data to output TXT file
            with open(output_file, 'w') as txt_file:
                txt_file.write(cleaned_data)
        else:
            raise Exception("File format not supported")
    else:
        raise Exception("Files submitted not the same type")
# Call the clean_csv() function with input and output file names and an exceptions list

