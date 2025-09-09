# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DouK-Downloader (formerly TikTokDownloader) is a comprehensive data collection and file download tool for TikTok and DouYin (Chinese TikTok) platforms. It supports downloading videos, images, live streams, and collecting various data including user accounts, comments, and trending content.

## Development Environment

- **Python Version**: 3.12 (required)
- **Package Manager**: UV (recommended) or pip
- **Code Style**: Ruff with Black-compatible formatting
- **Line Length**: 88 characters
- **Indentation**: 4 spaces

## Common Commands

### Environment Setup
```bash
# Install dependencies using UV
uv sync

# Or using pip
pip install -r requirements.txt

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### Running the Application
```bash
# Run the main application
python main.py

# Run in development mode
uv run python main.py
```

### Code Quality
```bash
# Format code with Ruff
ruff format .

# Lint code with Ruff
ruff check .

# Run tests (if available)
pytest
```

### Building Executables
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --icon=./static/images/DouK-Downloader.ico --add-data "static:static" --add-data "locale:locale" --collect-all emoji main.py
```

## Architecture Overview

### Core Components

1. **Application Layer** (`src/application/`):
   - `TikTokDownloader.py`: Main application class and entry point
   - `main_terminal.py`: Terminal interface implementation
   - `main_server.py`: Web API server (FastAPI)
   - `main_monitor.py`: Clipboard monitoring functionality

2. **Interface Layer** (`src/interface/`):
   - Platform-specific data handlers for TikTok and DouYin
   - Modules for accounts, videos, comments, live streams, etc.
   - Separate files for Chinese (`*.py`) and international (`*_tiktok.py`) platforms

3. **Data Models** (`src/models/`):
   - Pydantic models for data validation and serialization
   - Response models, account models, content models
   - Database entity models

4. **Core Services** (`src/`):
   - `config/`: Configuration management and settings
   - `downloader/`: File download functionality
   - `encrypt/`: Platform-specific encryption and token generation
   - `extract/`: Data extraction and parsing
   - `link/`: URL handling and request management
   - `manager/`: Database and cache management
   - `storage/`: Data persistence (CSV, XLSX, SQLite, MySQL)
   - `tools/`: Utility functions and helpers
   - `translation/`: Internationalization support

### Key Architectural Patterns

- **Async/Await**: Heavy use of async programming for network requests
- **Modular Design**: Clear separation of concerns between platform handlers
- **Data Validation**: Pydantic models for request/response validation
- **Plugin Architecture**: Extensible storage backends and platform handlers
- **Context Management**: Proper resource cleanup using context managers

## Development Guidelines

### Code Style
- Follow existing Ruff configuration in `pyproject.toml`
- Use type hints consistently
- Write async functions for I/O operations
- Prefer context managers for resource management

### Platform Handling
- DouYin (Chinese platform) and TikTok (International) have separate handlers
- Common functionality is shared through base classes
- Platform-specific encryption and API handling in respective modules

### Configuration Management
- Settings are managed through `src/config/settings.py`
- User preferences stored in JSON files
- Environment variables for deployment configuration

### Data Storage
- SQLite for local caching and download history
- CSV/XLSX export capabilities
- Optional MySQL support for larger deployments
- File-based configuration management

### Error Handling
- Custom exceptions in `src/tools/error.py`
- Graceful degradation for network issues
- Retry mechanisms for failed requests
- Comprehensive logging system

## Testing

- Test files are located in `src/testers/`
- Run tests with `pytest`
- Test format validation and parameter handling
- Mock external API calls in tests

## Internationalization

- Translation files in `locale/` directory
- Dynamic language switching support
- Text extraction and replacement system
- Support for Chinese and English interfaces

## Security Considerations

- Cookie handling for authenticated requests
- Device ID and token generation for platform compatibility
- Secure storage of sensitive configuration
- Request signing and verification mechanisms

## Deployment

- Docker support with Dockerfile
- GitHub Actions for automated builds
- Cross-platform executable generation
- Web API mode for server deployment

## Using the Web API to Download TikTok Videos

### Starting the API Server

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Start the application and select Web API mode:**
   ```bash
   # Start with interactive prompts
   uv run python main.py
   # Then select:
   # - Language: 2 (English)
   # - Disclaimer: YES
   # - Mode: 7 (Web API Mode)
   ```

3. **Or start programmatically:**
   ```bash
   printf "2\nYES\n7\n" | uv run python main.py
   ```

4. **The API server will start on `http://127.0.0.1:5555`**
   - Documentation: `http://127.0.0.1:5555/docs`
   - Alternative docs: `http://127.0.0.1:5555/redoc`

### Downloading TikTok Videos via API

1. **Extract video ID from TikTok URL:**
   ```
   https://www.tiktok.com/@username/video/7547760453468966150
   Video ID: 7547760453468966150
   ```

2. **Get video details and download URL:**
   ```bash
   curl -X POST http://127.0.0.1:5555/tiktok/detail \
     -H "Content-Type: application/json" \
     -d '{"detail_id": "VIDEO_ID_HERE"}'
   ```

3. **Download the video:**
   ```bash
   # Get download URL
   DOWNLOAD_URL=$(curl -X POST http://127.0.0.1:5555/tiktok/detail \
     -H "Content-Type: application/json" \
     -d '{"detail_id": "VIDEO_ID_HERE"}' \
     -s | jq -r '.data.downloads')

   # Download video file
   curl -L -o "video.mp4" "$DOWNLOAD_URL" \
     -H "User-Agent: TikTok 26.2.0 rv:262018 (iPhone; iOS 14.4.2; en_US) Cronet" \
     -H "Referer: https://www.tiktok.com/" \
     --progress-bar
   ```

### Complete Example

```bash
# 1. Start API server (in background)
printf "2\nYES\n7\n" | uv run python main.py &

# 2. Wait for server to start
sleep 5

# 3. Download TikTok video
VIDEO_ID="7547760453468966150"

# Get video details and download URL
curl -X POST http://127.0.0.1:5555/tiktok/detail \
  -H "Content-Type: application/json" \
  -d "{\"detail_id\": \"$VIDEO_ID\"}" \
  -s | jq -r '.data.downloads' > download_url.txt

# Download the video
curl -L -o "tiktok_${VIDEO_ID}.mp4" "$(cat download_url.txt)" \
  -H "User-Agent: TikTok 26.2.0 rv:262018 (iPhone; iOS 14.4.2; en_US) Cronet" \
  -H "Referer: https://www.tiktok.com/" \
  --progress-bar

# Cleanup
rm download_url.txt
```

### API Response Format

The API returns detailed video information including:
- Video metadata (title, description, duration, resolution)
- User information (username, display name)
- Engagement metrics (views, likes, comments, shares)
- Download URLs for video and audio
- Thumbnail images

### Notes

- The API server runs on port 5555 by default
- TikTok videos may require specific user agents to download successfully
- Download URLs have expiration times and should be used promptly
- No authentication token is required by default (can be configured)

## Extracting Text Content and Captions from TikTok Videos

### Getting Video Descriptions and Text Content

To extract text content (descriptions, recipes, captions) from TikTok videos:

```bash
# Get basic video description
curl -X POST http://127.0.0.1:5555/tiktok/detail \
  -H "Content-Type: application/json" \
  -d '{"detail_id": "VIDEO_ID"}' \
  -s | jq '{desc, text_extra, tag}'

# Get detailed text content (structured descriptions)
curl -X POST http://127.0.0.1:5555/tiktok/detail \
  -H "Content-Type: application/json" \
  -d '{"detail_id": "VIDEO_ID", "source": true}' \
  -s | jq '.data | {desc, contents}'
```

### Extracting Auto-Generated Captions/Subtitles

For videos with auto-generated captions (speech-to-text):

1. **Check if captions are available:**
   ```bash
   curl -X POST http://127.0.0.1:5555/tiktok/detail \
     -H "Content-Type: application/json" \
     -d '{"detail_id": "VIDEO_ID", "source": true}' \
     -s | jq '.data.video.claInfo.captionInfos'
   ```

2. **List available caption languages:**
   ```bash
   curl -X POST http://127.0.0.1:5555/tiktok/detail \
     -H "Content-Type: application/json" \
     -d '{"detail_id": "VIDEO_ID", "source": true}' \
     -s | jq '.data.video.claInfo.captionInfos[] | {language, isOriginalCaption, isAutoGen}'
   ```

3. **Download caption file (WebVTT format):**
   ```bash
   # Get original language captions
   CAPTION_URL=$(curl -X POST http://127.0.0.1:5555/tiktok/detail \
     -H "Content-Type: application/json" \
     -d '{"detail_id": "VIDEO_ID", "source": true}' \
     -s | jq -r '.data.video.claInfo.captionInfos[] | select(.isOriginalCaption==true) | .url')
   
   curl -s "$CAPTION_URL" > captions.vtt
   ```

4. **Extract only the text from captions:**
   ```bash
   curl -X POST http://127.0.0.1:5555/tiktok/detail \
     -H "Content-Type: application/json" \
     -d '{"detail_id": "VIDEO_ID", "source": true}' \
     -s | jq -r '.data.video.claInfo.captionInfos[] | select(.isOriginalCaption==true) | .url' | \
   xargs curl -s | grep -v "^WEBVTT" | grep -v "^$" | grep -v "^[0-9][0-9]:" | sed 's/^[[:space:]]*//'
   ```

### Complete Text Extraction Script

```bash
#!/bin/bash
VIDEO_ID="$1"

echo "=== TikTok Video Text Extraction ==="
echo "Video ID: $VIDEO_ID"
echo

# Get basic info
echo "=== Basic Description ==="
curl -X POST http://127.0.0.1:5555/tiktok/detail \
  -H "Content-Type: application/json" \
  -d "{\"detail_id\": \"$VIDEO_ID\"}" \
  -s | jq -r '.data.desc // "No description available"'
echo

# Get detailed content if available
echo "=== Detailed Content ==="
curl -X POST http://127.0.0.1:5555/tiktok/detail \
  -H "Content-Type: application/json" \
  -d "{\"detail_id\": \"$VIDEO_ID\", \"source\": true}" \
  -s | jq -r '.data.contents[]?.desc' | grep -v "^$"
echo

# Check for captions
echo "=== Auto-Generated Captions ==="
CAPTION_URL=$(curl -X POST http://127.0.0.1:5555/tiktok/detail \
  -H "Content-Type: application/json" \
  -d "{\"detail_id\": \"$VIDEO_ID\", \"source\": true}" \
  -s | jq -r '.data.video.claInfo.captionInfos[]? | select(.isOriginalCaption==true) | .url')

if [ -n "$CAPTION_URL" ]; then
  curl -s "$CAPTION_URL" | grep -v "^WEBVTT" | grep -v "^$" | grep -v "^[0-9][0-9]:" | sed 's/^[[:space:]]*//'
else
  echo "No auto-generated captions available"
fi
```

### Usage Examples

```bash
# Save script as extract_text.sh and make executable
chmod +x extract_text.sh

# Extract text from a recipe video
./extract_text.sh 7546338533716315400

# Extract text from a speech video
./extract_text.sh 7547760453468966150
```

### Text Content Types

The API can extract different types of text content:

1. **Video Descriptions**: Basic title/description text
2. **Structured Content**: Detailed formatted content (recipes, instructions)
3. **Auto-Generated Captions**: Speech-to-text from video audio
4. **Translated Captions**: Machine-translated versions in different languages
5. **Hashtags**: Extracted and structured hashtag information

### Caption Availability

- **Auto-generated captions**: Available for videos with clear speech
- **Manual captions**: When creators add their own subtitles
- **No captions**: When `noCaptionReason` is present in the response
- **Multiple languages**: Original + translated versions when available