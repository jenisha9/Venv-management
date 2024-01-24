import os
import shutil
import subprocess


def list_all_directories(root_path):
    try:
        all_directories = [
            d
            for d in os.listdir(root_path)
            if os.path.isdir(os.path.join(root_path, d))
        ]
        return all_directories
    except OSError as e:
        print(f"Error listing directories: {e}")
        return []


def list_virtual_environments(directory):
    virtual_environments = [
        root
        for root, dirs, files in os.walk(directory)
        if any(os.path.isdir(os.path.join(root, "bin")) for d in dirs)
    ]
    print("\nAvailable virtual environments:")
    for i, env in enumerate(virtual_environments, start=1):
        print(f"{i}. {os.path.basename(env)}")
    return virtual_environments


def install_package(selected_environment):
    package_name = input("Enter the name of the package to install: ")
    venv_path = os.path.join(selected_environment, "bin", "python")

    bash_check = [venv_path, "-m", "pip", "list"]
    result = subprocess.run(bash_check, capture_output=True, text=True)

    if package_name.lower() in result.stdout.lower():
        print(f"Package '{package_name}' is already installed.")
        return

    try:
        activate_script = [venv_path, "-m", "pip", "install", package_name]
        subprocess.run(activate_script, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error installing package '{package_name}': {e}")
        print(f"The specified package '{package_name}' does not exist or there was an issue during installation.")

    else:
        print(f"Package '{package_name}' installed successfully.\n")
        list_packages(selected_environment)
        
        
def uninstall_package(selected_environment, package_name):
    venv_path = os.path.join(selected_environment, "bin", "python")

    bash_check = [venv_path, "-m", "pip", "list"]
    result = subprocess.run(bash_check, capture_output=True, text=True)

    if package_name.lower() not in result.stdout.lower():
        print(f"Package '{package_name}' is not installed.")
        return

    try:
        command = [venv_path, "-m", "pip", "uninstall", package_name, "-y"]
        subprocess.run(command, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error uninstalling the package {package_name}: {e}")

    else:
        print(f"Package '{package_name}' uninstalled successfully.")

    list_packages(selected_environment)



def delete_virtual_environment(directory):
    confirm_delete = input("Do you want to delete this virtual environment? (yes/no): ").lower()

    if confirm_delete in ["yes", "y", "ye"]:
     try:
         shutil.rmtree(directory)
         print(f"Virtual environment at '{directory}' has been successfully deleted.")
     except Exception as e:
        print(f"Error deleting virtual environment: {e}")

    elif confirm_delete in ["no", "n"]:
       print("Virtual environment will not be deleted.")

    else:
       print("Invalid input. Please enter 'yes' or 'no'.")


def select_directory():
    while True:
        root_directory = os.path.expanduser("~")
        all_directories = list_all_directories(root_directory)

        print(f"All directories in '{root_directory}':")
        for i, directory in enumerate(all_directories, start=1):
            print(f"{i}. {directory}")

        print("0. Exit program")
        selected_index = input(
            "Enter the number of the directory to check virtual environment: "
        )
        selected_index = int(selected_index) - 1

        if selected_index == -1:
            print("Exiting program.")
            return None
        elif 0 <= selected_index < len(all_directories):
            base_path = os.path.expanduser("~")
            return os.path.join(base_path, all_directories[selected_index])
        else:
            print("Invalid input. Please enter a valid number.")


def list_files(selected_environment):
    try:
        print(
            f"\nFiles in the selected virtual environment directory '{selected_environment}':"
        )
        for i, file_name in enumerate(os.listdir(selected_environment), start=1):
            print(f"{i}. {file_name}")
    except FileNotFoundError:
        print(f"Directory not found: '{selected_environment}'")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def list_packages(selected_environment):
    try:
        print("\nInstalled packages in the virtual environment :")
        command = [
            os.path.join(selected_environment, "bin/python"),
            "-m",
            "pip",
            "list",
        ]
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print(f"Python executable not found in: '{selected_environment}'")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def package_management(selected_environment):
    while True:
        print(f"\n You are currently working on '{selected_environment}' \n")
        print("\nPackage Management Options:")
        print("1. Install a package")
        print("2. Uninstall a package")
        print("3. Skip")
        print("4. Delete virtual environment")
        print("5. Exit")
        option = input("Enter the option number: ")

        if option == "1":
            install_package(selected_environment)

        elif option == "2":
            package_name = input("Enter the name of the package to uninstall: ")
            uninstall_package(selected_environment, package_name)

        elif option == "3":
            print("Skipping package management.")
            select_directory()

        elif option == "4":
            delete_virtual_environment(selected_environment)
            break

        elif option == "5":
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please enter a valid option.")


def main():
    while True:
        directory_path = select_directory()

        if directory_path is None:
            break

        while True:
            virtual_environments = list_virtual_environments(directory_path)

            if virtual_environments:
                try:
                    selected_index = input(
                        " \n Enter the number of the virtual environment you want to manage (0 to select another directory):  "
                    )
                    selected_index = int(selected_index) - 1

                    if selected_index == -1:
                     break # Select another directory

                    if 0 <= selected_index < len(virtual_environments):
                        selected_environment = virtual_environments[selected_index]
                        list_files(selected_environment)
                        list_packages(selected_environment)
                        package_management(selected_environment)
                    else:
                        print("Invalid selection. Please enter a valid number.")
                        continue

                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    continue

            else:
                print(
                    f"No virtual environments found in the directory '{directory_path}' or its subdirectories."
                )

            another_directory = input(
                "Do you want to select another directory? (yes/no): "
            ).lower()
            if another_directory != ["yes", "ye", "y"]:
                print("Exiting program.")
                break


if __name__ == "__main__":
    main()
