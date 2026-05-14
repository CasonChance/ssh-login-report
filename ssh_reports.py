# NAME: Cason Chance
# TOPIC: SSH Login Report - Python Version
# DATE: 2026-05-07
import re
import sys

LOG_FILE = "/var/log/auth.log"
REPORT_FILE = "ssh_report_output.txt"

def read_log(filepath):
    """Opens the log file and returns all lines as a list."""
    try:
        with open(filepath, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"Error: could not find {filepath}")
        return []

def find_failed(lines):
    """Searches log lines for failed password attempts."""
    failed = []
    for line in lines:
        if "Failed password" in line and "sshd-session" in line:
            failed.append(line.strip())
    return failed

def find_accepted(lines):
    """Searches log lines for successful logins."""
    accepted = []
    for line in lines:
        if "Accepted" in line and "sshd-session" in line:
            accepted.append(line.strip())
    return accepted

def count_by_ip(lines):
    """Counts failed attempts per IP address using regex."""
    ip_counts = {}
    for line in lines:
        if "Failed password" in line and "sshd-session" in line:
            match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)
            if match:
                ip = match.group(1)
                if ip in ip_counts:
                    ip_counts[ip] += 1
                else:
                    ip_counts[ip] = 1
    return ip_counts

def flag_suspicious_ips(ip_counts):
    """Flags any IP with 3 or more failed login attempts."""
    suspicious = []
    for ip, count in ip_counts.items():
        if count >= 3:
            suspicious.append((ip, count))
    return suspicious

def save_report(failed, accepted, ip_counts, suspicious):
    """Saves the full report to a text file."""
    with open(REPORT_FILE, "w") as f:
        f.write("--- Failed Login Attempts ---\n")
        for line in failed:
            f.write(line + "\n")
        f.write(f"Total failed attempts: {len(failed)}\n")
        f.write("\n--- Successful Logins ---\n")
        for line in accepted:
            f.write(line + "\n")
        f.write(f"Total successful logins: {len(accepted)}\n")
        f.write("\n--- Failed Attempts by IP ---\n")
        for ip, count in ip_counts.items():
            f.write(f"{ip}: {count} attempt(s)\n")
        f.write("\n--- Suspicious IPs (3+ failed attempts) ---\n")
        if suspicious:
            for ip, count in suspicious:
                f.write(f"FLAGGED: {ip} - {count} failed attempts\n")
        else:
            f.write("No suspicious IPs detected.\n")
    print(f"\nReport saved to {REPORT_FILE}")

def main():
    # If a log path was passed on the command line, use it.
    # Otherwise default to the system auth.log.
    if len(sys.argv) > 1:
        log_path = sys.argv[1]
    else:
        log_path = LOG_FILE

    lines = read_log(log_path)
    print(f"Total lines read: {len(lines)}")
    failed = find_failed(lines)
    print(f"\n--- Failed Login Attempts ---")
    for line in failed:
        print(line)
    print(f"Total failed attempts: {len(failed)}")
    accepted = find_accepted(lines)
    print(f"\n--- Successful Logins ---")
    for line in accepted:
        print(line)
    print(f"Total successful logins: {len(accepted)}")
    print(f"\n--- Failed Attempts by IP ---")
    ip_counts = count_by_ip(lines)
    for ip, count in ip_counts.items():
        print(f"{ip}: {count} attempt(s)")
    suspicious = flag_suspicious_ips(ip_counts)
    print(f"\n--- Suspicious IPs (3+ failed attempts) ---")
    if suspicious:
        for ip, count in suspicious:
            print(f"FLAGGED: {ip} - {count} failed attempts")
    else:
        print("No suspicious IPs detected.")
    save_report(failed, accepted, ip_counts, suspicious)

if __name__ == '__main__':
    main()
