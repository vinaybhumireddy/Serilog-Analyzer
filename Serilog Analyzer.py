import re
import json

# Sample log line format
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

# Function to generate a summary of the logs
def generate_summary(logs):
    summary = {
        'total_logs': len(logs),
        'levels': {},
        'sources': {},
    }
    for log in logs:
        # Count log levels
        level = log['Level']
        if level not in summary['levels']:
            summary['levels'][level] = 0
        summary['levels'][level] += 1

        # Count source contexts
        source = log['SourceContext']
        if source not in summary['sources']:
            summary['sources'][source] = 0
        summary['sources'][source] += 1

    return summary

# Example usage
log_file_path = 'path/to/your/logfile.txt'
parsed_logs = analyze_log_file(log_file_path)
summary = generate_summary(parsed_logs)

# Print the summary
print(json.dumps(summary, indent=4))

# Optionally, print parsed logs
for log in parsed_logs:
    print(json.dumps(log, indent=4))
