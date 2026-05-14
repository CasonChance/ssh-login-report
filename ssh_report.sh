#!/bin/bash
# name: Cason Chance
# Topic: SSH Login Report Script
# DATE: 2026-05-07

echo "===== SSH LOGIN REPORT ====="
echo ""

echo "--- Failed Login Attempts ---"
sudo grep "Failed password" /var/log/auth.log | grep "sshd-session"

echo ""
echo "--- Successful Logins ---"
sudo grep "Accepted" /var/log/auth.log | grep "sshd-session"

echo ""
echo "--- Summary ---"
echo -n "Total Failed attempts: "
sudo grep "Failed password" /var/log/auth.log |grep "sshd-session" | wc -l

echo -n "Total Successful logins: "
sudo grep "Accepted" /var/log/auth.log |grep "sshd-session" | wc -l

echo ""
echo "===== END OF REPORT ====="

