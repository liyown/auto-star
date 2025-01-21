# Auto-Star

A Python tool for automatically liking GitHub repositories with rate limiting to prevent detection.

## Features

- Automatic login with username/password from .env file
- Automatically likes new repositories
- Rate limiting (5 likes per hour)
- Configurable through environment variables
- Detailed logging

## Installation

1. Make sure you have Python 3.8+ and Poetry installed
2. Clone this repository
3. Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

4. Edit `.env` file and set your credentials:

```
USER_NAME=your_username
PASSWORD=your_password
```

5. Install dependencies:

```bash
poetry install
```

## Usage

Simply run the tool:

```bash
poetry run auto-star
```

The tool will:

- Load credentials from .env file
- Automatically like 5 new repositories every hour
- Skip already liked repositories
- Run continuously until stopped with Ctrl+C

## Safety Features

- Secure credential management through .env file
- Rate limiting (5 likes per hour)
- Automatic detection of already liked repositories
- Error handling and logging
- Safe shutdown on keyboard interrupt

## Notes

- The tool will run continuously until stopped with Ctrl+C
- It automatically skips already liked repositories
- Logs are printed to the console with timestamps
- Credentials are stored securely in .env file (not committed to git)
