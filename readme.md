# PyHub Project

This project integrates a **Flask backend** with an **Electron frontend** for a dynamic, cross-platform web and desktop application. The app runs in a browser or as a standalone desktop app using Electron.

## Getting Started

### Prerequisites

- **Python 3.x**
- **Node.js** (for Electron)
- **npm** (for managing Electron dependencies)

### Install Python Dependencies

Install the Flask dependencies:

bash
pip install -r requirements.txt


### Install Electron Dependencies

Navigate to the `electron_app` directory and install dependencies:

bash
cd electron_app
npm install


### Running the Project

1. Start the Flask server:

bash
python app.py


2. You will be prompted to either use the app in a browser or launch the Electron app.

- **For Browser Mode**: Select "No" in the dialog.
- **For App Mode**: Select "Yes" to launch the Electron app.

### Project Features

- **Flask Backend**: Handles the API and serves the templates.
- **Electron Frontend**: Provides a desktop environment for the application.
- **Modular Design**: Each section (debug, explore, etc.) has its own route and template.

### Debug

The debug module provides tools for troubleshooting and analyzing the application. It includes features such as:

- Logging and error tracking
- Performance profiling
- Variable inspection
- Breakpoint management

To access the debug features, navigate to the debug section in the application interface.

