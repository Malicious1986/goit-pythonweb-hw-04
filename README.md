# goit-pythonweb-hw-04

A small utility that asynchronously sorts files from a source folder into subfolders grouped by file extension.

This repository contains `sort_files.py` which uses async file/path operations (via `aiopath`) and `aioshutil` to copy files concurrently.

## Usage

Basic usage:

```bash
# sort files from Downloads into ~/Sorted
python3 sort_files.py -s ~/Downloads -o ~/Sorted
```

Options:

- `-s, --source` : Path to the source folder to scan (required)
- `-o, --output` : Path to the folder where files will be copied into extension-named subfolders (required)
