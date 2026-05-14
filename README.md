# SSH Login Report

Two scripts that read "/var/log/auth.log" and tell you what's been going on with SSH failed attempts, successful logins, attempts grouped by IP, and a flag for any IP that's tried and failed 3+ times.

### Why two scripts
"grep" got me the answer fast, but I couldn't easily count attempts per IP or flag anything, and the output disappeared the second I closed the terminal.

So I rewrote it in Python. Same job, more useful I used regex to pull IPs out of the log lines, a dictionary to count attempts per IP, a threshold check to flag anything suspicious, and a saved report file so I can actually go back and read it.

Both scripts are here because it shows that I hit a limit with the bash script, then moved on.

- "ssh_report.sh" — bash, quick, prints to terminal
- "ssh_reports.py" — Python, does more, saves a report file

### Running it

Both read "/var/log/auth.log", which only root can read on Ubuntu, so both need "sudo".


- sudo bash ssh_report.sh
- sudo python3 ssh_reports.py


The Python version writes "ssh_report_output.txt" to wherever you run it from.

### Trying it without a real auth.log

"ssh_reports.py" accepts an optional path argument:


python3 ssh_reports.py test_fixtures/sample_auth.log


"sample_output.txt" is the captured output of that exact command with fake IPs and usernames, but the output itself is what the script actually produces. I added this incase anyone wanted to see the code, and be able to use an example without pointing it at anything.

### Next features

- Read rotated logs too 
- Make the "suspicious" threshold a command-line argument 
- Filter by timestamp 

Tested on Ubuntu 26.04 (Resolute Raccoon).

Built as part of my home security lab.
