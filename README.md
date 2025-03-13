# AI Alignment Digest Generator

This tool aggregates and summarizes the latest posts from LessWrong and AI Alignment Forum, creating a daily digest of important AI alignment discussions.

## Features
- Fetches 5 latest posts from LessWrong RSS feed
- Fetches 5 latest posts from AI Alignment Forum
- Generates concise summaries using DeepSeek AI
- Creates daily digests

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your DeepSeek API key:
   ```
   DEEPSEEK_API_KEY=your_api_key_here
   ```
4. Run the script:
   ```bash
   python alignment_digest.py
   ```

## Configuration
- The script runs daily by default
- Modify the number of posts or scheduling in the script as needed

## Output
The digest will be saved in the `digests` folder with the current date as the filename. 