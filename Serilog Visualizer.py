import re
import pandas as pd
import matplotlib.pyplot as plt

# Define the log line format
log_line_format = r'\[(?P<Timestamp>\d{2}:\d{2}:\d{2})\] (?P<Level>\w{3}) \{(?P<RequestedId>.*?)\} (?P<SourceContext>.*?) => (?P<Message>.*?)(?:\n(?P<Exception>.*))?$'

# Function to parse a single log line
def parse_log_line(line):
    match = re.match(log_line_format, line)
    if match:
        return match.groupdict()
    return None

# Function to read and parse the log file
def analyze_log_file(file_path):
    parsed_logs = []
    with open(file_path, 'r') as file:
        for line in file:
            parsed_log = parse_log_line(line)
            if parsed_log:
                parsed_logs.append(parsed_log)
    return parsed_logs

# Function to convert parsed logs to a DataFrame
def logs_to_dataframe(parsed_logs):
    df = pd.DataFrame(parsed_logs)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%H:%M:%S').dt.time
    return df

# Function to visualize the log data
def visualize_logs(df):
    # Distribution of log levels
    level_counts = df['Level'].value_counts()
    plt.figure(figsize=(10, 6))
    level_counts.plot(kind='bar', color='skyblue')
    plt.title('Distribution of Log Levels')
    plt.xlabel('Log Level')
    plt.ylabel('Count')
    plt.show()

    # Log entries over time
    plt.figure(figsize=(10, 6))
    df['Timestamp'].value_counts().sort_index().plot(kind='line', marker='o')
    plt.title('Log Entries Over Time')
    plt.xlabel('Time')
    plt.ylabel('Number of Log Entries')
    plt.show()

# Example usage
log_file_path = 'path/to/your/logfile.txt'
parsed_logs = analyze_log_file(log_file_path)
df = logs_to_dataframe(parsed_logs)
visualize_logs(df)
