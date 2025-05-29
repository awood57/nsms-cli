#!/usr/bin/env python3

import os
import subprocess
import sys
import time

# Colour codes for terminal output
CYAN = "\033[0;36m"
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
NC = "\033[0m"


# Directories/Tool Paths
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CORE_DIR = os.path.join(os.path.dirname(__file__), "../nsms-core/")
BIN_DIR = os.path.join(os.path.dirname(__file__), "submenus")
LOGGER_PATH = os.path.join(CORE_DIR, "logger.sh")
STATUS_PATH = os.path.join(CORE_DIR, "tool_status.sh")


def log_message(message, level):
    subprocess.run(["bash", LOGGER_PATH, "log_message", message, level])


def log_session_start():
    result = subprocess.run(
        ["bash", LOGGER_PATH, "log_session_start"], capture_output=True, text=True
    )
    return result.stdout.strip()


def log_session_end(session_id):
    subprocess.run(["bash", LOGGER_PATH, "log_session_end"])


# Root check
def check_privileges(session_id):
    if os.geteuid() != 0:
        log_message("Script execution attempted without root privileges", "ERROR")
        print(f"{RED}Error: This script requires root privileges.{NC}")
        print(f"{YELLOW}Please run with sudo.{NC}")
        log_session_end(session_id)
        sys.exit(1)
    log_message("Root privilege check passed", "INFO")


# Validate script path
def validate_script(script_path):
    if not os.path.isfile(script_path):
        log_message(f"Required script not found: {script_path}", "ERROR")
        print(f"{RED}Required script not found: {script_path}{NC}")
        input(f"\n{YELLOW}Press Enter to continue...{NC}")
        return False
    return True


# Tool runner
def run_tool(script_name, session_id):
    script_path = os.path.join(BIN_DIR, script_name)
    if validate_script(script_path):
        os.chmod(script_path, 0o755)
        result = subprocess.call(
            [script_path], env=dict(os.environ, SESSION_ID=session_id)
        )
        if result == 0:
            log_message(f"Tool {script_name} completed successfully", "INFO")
        else:
            log_message(
                f"Tool {script_name} failed with return code: {result}", "ERROR"
            )
            input(f"{YELLOW}Press Enter to continue...{NC}")
        return result
    return 1


# System information display
def show_system_info():
    log_message("Displaying system information", "INFO")
    print(f"{CYAN}Gathering system information...{NC}")
    print(f"{BLUE}System Information:{NC}")
    subprocess.call("uname -a", shell=True)

    print(f"\n{BLUE}CPU Information:{NC}")
    subprocess.call("grep 'model name' /proc/cpuinfo | head -n 1", shell=True)

    print(f"\n{BLUE}Memory Usage:{NC}")
    subprocess.call("free -h", shell=True)

    print(f"\n{BLUE}Disk Usage:{NC}")
    subprocess.call("df -h /", shell=True)

    print(f"\n{BLUE}Network Interfaces:{NC}")
    subprocess.call("ip -brief addr", shell=True)

    print(f"\n{BLUE}Listening Ports:{NC}")
    subprocess.call("ss -tuln", shell=True)

    input(f"\n{YELLOW}Press Enter to continue...{NC}")


# Cleanup
def cleanup(session_id):
    log_message("Main CLI interface exiting", "INFO")
    log_session_end(session_id)


def main():
    session_id = log_session_start()
    check_privileges(session_id)

    try:
        while True:
            colour_map = {"ONLINE": GREEN, "OFFLINE": RED, "NOT INSTALLED": YELLOW}

            tools = [
                ("Firewall (UFW)", "ufw"),
                ("Intrusion Detection (Suricata)", "suricata"),
                ("Brute Force Protection (Fail2Ban)", "fail2ban"),
            ]

            tool_status_lines = []

            for label, command in tools:
                result = subprocess.run(
                    ["bash", STATUS_PATH, command], capture_output=True, text=True
                )
                status = result.stdout.strip()
                colour = colour_map.get(status, NC)
                tool_status_lines.append(f" • {label:<35} {colour}{status}{NC}")

                os.system("clear")
                print("══════════════════════════════════════════════════════")
                print(f"         {BLUE}Network Security Monitoring System{NC}")
                print("══════════════════════════════════════════════════════")
                print(f" {CYAN}Security Services Status:{NC}")
                for line in tool_status_lines:
                    print(line)
                print("══════════════════════════════════════════════════════")

            print(f"{YELLOW}1) Packet Sniffing and Analysis (tcpdump){NC}")
            print(f"{YELLOW}2) Intrusion Detection Management (Suricata){NC}")
            print(f"{YELLOW}3) Firewall Management (ufw){NC}")
            print(f"{YELLOW}4) Intrusion Prevention (fail2ban){NC}")
            print(f"{YELLOW}5) Network Connection Monitoring{NC}")
            print(f"{YELLOW}6) System information{NC}")
            print(f"{YELLOW}7) Exit{NC}\n")

            choice = input("Enter your choice [1-7]: ").strip()
            log_message(f"Menu option selected: {choice}", "INFO")

            if choice == "1":
                run_tool("tcpdump_monitor.py", session_id)
            elif choice == "2":
                run_tool("suricata_manager.py", session_id)
            elif choice == "3":
                run_tool("ufw_manager.py", session_id)
            elif choice == "4":
                run_tool("fail2ban_manager.py", session_id)
            elif choice == "5":
                run_tool("view_active_connections.py", session_id)
            elif choice == "6":
                show_system_info()
            elif choice == "7":
                log_message("User requested exit", "INFO")
                print(f"{GREEN}Exiting Network Security Interface{NC}")
                break
            else:
                log_message(f"Invalid menu choice entered: {choice}", "WARNING")
                print(f"{RED}Invalid choice, please try again.{NC}")
                time.sleep(2)
    finally:
        cleanup(session_id)


if __name__ == "__main__":
    main()
