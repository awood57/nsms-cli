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
LOGGER_PATH = os.path.join(CORE_DIR, "logger.sh")
TOOL_DIR = os.path.join(CORE_DIR, "network_tools.sh")


def log_message(message, level="INFO"):
    subprocess.run(["bash", LOGGER_PATH, "log_message", message, level])


def main_menu():
    while True:
        os.system("clear")
        print("═══════════════════════════════════════════")
        print(f"      {BLUE}Network Testing     {NC}      ")
        print("═══════════════════════════════════════════")
        print(
            f"""{YELLOW}1) Show network interfaces
2) Run ping test
3) Show open ports and active connections
4) Run traceroute
5) Check DNS
6) Show Routing Table
8) Exit{NC}"""
        )
        choice = input("Enter your choice [1-7]: ")  # nosec B322

        log_message(f"User selected menu option: {choice}")

        if choice == "1":
            subprocess.run(["bash", TOOL_DIR, "show_network_interfaces"])
        elif choice == "2":
            subprocess.run(["bash", TOOL_DIR, "run_ping_test"])
        elif choice == "3":
            subprocess.run(["bash", TOOL_DIR, "show_open_ports"])
        elif choice == "4":
            subprocess.run(["bash", TOOL_DIR, "run_traceroute"])
        elif choice == "5":
            subprocess.run(["bash", TOOL_DIR, "check_dns"])
        elif choice == "6":
            subprocess.run(["bash", TOOL_DIR, "show_routing_table"])
        elif choice == "7":
            log_message("Exiting Suricata Management CLI", "INFO")
            break
        else:
            print(f"{RED}Invalid choice. Please select a valid option.{NC}")
            time.sleep(1)


if __name__ == "__main__":
    main_menu()
