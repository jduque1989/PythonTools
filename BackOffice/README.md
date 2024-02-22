
# Python Automation Scripts

This repository contains two Python scripts designed to automate web browser interactions using Selenium. These scripts are intended for users looking to automate web tasks such as form submissions, data extraction, and web navigation.

## Scripts Overview

- **commissions.py**: Automates specific web interactions related to commissioning processes. It utilizes Selenium WebDriver for browser automation, handling form submissions, and navigating through web pages.
- **cv3.py**: Aims at automating tasks for CV (Curriculum Vitae) submissions or data extraction from web sources. It includes functionalities for handling timeouts, extracting data using BeautifulSoup, and managing web sessions.

## Dependencies

To run these scripts, you will need Python installed on your system along with the following packages:

- `selenium` for web automation
- `python-dotenv` for environment variable management
- `webdriver_manager` for managing browser driver dependencies
- `beautifulsoup4` for parsing HTML and XML documents (required for `cv3.py`)

You can install these dependencies by running:

```
pip install selenium python-dotenv webdriver-manager beautifulsoup4
```

## Setup

1. Clone this repository to your local machine.
2. Create a `.env` file in the root directory of the project to store your environment variables (e.g., login credentials, API keys) securely.
3. Ensure you have Chrome or any compatible browser installed along with its corresponding WebDriver.

## Running the Scripts

To run the scripts, navigate to the project directory in your terminal and execute:

For `commissions.py`:
```
python commissions.py
```

For `cv3.py`:
```
python cv3.py
```

Make sure to customize any specific variables or parameters within the scripts to fit your use case.

## Contribution

Feel free to fork this repository and submit pull requests to contribute to the development of these automation scripts. Your contributions are highly appreciated!
