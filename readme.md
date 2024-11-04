# PyHub Project

PyHub integrates a **Flask backend** with an **Electron frontend** to create a seamless, cross-platform application that works both in-browser and as a desktop app. This setup allows you to leverage the power of Python for backend processing and JavaScript for a dynamic user interface.

## 🚀 Getting Started

### Prerequisites

Before diving in, ensure you have the following installed:

- **Python 3.x** - for the backend logic
- **Node.js** and **npm** - for managing the Electron application
- **Yarn** (optional) - for faster and reliable dependency management

### Download Python

Here are the updated download links for the latest Python releases as of November 4, 2024:

| **Release Type**   | **Version**     | **Release Date** | **Download Links**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ------------------ | --------------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Latest Release** | Python 3.13.0   | Oct. 7, 2024     | [Installer (64-bit)](https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe), [Installer (32-bit)](https://www.python.org/ftp/python/3.13.0/python-3.13.0.exe), [Installer (ARM64)](https://www.python.org/ftp/python/3.13.0/python-3.13.0-arm64.exe), [Embeddable Package (64-bit)](https://www.python.org/ftp/python/3.13.0/python-3.13.0-embed-amd64.zip), [Embeddable Package (32-bit)](https://www.python.org/ftp/python/3.13.0/python-3.13.0-embed-win32.zip), [Embeddable Package (ARM64)](https://www.python.org/ftp/python/3.13.0/python-3.13.0-embed-arm64.zip)             |
| **Stable Release** | Python 3.12.7   | Oct. 1, 2024     | [Installer (64-bit)](https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe), [Installer (32-bit)](https://www.python.org/ftp/python/3.12.7/python-3.12.7.exe), [Installer (ARM64)](https://www.python.org/ftp/python/3.12.7/python-3.12.7-arm64.exe), [Embeddable Package (64-bit)](https://www.python.org/ftp/python/3.12.7/python-3.12.7-embed-amd64.zip), [Embeddable Package (32-bit)](https://www.python.org/ftp/python/3.12.7/python-3.12.7-embed-win32.zip), [Embeddable Package (ARM64)](https://www.python.org/ftp/python/3.12.7/python-3.12.7-embed-arm64.zip)             |
| **Pre-release**    | Python 3.14.0a1 | Oct. 15, 2024    | [Installer (64-bit)](https://www.python.org/ftp/python/3.14.0/python-3.14.0a1-amd64.exe), [Installer (32-bit)](https://www.python.org/ftp/python/3.14.0/python-3.14.0a1.exe), [Installer (ARM64)](https://www.python.org/ftp/python/3.14.0/python-3.14.0a1-arm64.exe), [Embeddable Package (64-bit)](https://www.python.org/ftp/python/3.14.0/python-3.14.0a1-embed-amd64.zip), [Embeddable Package (32-bit)](https://www.python.org/ftp/python/3.14.0/python-3.14.0a1-embed-win32.zip), [Embeddable Package (ARM64)](https://www.python.org/ftp/python/3.14.0/python-3.14.0a1-embed-arm64.zip) |

For macOS users:

| **Release Type**   | **Version**     | **Release Date** | **Download Links**                                                                                           |
| ------------------ | --------------- | ---------------- | ------------------------------------------------------------------------------------------------------------ |
| **Latest Release** | Python 3.13.0   | Oct. 7, 2024     | [macOS 64-bit universal2 installer](https://www.python.org/ftp/python/3.13.0/python-3.13.0-macosx10.9.pkg)   |
| **Stable Release** | Python 3.12.7   | Oct. 1, 2024     | [macOS 64-bit universal2 installer](https://www.python.org/ftp/python/3.12.7/python-3.12.7-macosx10.9.pkg)   |
| **Pre-release**    | Python 3.14.0a1 | Oct. 15, 2024    | [macOS 64-bit universal2 installer](https://www.python.org/ftp/python/3.14.0/python-3.14.0a1-macosx10.9.pkg) |

For Linux/UNIX users, it's recommended to install Python using your distribution's package manager.

**Package Manager Commands:**

| **Package Manager**     | **Command**                                   |
| ----------------------- | --------------------------------------------- |
| **winget**              | `winget install Python.Python.3`              |
| **Homebrew (macOS)**    | `brew install python`                         |
| **apt (Debian/Ubuntu)** | `sudo apt update && sudo apt install python3` |
| **pacman (Arch Linux)** | `sudo pacman -S python`                       |

For detailed installation guides and more information, visit the [official Python downloads page](https://www.python.org/downloads/).

### Installation Guides

| **Tool**            | **Installation Guide**                                                                                                           |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **Python**          | [Download and install the latest version of Python](https://www.python.org/downloads/).                                          |
| **pip**             | [Install pip, the Python package manager](https://pip.pypa.io/en/stable/installation/).                                          |
| **Node.js & npm**   | [Install Node.js and npm](https://nodejs.org/en/download/package-manager).                                                       |
| **Yarn** (Optional) | [Install Yarn for a smoother dependency management experience](https://classic.yarnpkg.com/lang/en/docs/install/#debian-stable). |

## 📦 Installation

### Backend (Flask) Setup

1. Clone the repository and navigate to the project directory.
   ```sh
   git clone https://github.com/rxElectron/PyHub.git
   cd pyhub
   ```
2. Install the required Python dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Frontend (Electron) Setup

1. Navigate to the `electron_app` directory:
   ```sh
   cd electron_app
   ```
2. Install the necessary Electron dependencies:
   ```sh
   npm install
   # or
   yarn install
   ```

## ▶️ Running the Project

### Step 1: Start the Flask Backend

Run the Flask server by executing:

```sh
python app.py
```

### Step 2: Choose Your Interface

Once the backend is running, you have two options for the frontend:

- **Browser Mode**: Open your browser and navigate to the URL shown in the terminal.
- **Electron App Mode**: Run the Electron app by selecting "Yes" when prompted in the dialog or by executing the start command within the `electron_app` directory:
  ```sh
  npm start
  # or
  yarn start
  ```

## 🌟 Project Features

- **🖥 Flask Backend**: Handles REST API endpoints, data processing, and template serving.
- **💻 Electron Frontend**: Wraps the web application in a desktop environment, providing access to native features.
- **📦 Modular Architecture**: Each feature, such as debugging and exploring, has its own dedicated route and component, making the app more maintainable and scalable.

## 🛠 Debugging Tools

The **Debug Module** helps you troubleshoot issues effectively, offering:

- **Logging & Error Tracking**: View application logs and errors.
- **Performance Profiling**: Analyze performance bottlenecks.
- **Variable Inspection & Breakpoint Management**: Dive into variable values and control the flow.

To access these features, simply navigate to the **Debug** section within the app interface.

## 🙌 Acknowledgements

Thanks to all the contributors and open-source libraries that made this project possible. Special shoutout to the developers of **Flask** and **Electron** for enabling rapid cross-platform development!

## 📑 Node Management Setup

To manage Node.js versions, you can use **nvm** (Node Version Manager) or **fnm** (Fast Node Manager). Below are instructions for setting up both tools on different systems.

1. Install **nvm** (Node Version Manager):
   ```sh
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
   ```
2. Download and install Node.js (you may need to restart the terminal):
   ```sh
   nvm install 22
   ```
3. Verify the installed Node.js and npm versions:
   ```sh
   node -v # should print `v22.11.0`
   npm -v  # should print `10.9.0`
   ```

#### Linux/macOS

1. Install **fnm**:
   ```sh
   curl -fsSL https://fnm.vercel.app/install | bash
   ```
2. Activate **fnm**:
   ```sh
   source ~/.bashrc
   ```
3. Download and install Node.js:
   ```sh
   fnm use --install-if-missing 22
   ```
4. Verify the installed Node.js and npm versions:
   ```sh
   node -v # should print `v22.11.0`
   npm -v  # should print `10.9.0`
   ```

#### Windows

1. Install **fnm** via **winget**:
   ```sh
   winget install Schniz.fnm
   ```
2. Configure **fnm** environment:
   ```sh
   fnm env --use-on-cd | Out-String | Invoke-Expression
   ```
3. Download and install Node.js:
   ```sh
   fnm use --install-if-missing 22
   ```
4. Verify the installed Node.js and npm versions:
   ```sh
   node -v # should print `v22.11.0`
   npm -v  # should print `10.9.0`
   ```

## 🧶 Yarn Setup

Before using Yarn, ensure it is installed on your system. There are multiple ways to install Yarn:

The recommended way to install Yarn is through npm:

```sh
npm install --global yarn
```

| **Operating System** | **Installation Method**                                                                                                                           |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Arch Linux**       | `pacman -S yarn`                                                                                                                                  |
| **Windows**          | Use **Chocolatey** (`choco install yarn`), **Scoop** (`scoop install yarn`), or [download the installer](https://classic.yarnpkg.com/latest.msi). |
| **macOS**            | Use **Homebrew** (`brew install yarn`), **MacPorts** (`sudo port install yarn`), or [installation script](https://yarnpkg.com/install.sh).        |

### Verify Yarn Installation

To verify if Yarn is installed correctly, run:

```sh
yarn --version
```

If Yarn is not found in your PATH, add the following to your profile (e.g., `.bashrc`, `.zshrc`):

```sh
export PATH="$PATH:/opt/yarn-[version]/bin"
```

For Fish shell users:

```sh
set -U fish_user_paths (yarn global bin) $fish_user_paths
```

## 🐍 Installing pip in Python Environment

If your Python environment does not have **pip** installed, you can use one of the following methods:

- **Linux/macOS**:
  ```sh
  python -m ensurepip --upgrade
  ```
- **Windows**:
  ```sh
  py -m ensurepip --upgrade
  ```

1. Download the script from [get-pip.py](https://bootstrap.pypa.io/get-pip.py).
2. Run the script in the terminal:
   - **Windows**:
     ```sh
     py get-pip.py
     ```

### Upgrading pip

To upgrade pip, run:

```sh
python -m pip install --upgrade pip
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

