import os
import shutil
import subprocess


def list_all_directories(root_path):
    all_directories = [
        d for d in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, d))
    ]
    return all_directories


def list_virtual_environments(directory):
    virtual_environments = []

    for root, dirs, files in os.walk(directory):
        if any(os.path.isdir(os.path.join(root, "bin")) for d in dirs):
            virtual_environments.append(root)

    return virtual_environments


def list_packages(selected_environment):
    command = [os.path.join(selected_environment, "bin/python"), "-m", "pip", "list"]
    subprocess.run(command)


def install_package(selected_environment, package_name):
    activate_script = os.path.join(selected_environment, "bin/activate")
    activate_command = f"source {activate_script} && pip install {package_name}"

    subprocess.run(activate_command, shell=True, executable="/bin/zsh")


def uninstall_package(selected_environment, package_name):
    command = [
        os.path.join(selected_environment, "bin/pip"),
        "uninstall",
        package_name,
        "-y",
    ]
    subprocess.run(command)


def delete_virtual_environment(directory):
    shutil.rmtree(directory)
    print(f"Virtual environment at '{directory}' deleted successfully.")


if __name__ == "__main__":
    while True:
        root_directory = os.path.expanduser("~")
        all_directories = list_all_directories(root_directory)

        print(f"All directories in '{root_directory}':")
        for i, directory in enumerate(all_directories, start=1):
            print(f"{i}. {directory}")

        selected_index = input(
            "Enter the number of the directory to check virtual environment: "
        )
        selected_index = int(selected_index) - 1

        base_path = os.path.expanduser("~")
        user_input = os.path.join(base_path, all_directories[selected_index])
        os.chdir(user_input)
        directory_path = os.getcwd()

        virtual_environments = list_virtual_environments(directory_path)

        if virtual_environments:
            print("\nAvailable virtual environments:")
            for i, env in enumerate(virtual_environments, start=1):
                print(f"{i}. {os.path.basename(env)}")

            selected_index = input(
                "Enter the number of the virtual environment you want to manage: "
            )
            selected_index = int(selected_index) - 1
            selected_environment = virtual_environments[selected_index]

            # Print files
            print(
                f"\nFiles in the selected virtual environment directory '{selected_environment}':"
            )
            for i, file_name in enumerate(os.listdir(selected_environment), start=1):
                print(f"{i}. {file_name}")

            # Display installed packages
            print("\nInstalled packages in the virtual environment:")
            list_packages(selected_environment)

            # Package management options
            print("\nPackage Management Options:")
            print("1. Install a package")
            print("2. Uninstall a package")
            print("3. Skip")
            print("4. Delete virtual environment")
            print("5. Exit program")
            option = input("Enter the option number: ")

            if option == "1":
                package_name = input("Enter the name of the package to install: ")
                install_package(selected_environment, package_name)
                print(f"Package '{package_name}' installed successfully.")

            elif option == "2":
                package_name = input("Enter the name of the package to uninstall: ")
                uninstall_package(selected_environment, package_name)
                print(f"Package '{package_name}' uninstalled successfully.")

            elif option == "3":
                print("Skipping package management.")

            elif option == "4":
                confirm_delete = input(
                    "Do you want to delete this virtual environment? (yes/no): "
                ).lower()
                if confirm_delete == "yes":
                    delete_virtual_environment(selected_environment)
                    print(
                        f"The virtual environment at '{selected_environment}' has been deleted."
                    )
                else:
                    print(
                        f"The virtual environment at '{selected_environment}' was not deleted."
                    )

            elif option == "5":
                print("Exiting program.")
                break

            else:
                print("Invalid option. Please enter a valid option.")

        else:
            print(
                f"No virtual environments found in the directory '{directory_path}' or its subdirectories."
            )

        another_directory = input(
            "Do you want to select another directory? (yes/no): "
        ).lower()
        if another_directory != "yes":
            print("Exiting program.")
            break
