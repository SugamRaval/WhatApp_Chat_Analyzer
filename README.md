# WhatsApp Chat Analyzer
## Introduction<br>
This project provides a comprehensive analysis of WhatsApp chat data. By leveraging the power of data preprocessing, and visualization tools, it delivers insights into chat activity, user behavior, word frequency, emoji usage, and more. The analysis is presented through an interactive web application built with Streamlit.<br>
## Analysis Performed<br>
### Preprocessing
* <b>Date and Time Conversion:</b> Converts 12-hour formatted timestamps to 24-hour format and extracts relevant date and time components.<br>
* <b>Message Segmentation:</b> Splits raw messages into individual components such as date, user, and message content.<br>
* <b>User and Message Separation:</b> Identifies the sender of each message and handles group notifications separately.<br>
* <b>Feature Extraction:</b> Extracts additional features like year, month, day, hour, minute, and period of the day for time-based analysis.<br>
### Data Analysis
* <b>Basic Statistics:</b> Calculates the total number of messages, words, media files, and links shared.
* <b>User Activity:</b> Identifies the most active users and their participation percentage.
* <b>Word Cloud:</b> Generates a word cloud to visualize the most frequently used words, excluding stop words.
* <b>Common Words:</b> Lists the most common words used in the chat.
* <b>Emoji Analysis:</b> Counts the frequency of emojis used and displays the most common ones.<br>
* <b>Time-Based Analysis:</b><br>
   - <b>Monthly and Daily Timeline:</b> Analyzes message activity over time.
   - <b>Activity Heatmap:</b> Visualizes user activity across different days of the week and periods of the day.
   - <b>Most Active Day and Month:</b> Identifies the most active days of the week and months.
## Setup Instruction
### Prerequisites
   * Python 3.7 or higher
   * Pip (Python package installer)
### Installation
   1. <b>Clone the repository:</b>
   - git clone https://github.com/yourusername/whatsapp-chat-analyzer.git
   - cd whatsapp-chat-analyzer
  2. <b>Create a virtual environment (optional but recommended):</b>
   - python -m venv venv
   - source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
  3. <b>Install the required packages:</b>
   - pip install -r requirements.txt
### Usage<br>
1. <b>Prepare your WhatsApp chat data:</b>
- Export your WhatsApp chat as a .txt file.<br>
2. <b>Run the Streamlit application:</b>
- streamlit run app.py
3. <b>Upload your chat file:</b>
- In the Streamlit sidebar, upload the exported WhatsApp chat .txt file.
- Select the user for analysis (or choose 'Overall' for the entire chat).
4. <b>View the Analysis:</b>
- Click the "Show Analysis" button to generate the insights.
- Explore various statistics, visualizations, and analyses provided by the app.
### File Descriptions
- <b>preprocessing.py:</b> Contains functions for preprocessing the chat data, including date conversion, message segmentation, and feature extraction.
- <b>helper.py:</b> Includes helper functions for performing specific analyses like user activity, word frequency, emoji counting, and time-based analysis.
- <b>app.py:</b> The main Streamlit application script that orchestrates the data preprocessing, analysis, and visualization.
### Contributing
- Contributions are welcome! Please feel free to submit a Pull Request.

