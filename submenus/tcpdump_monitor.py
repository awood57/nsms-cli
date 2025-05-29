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
TOOL_DIR = os.path.join(CORE_DIR, "tcpdump_tools.sh")
STATUS_PATH = os.path.join(CORE_DIR, "tool_status.sh")
LOGGER_PATH = os.path.join(CORE_DIR, "logger.sh")


def log_message(message, level="INFO"):
    subprocess.run(["bash", LOGGER_PATH, "log_message", message, level])


def main_menu():
    while True:
        colour_map = {"AVAILABLE": GREEN, "NOT INSTALLED": YELLOW}

        tcpdump_tool = subprocess.run(
            ["bash", STATUS_PATH, "tcpdump"], capture_output=True, text=True
        )
        tcpdump_status = tcpdump_tool.stdout.strip()
        tcpdump_colour = colour_map.get(tcpdump_status, NC)

        os.system("clear")
        print("═══════════════════════════════════════════")
        print(f"      {BLUE}Network Traffic Monitoring     {NC}      ")
        print("═══════════════════════════════════════════")
        print(f"  tcpdump status: {tcpdump_colour}{tcpdump_status}{NC}")
        print("═══════════════════════════════════════════")

        print(
            f"""{YELLOW}1) List available network interfaces
2) Capture live traffic
3) Save traffic to PCAP file
4) Show tcpdump help
5) Exit{NC}"""
        )
        choice = input("Enter your choice [1-4]: ")

        log_message(f"User selected menu option: {choice}")

        if choice == "1":
            subprocess.run(["bash", TOOL_DIR, "list_interfaces"])
            input(f"{YELLOW}Press Enter to continue...{NC}")
        elif choice == "2":
            subprocess.run(["bash", TOOL_DIR, "live_capture"])
        elif choice == "3":
            subprocess.run(["bash", TOOL_DIR, "live_pcap_capture"])
        elif choice == "4":
            subprocess.run(["bash", TOOL_DIR, "show_tcpdump_help"])
        elif choice == "5":
            log_message("Exiting tcpdump_monitor CLI")
            break
        else:
            print(f"{RED}Invalid choice. Please select a valid option.{NC}")
            time.sleep(1)


if __name__ == "__main__":
    main_menu()
