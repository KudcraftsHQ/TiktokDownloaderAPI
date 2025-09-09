import os
from asyncio import CancelledError
from asyncio import run

from src.application import TikTokDownloader


async def main():
    async with TikTokDownloader() as downloader:
        try:
            # Handle environment variables for automated deployment
            if os.getenv("AUTO_MODE"):
                # Set language from environment variable
                lang = os.getenv("LANGUAGE", "en_US")
                if lang:
                    await downloader._update_language(lang)
                
                # Skip disclaimer if accepted
                if os.getenv("DISCLAIMER_ACCEPTED", "").lower() in ("true", "1", "yes"):
                    await downloader.database.update_config_data("Disclaimer", 1)
                
                # Set run command for the specified mode
                mode = os.getenv("DEFAULT_MODE", "7")  # Default to Web API mode
                downloader.run_command = mode
            
            await downloader.run()
        except (
                KeyboardInterrupt,
                CancelledError,
        ):
            return


if __name__ == "__main__":
    run(main())
