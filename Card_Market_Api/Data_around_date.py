import pandas as pd
from datetime import datetime, timedelta

def extract_week_data(input_csv_path, target_date):
    target_date = datetime.strptime(target_date, '%Y-%m-%dT%H:%M:%SZ')

    start_date = target_date - timedelta(days=7)
    end_date = target_date + timedelta(days=7)

    df = pd.read_csv(input_csv_path, sep='\t', header=None, names=['Date', 'Value'])

    df['Date'] = pd.to_datetime(df['Date'])
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    output_csv_path = 'week_data.csv'  # You can change the output file name as needed
    filtered_df.to_csv(output_csv_path, sep='\t', index=False, header=None)

    return output_csv_path

# input_csv_path = 'your_input_data.csv'  # Replace with the path to your input CSV file
# target_date = '2023-09-25T15:07:47Z'    # Replace with your target date
# new_csv_path = extract_week_data(input_csv_path, target_date)
# print(f'New CSV file generated: {new_csv_path}')
