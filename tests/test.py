import pexpect


def test_menu():
    child = pexpect.spawn("python3 nsms-cli.py")
    # Tcpdump
    child.expect("Network Security Monitoring System")
    child.sendline("1")
    child.expect("Network Traffic Monitoring")
    child.sendline("5")
    # Suricata
    child.expect("Network Security Monitoring System")
    child.sendline("2")
    child.expect("Suricata Management")
    child.sendline("7")
    # ufw
    child.expect("Network Security Monitoring System")
    child.sendline("3")
    child.expect("Firewall Management")
    child.sendline("8")
    # fail2ban
    child.expect("Network Security Monitoring System")
    child.sendline("4")
    child.expect("Brute Force Prevention")
    child.sendline("8")
    # Connection Testing
    child.expect("Network Security Monitoring System")
    child.sendline("5")
    child.expect("Network Testing")
    child.sendline("7")
    # System Information
    child.expect("Network Security Monitoring System")
    child.sendline("6")
    child.expect("Gathering system information...")
    child.sendline("\n")
    # Exit
    child.expect("Network Security Monitoring System")
    child.sendline("7")
    child.expect(pexpect.EOF)
