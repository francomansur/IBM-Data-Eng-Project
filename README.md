# IBM-Data-Eng-Project

## Prerequisites

This project requires **Python 3.11**. Please ensure it is installed before proceeding.

- Download and install Python 3.11 from the [official Python website](https://www.python.org/downloads/).
- To verify your Python version, run the following command in your terminal:

```bash
python --version
```

## Setting Up a Virtual Environment (venv)

Follow these steps to create and configure a virtual environment for the project:

### 1. Create a Virtual Environment
Run the following command in your project directory to create a virtual environment:
```bash
python3.11 -m venv venv
```

### 2. Activate the Virtual Environment

#### On Windows:
```bash
venv\Scripts\activate
```

#### On MacOS/Linux:
```bash
source venv/bin/activate
```

Once activated, your terminal should display the environment name (venv) before the prompt.

### 3. Install Dependencies

After activating the virtual environment, install the required dependencies listed in the `requirements.txt` file by running the following command:

```bash
pip install -r requirements.txt
```

This will ensure all the necessary libraries and packages for the project are installed.

## Execute the Program

To execute the `banks_project.py` script, run the following command:

```bash
python banks_project.py
```

