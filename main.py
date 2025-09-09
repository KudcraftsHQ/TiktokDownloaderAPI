from asyncio import CancelledError
from asyncio import run

from src.application import TikTokDownloader


async def main():
    async with TikTokDownloader() as downloader:
        try:
            # Force English language
            await downloader._update_language("en_US")
            
            # Skip disclaimer
            await downloader.database.update_config_data("Disclaimer", 1)
            
            # Force Web API mode
            downloader.run_command = "7"
            
            await downloader.run()
        except (
                KeyboardInterrupt,
                CancelledError,
        ):
            return


if __name__ == "__main__":
    run(main())
