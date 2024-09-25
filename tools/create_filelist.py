import argparse
import os
from loguru import logger

from file import list_files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_dir", type=str)
    parser.add_argument("output_dir", type=str)
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    logger.info(f'Loading metadata from {args.data_dir}')
    files = list_files(args.data_dir, extensions=[".txt"], recursive=True)
    
    filelist = []
    for file in files:
        if 'vivoice' in str(file) or 'voice_clone' in str(file):
            continue
        if 'data_bac_nam' not in str(file):
            continue
        if file.name == "metadata.txt":
            logger.info(f'Loading {file}')
            with open(file, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip().split("|")
                    if len(line) != 3:
                        print(line)
                        continue
                    if not os.path.exists(line[1]):
                        print(f"File {line[1]} not exist")
                        continue
                    if 'vivos' in str(file):
                        line[2] = line[2].lower().strip().strip(".") + " ."
                    line = f"{line[1]}|{line[0]}|vi|{line[2]}"
                    filelist.append(line)

    with open(os.path.join(args.output_dir, "filelist.txt"), "w", encoding="utf-8") as f:
        for file in filelist:
            f.write(file + "\n")

    logger.success(f'Loaded {len(filelist)} files, save metadata to {args.output_dir}/filelist.txt')

if __name__ == "__main__":
    main()
