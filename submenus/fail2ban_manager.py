#!/usr/bin/env python3

import os
import subprocess
import time

# Colour codes
CYAN = "\033[0;36m"
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
NC = "\033[0m"

CORE_DIR = os.path.join(os.path.dirname(__file__), "../../nsms-core/")
TOOL_DIR = os.path.join(CORE_DIR, "fail2ban_tools.sh")
STATUS_PATH = os.path.join(CORE_DIR, "tool_status.sh")
LOGGER_PATH = os.path.join(CORE_DIR, "logger.sh")


def log_message(message, level):
    subprocess.run(["bash", LOGGER_PATH, "log_message", message, level])


def main_menu():
    while True:
        colour_map = {"ONLINE": GREEN, "OFFLINE": RED, "NOT INSTALLED": YELLOW}

        fail2ban_tool = subprocess.run(
            ["bash", STATUS_PATH, "fail2ban"], capture_output=True, text=True
        )
        fail2ban_status = fail2ban_tool.stdout.strip()
        fail2ban_colour = colour_map.get(fail2ban_status, NC)

        os.system("clear")
        print("═══════════════════════════════════════════")
        print(f"      {BLUE}Brute Force Prevention     {NC}      ")
        print("═══════════════════════════════════════════")
        print(f"  fail2ban status: {fail2ban_colour}{fail2ban_status}{NC}")
        print("═══════════════════════════════════════════")
        if RED in fail2ban_status:
            print(f"{RED}fail2ban is not installed.{NC}")
            input(f"{YELLOW}Press Enter to return...{NC}")  # nosec B322
            return

        print(
            f"""{YELLOW}1) Toggle Fail2ban
2) View active jails
3) View fail2ban logs
4) Search logs for IP
5) Unban an IP
6) Edit config
7) Restart fail2ban
8) Exit{NC}"""
        )
        choice = input("Enter your choice [1-8]: ")  # nosec B322

        log_message(f"User selected menu option: {choice}", "INFO")

        if choice == "1":
            subprocess.run(["bash", TOOL_DIR, "toggle_fail2ban"])
        elif choice == "2":
            subprocess.run(["bash", TOOL_DIR, "view_active_jails"])
            input(f"{YELLOW}Press Enter to continue...{NC}")  # nosec B322
        elif choice == "3":
            subprocess.run(["bash", TOOL_DIR, "view_fail2ban_logs"])
            input(f"{YELLOW}Press Enter to continue...{NC}")  # nosec B322
        elif choice == "4":
            ip = input("Enter IP address to search for: ")  # nosec B322
            subprocess.run(["bash", TOOL_DIR, "search_logs_for_ip", ip])
            input(f"{YELLOW}Press Enter to continue...{NC}")  # nosec B322
        elif choice == "5":
            ip = input("Enter IP address to unban: ")  # nosec B322
            subprocess.run(["bash", TOOL_DIR, "unban_ip", ip])
        elif choice == "6":
            subprocess.run(["bash", TOOL_DIR, "edit_fail2ban_config"])
        elif choice == "7":
            subprocess.run(["bash", TOOL_DIR, "restart_fail2ban"])
        elif choice == "8":
            log_message("Exiting Fail2ban CLI", "INFO")
            break
        else:
            print(f"{RED}Invalid choice. Please select a valid option.{NC}")
            time.sleep(1)


if __name__ == "__main__":
    main_menu()
