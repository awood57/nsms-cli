#!/usr/bin/env python3

import os
import subprocess
import time

# Colour Codes
CYAN = "\033[0;36m"
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
NC = "\033[0m"

# Tool directories
CORE_DIR = os.path.join(os.path.dirname(__file__), "../../nsms-core/")
TOOL_DIR = os.path.join(CORE_DIR, "ufw_tools.sh")
STATUS_PATH = os.path.join(CORE_DIR, "tool_status.sh")
LOGGER_PATH = os.path.join(CORE_DIR, "logger.sh")


def log_message(message, level):
    subprocess.run(["bash", LOGGER_PATH, "log_message", message, level])


# Check SESSION_ID
SESSION_ID = os.getenv("SESSION_ID")
STANDALONE = False
if not SESSION_ID:
    STANDALONE = True
else:
    log_message(
            f"ufw_manager started with existing session ID: {SESSION_ID}",
            "INFO"
            )


def run_command(command):
    try:
        output = subprocess.check_output(
            command, stderr=subprocess.STDOUT, shell=True, text=True
        )
        return output
    except subprocess.CalledProcessError as e:
        return e.output


def log_session_start():
    subprocess.run(["bash", LOGGER_PATH, "log_session_start"])


def main_menu():
    while True:
        colour_map = {"ONLINE": GREEN, "OFFLINE": RED, "NOT INSTALLED": YELLOW}

        ufw_tool = subprocess.run(
            ["bash", STATUS_PATH, "ufw"], capture_output=True, text=True
        )
        ufw_status = ufw_tool.stdout.strip()
        ufw_colour = colour_map.get(ufw_status, NC)

        os.system("clear")
        print("═══════════════════════════════════════════")
        print(f"      {BLUE}Firewall Management     {NC}      ")
        print("═══════════════════════════════════════════")
        print(f" Firewall Status: {ufw_colour}{ufw_status}{NC}")
        print("═══════════════════════════════════════════")

        print(
            f"""{YELLOW}1) Toggle Firewall
2) View Current Rules
3) Add a new rule
4) Delete a rule
5) Edit rules manually
6) Reset firewall
7) Show logs
8) Exit{NC}"""
        )
        choice = input("Enter your choice [1-8]: ")

        log_message(f"User selected menu option: {choice}", "INFO")

        if choice == "1":
            subprocess.run(["bash", TOOL_DIR, "toggle_firewall"])
        elif choice == "2":
            subprocess.run(["bash", TOOL_DIR, "view_rules"])
            input(f"{YELLOW}Press Enter to continue...{NC}")
        elif choice == "3":
            subprocess.run(["bash", TOOL_DIR, "add_new_rule"])
        elif choice == "4":
            subprocess.run(["bash", TOOL_DIR, "delete_rule"])
        elif choice == "5":
            subprocess.run(["bash", TOOL_DIR, "edit_rules"])
        elif choice == "6":
            subprocess.run(["bash", TOOL_DIR, "reset_firewall"])
        elif choice == "7":
            subprocess.run(["bash", TOOL_DIR, "show_logs"])
            input(f"{YELLOW}Press Enter to continue...{NC}")
        elif choice == "8":
            log_message("Exiting ufw_manager CLI", "INFO")
            break
        else:
            print(f"{RED}Invalid choice. Please select a valid option.{NC}")
            time.sleep(1)


if __name__ == "__main__":
    main_menu()
