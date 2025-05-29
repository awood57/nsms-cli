#!/usr/bin/env python3

import os
import subprocess
import sys
import time
import shutil

# Colour codes
CYAN = "\033[0;36m"
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
NC = "\033[0m"

SURICATA_CONFIG_PATH = "/etc/suricata/suricata.yaml"
SURICATA_LOG_PATH = "/var/log/suricata/fast.log"
SURICATA_STATS_PATH = "/var/log/suricata/stats.log"


CORE_DIR = os.path.join(os.path.dirname(__file__), "../../nsms-core/")
TOOL_DIR = os.path.join(CORE_DIR, "suricata_tools.sh")
STATUS_PATH = os.path.join(CORE_DIR, "tool_status.sh")
LOGGER_PATH = os.path.join(CORE_DIR, "logger.sh")


def log_message(message, level="INFO"):
    subprocess.run(["bash", LOGGER_PATH, "log_message", message, level])


def main_menu():
    while True:
        colour_map = {"ONLINE": GREEN, "OFFLINE": RED, "NOT INSTALLED": YELLOW}

        suricata_tool = subprocess.run(
            ["bash", STATUS_PATH, "suricata"], capture_output=True, text=True
        )
        suricata_status = suricata_tool.stdout.strip()
        suricata_colour = colour_map.get(suricata_status, NC)

        os.system("clear")
        print("═══════════════════════════════════════════")
        print(f"      {BLUE}Suricata Management     {NC}      ")
        print("═══════════════════════════════════════════")
        print(f"  Suricata status: {suricata_colour}{suricata_status}{NC}")
        print("═══════════════════════════════════════════")
        print(
            f"""{YELLOW}1) Toggle Suricata
2) View Suricata logs (fast.log)
3) View Suricata stats (stats.log)
4) Edit Suricata config
5) Update Suricata rules
6) Restart Suricata
7) Exit{NC}"""
        )
        choice = input("Enter your choice [1-7]: ")

        log_message(f"User selected menu option: {choice}")

        if choice == "1":
            subprocess.run(["bash", TOOL_DIR, "toggle_suricata"])
        elif choice == "2":
            subprocess.run(["bash", TOOL_DIR, "view_fast_log"])
        elif choice == "3":
            subprocess.run(["bash", TOOL_DIR, "view_stats_log"])
        elif choice == "4":
            subprocess.run(["bash", TOOL_DIR, "edit_config"])
        elif choice == "5":
            subprocess.run(["bash", TOOL_DIR, "update_rules"])
        elif choice == "6":
            subprocess.run(["bash", TOOL_DIR, "restart_suricata"])
        elif choice == "7":
            log_message("Exiting Suricata Management CLI", "INFO")
            break
        else:
            print(f"{RED}Invalid choice. Please select a valid option.{NC}")
            time.sleep(1)


if __name__ == "__main__":
    main_menu()
