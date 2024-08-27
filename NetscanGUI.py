import socket
import subprocess
import sys
from tkinter import *
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor
import ctypes

def is_admin():
    """Check if the script is running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def scan_port(ip, port):
    """Scan a single port on the given IP address."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            if result == 0:
                return f"Port {port} is open on {ip}"
            else:
                return None
    except Exception as e:
        return f"Error scanning port {port} on {ip}: {e}"

def scan_ports(ip, start_port, end_port, output_text, max_threads=100):
    """Scan a range of ports on the given IP address."""
    output_text.delete(1.0, END)
    output_text.insert(END, f"Scanning ports {start_port}-{end_port} on {ip}...\n")
    
    open_ports = []
    with ThreadPoolExecutor(max_threads) as executor:
        futures = [executor.submit(scan_port, ip, port) for port in range(start_port, end_port + 1)]
        for future in futures:
            result = future.result()
            if result:
                open_ports.append(result)
    
    if open_ports:
        output_text.insert(END, "Open ports:\n")
        for port_info in open_ports:
            output_text.insert(END, port_info + "\n")
    else:
        output_text.insert(END, f"No open ports found on {ip} in the range {start_port}-{end_port}.\n")

def start_scan():
    ip = ip_entry.get()
    start_port = int(start_port_entry.get())
    end_port = int(end_port_entry.get())
    mac_address = mac_entry.get()
    
    # You can add additional checks for IP, MAC validation here
    
    scan_ports(ip, start_port, end_port, output_text)

def create_gui():
    root = Tk()
    root.title("Network Port Scanner")
    
    # IP Address
    Label(root, text="IP Address:").grid(row=0, column=0, padx=10, pady=5, sticky=W)
    global ip_entry
    ip_entry = Entry(root, width=30)
    ip_entry.grid(row=0, column=1, padx=10, pady=5)

    # MAC Address
    Label(root, text="MAC Address:").grid(row=1, column=0, padx=10, pady=5, sticky=W)
    global mac_entry
    mac_entry = Entry(root, width=30)
    mac_entry.grid(row=1, column=1, padx=10, pady=5)

    # Start Port
    Label(root, text="Start Port:").grid(row=2, column=0, padx=10, pady=5, sticky=W)
    global start_port_entry
    start_port_entry = Entry(root, width=30)
    start_port_entry.grid(row=2, column=1, padx=10, pady=5)

    # End Port
    Label(root, text="End Port:").grid(row=3, column=0, padx=10, pady=5, sticky=W)
    global end_port_entry
    end_port_entry = Entry(root, width=30)
    end_port_entry.grid(row=3, column=1, padx=10, pady=5)
    
    # Scan Button
    scan_button = Button(root, text="Start Scan", command=start_scan)
    scan_button.grid(row=4, column=0, columnspan=2, pady=10)

    # Output Text Box
    global output_text
    output_text = Text(root, height=10, width=60)
    output_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
    
    root.mainloop()

if __name__ == '__main__':
    if is_admin():
        create_gui()
    else:
        # Re-run the program with admin privileges
        if sys.platform == "win32":
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        else:
            subprocess.run(['sudo', sys.executable, __file__])
