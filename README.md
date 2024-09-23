# WordPress Private Content to CustomGPT AI Agent Builder

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)

A powerful and user-friendly tool to securely sync your private WordPress content to CustomGPT, enabling you to build AI agents with your private/paywalled data.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Features

- 🔒 Secure sync of private WordPress content to CustomGPT
- 🔄 Support for both posts and pages
- 📊 Build AI agents from private, paywalled and logged-in data. 
- 🚀 Detailed citations and sources (for driving subscriptions and accessing paywalled data)
- ✅ Indexing status check and confirmation

![Project Screenshot](screenshot.png)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- A WordPress website with a read-only user with access to private/paywalled content. 
- A CustomGPT account with API access

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/wordpress-to-customgpt.git
   cd wordpress-to-customgpt
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the provided local URL (usually `http://localhost:8501`).

3. Fill in the required fields:
   - WordPress Website URL
   - WordPress Username
   - WordPress Application Password
   - CustomGPT API Key

4. Click "Fetch and Transfer Data" to start the process.

5. Monitor the progress and wait for the confirmation of successful transfer and indexing.

## Configuration

### WordPress Setup

1. Log in to your WordPress admin panel.
2. Navigate to Users > Your Profile.
3. Scroll down to the Application Passwords section.
4. Enter a name for the application password (e.g., "CustomGPT Transfer") and click "Add New Application Password".  [Need Help?](https://make.wordpress.org/core/2020/11/05/application-passwords-integration-guide/)
5. Copy the generated password - you'll need this for the "WordPress Application Password" field in the app.

### CustomGPT Setup

1. Log in to your [CustomGPT account](https://app.customgpt.ai/).
2. Navigate to your profile settings.
3. Find your API key in the [API section](https://app.customgpt.ai/profile#api).
4. Use this API key in the "CustomGPT API Key" field in the app.

## Contributing

Contributions to the WordPress to CustomGPT Data Transfer project are welcome! Here's how you can contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-branch-name`.
5. Create a pull request.

Please make sure to update tests as appropriate and adhere to the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any problems or have any questions, please open an issue in the GitHub repository or contact the maintainers directly.

---

Made with ❤️ by [adorosario](https://github.com/adorosario)