import re
import os
from datetime import datetime

def load_log_file():
    filepath = input("Enter log file path (.txt or.log): ").strip()

    if not os.path.exists(filepath):
        print("Error: File not found")
        return None

    if not filepath.endswith(('.txt', '.log')):
        print("Error: Only.txt and.log files supported")
        return None

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        if not lines:
            print("Error: File is empty")
            return None
        print(f"Loaded {len(lines)} lines successfully")
        return lines
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def analyze_logs(log_lines):
    if not log_lines:
        print("No logs to analyze. Load a file first.")
        return None

    pattern = r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})?\s*\[?(ERROR|WARNING|INFO)\]?'

    counts = {'ERROR': 0, 'WARNING': 0, 'INFO': 0, 'UNKNOWN': 0}
    parsed_logs = []

    for line in log_lines:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            timestamp = match.group(1)
            level = match.group(2).upper()
            counts[level] += 1
            parsed_logs.append({'timestamp': timestamp, 'level': level, 'message': line.strip()})
        else:
            counts['UNKNOWN'] += 1

    return {'counts': counts, 'logs': parsed_logs, 'total': len(log_lines)}

def search_logs(log_data):
    if not log_data:
        print("Load and analyze a file first")
        return

    keyword = input("Enter keyword to search: ").strip()
    if not keyword:
        return

    level_filter = input("Filter by level [ERROR/WARNING/INFO/ALL]: ").strip().upper()
    if level_filter == '':
        level_filter = 'ALL'

    results = []
    for log in log_data['logs']:
        if keyword.lower() in log['message'].lower():
            if level_filter == 'ALL' or log['level'] == level_filter:
                results.append(log)

    print(f"\nFound {len(results)} matching logs:")
    for r in results[:20]: # show max 20
        print(f"[{r['level']}] {r['timestamp'] or 'N/A'} - {r['message'][:100]}")

    if len(results) > 20:
        print(f"... and {len(results) - 20} more")

def generate_report(log_data):
    if not log_data:
        print("Load and analyze a file first")
        return

    counts = log_data['counts']
    total = log_data['total']

    report = f"""Log Analysis Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Total Log Lines: {total}
ERROR Count: {counts['ERROR']}
WARNING Count: {counts['WARNING']}
INFO Count: {counts['INFO']}
UNKNOWN Count: {counts['UNKNOWN']}

Summary:
- Error Rate: {counts['ERROR']/total*100:.2f}%
- Warning Rate: {counts['WARNING']/total*100:.2f}%
- Info Rate: {counts['INFO']/total*100:.2f}%
"""

    filename = input("Save report as [report.txt]: ").strip() or "report.txt"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report saved to {filename}")
    except Exception as e:
        print(f"Error saving report: {e}")

    print("\n" + report)

def main_menu():
    log_data = None
    while True:
        print("\n===== Log Analyzer =====")
        print("1. Load File")
        print("2. Analyze Logs")
        print("3. Search Logs")
        print("4. Generate Report")
        print("5. Exit")

        choice = input("Choose option: ").strip()

        if choice == '1':
            log_lines = load_log_file()
            if log_lines:
                log_data = analyze_logs(log_lines)
        elif choice == '2':
            if log_data:
                print("\nAnalysis Complete:")
                for k, v in log_data['counts'].items():
                    print(f"{k}: {v}")
            else:
                print("Load a file first")
        elif choice == '3':
            search_logs(log_data)
        elif choice == '4':
            generate_report(log_data)
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main_menu()