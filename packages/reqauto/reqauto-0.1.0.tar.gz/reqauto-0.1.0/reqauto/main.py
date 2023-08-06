import os
import sys
import subprocess
import pkg_resources

def generate_requirements():
    installed_packages = [d for d in pkg_resources.working_set]
    with open("requirements.txt", "w") as req_file:
        for package in installed_packages:
            req_file.write(f"{package.project_name}=={package.version}\n")
    print("Generated requirements.txt successfully.")

def install_requirements():
    if os.path.isfile("requirements.txt"):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        print("requirements.txt not found.")

def main():
    generate_requirements()
    install_requirements()

if __name__ == "__main__":
    main()
