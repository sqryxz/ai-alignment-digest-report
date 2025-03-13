# AI Alignment Daily Digest Generator

An automated tool that aggregates and summarizes the latest discussions from the AI alignment community. It fetches posts from LessWrong and the AI Alignment Forum, generates concise summaries using DeepSeek's AI, and creates a daily digest of key themes and developments.

## Features

- 🔄 Fetches latest posts from:
  - LessWrong (via RSS feed)
  - AI Alignment Forum (via GraphQL API)
- 🤖 Uses DeepSeek's AI to generate:
  - High-level summary of key themes across posts
  - Concise summaries of individual posts
- 📅 Automated daily digest generation
- 📝 Markdown-formatted output with:
  - Key themes and developments section
  - Individual post summaries
  - Source attribution and links

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/sqryxz/ai-alignment-digest-report.git
   cd ai-alignment-digest-report
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment:
   ```bash
   cp .env.template .env
   ```
   Then edit `.env` and add your DeepSeek API key from https://platform.deepseek.com/api_keys

## Usage

### Manual Run

Run the script directly:
```bash
python alignment_digest.py
```

The script will:
1. Generate a digest immediately
2. Continue running and generate new digests daily at midnight
3. Save digests in the `digests` folder with the date as filename

### GitHub Actions

The repository includes a GitHub Actions workflow that:
- Runs daily at midnight UTC
- Generates a new digest
- Commits the digest to the repository
- (Optional) Can be triggered manually via workflow_dispatch

## Output Format

Each digest is saved as a markdown file with the following structure:

```markdown
# AI Alignment Daily Digest - YYYY-MM-DD

## Key Themes and Developments
[AI-generated summary of main themes across posts]

## Individual Post Summaries

### [Post Title]
Source: [LessWrong/AI Alignment Forum]
Link: [URL]

Summary: [AI-generated summary]

---
```

## Configuration

Key configuration options in `alignment_digest.py`:
- `POSTS_PER_SOURCE`: Number of posts to fetch from each source (default: 5)
- Schedule time: When the daily digest is generated (default: midnight)
- Summary length: Controlled by the prompt in `summarize_post()`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Some areas for potential improvement:

- Additional sources of AI alignment content
- Enhanced summary generation
- Better theme extraction
- UI improvements for digest format
- Additional automation features

## License

MIT License - feel free to use this code for your own projects.

## Acknowledgments

- LessWrong and AI Alignment Forum for their valuable content
- DeepSeek for their AI API
- All contributors to the AI alignment community 