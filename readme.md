# PyHub Project

PyHub integrates a **Flask backend** with an **Electron frontend** to create a seamless, cross-platform application that works both in-browser and as a desktop app. This setup allows you to leverage the power of Python for backend processing and JavaScript for a dynamic user interface.

## 🚀 Getting Started

### Prerequisites

Before diving in, ensure you have the following installed:

- **Python 3.x** - for the backend logic
- **Node.js** and **npm** - for managing the Electron application
- **Yarn** (optional) - for faster and reliable dependency management

### Installation Guides

#### Python
Download and install the latest version of Python from the [official website](https://www.python.org/downloads/).

#### pip
You can install `pip`, the Python package manager, by following [these instructions](https://pip.pypa.io/en/stable/installation/).

#### Node.js and npm
Install Node.js and npm by visiting [Node.js Downloads](https://nodejs.org/en/download/package-manager).

#### Yarn (Optional)
For a smoother dependency management experience, consider installing Yarn. Check out the [Yarn installation guide](https://classic.yarnpkg.com/lang/en/docs/install/#debian-stable).

## 📦 Installation

### Backend (Flask) Setup
1. Clone the repository and navigate to the project directory.
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

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙌 Acknowledgements

Thanks to all the contributors and open-source libraries that made this project possible. Special shoutout to the developers of **Flask** and **Electron** for enabling rapid cross-platform development!

