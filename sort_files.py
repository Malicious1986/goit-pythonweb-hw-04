import argparse
import asyncio
import logging
from aiopath import AsyncPath as Path
import aioshutil


async def copy_file(src: Path, dst_root: Path):
    try:
        ext = src.suffix.lower().lstrip(".") or "_no_ext"
        target_dir = dst_root / ext
        await target_dir.mkdir(parents=True, exist_ok=True)

        dst = target_dir / src.name
        await aioshutil.copy2(str(src), str(dst))

        logging.info(f"Copied: {src} -> {dst}")
    except Exception as e:
        logging.error(f"Failed to copy {src}: {e}")


async def read_folder(source: Path, output: Path):
    try:
        entries = [entry async for entry in source.iterdir()]
    except Exception as e:
        logging.error(f"Failed to list directory {source}: {e}")
        return

    files = []
    dirs = []
    for entry in entries:
        try:
            if await entry.is_file():
                files.append(copy_file(entry, output))
                continue
            if await entry.is_dir():
                dirs.append(read_folder(entry, output))
        except Exception as e:
            logging.error(f"Failed to stat {entry}: {e}")

    if files or dirs:
        await asyncio.gather(*files, *dirs)

    logging.info(f"Processed directory: {source}")


async def _run(source: Path, output: Path):
    source = await Path(source).expanduser()
    output = await Path(output).expanduser()

    if not await source.exists() or not await source.is_dir():
        logging.error(f"Source folder does not exist: {source}")
        return

    await output.mkdir(parents=True, exist_ok=True)

    await read_folder(source, output)


def main():
    parser = argparse.ArgumentParser(
        description="Asynchronously sort files into subfolders based on file extension."
    )
    parser.add_argument("-s", "--source", required=True, help="Path to source folder")
    parser.add_argument("-o", "--output", required=True, help="Path to output folder")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    asyncio.run(_run(args.source, args.output))


if __name__ == "__main__":
    main()
