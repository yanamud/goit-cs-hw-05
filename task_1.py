import os
import asyncio
import argparse
import aiofiles
import logging

logging.basicConfig(level = logging.ERROR)  


async def read_folder(source_folder, output_folder):
    try:
        # для перевірки чи знайдені файли
        files_found = False  
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                source_file = os.path.join(root, file)
                async with aiofiles.open(source_file, 'rb') as src:
                    extension = os.path.splitext(file)[1]
                    destination_folder = os.path.join(output_folder, extension.lstrip('.'))
                    if not os.path.exists(destination_folder):
                        os.makedirs(destination_folder)
                    destination_file = os.path.join(destination_folder, file)
                    async with aiofiles.open(destination_file, 'wb') as dest:
                        await copy_file(src, dest)
                        print(f"Copied: {source_file} -> {destination_file}")
                        # якщо знайдено файл
                        files_found = True  
        if not files_found:
            print("No files found in the source folder.")  
            for directory in dirs:
                # Рекурсивний виклик
                await read_folder(os.path.join(root, directory), output_folder)  
    except Exception as e:
        logging.error(f"An error occurred: {e}") 


async def copy_file(source, destination):
    try:
        content = await source.read()
        await destination.write(content)
    except Exception as e:
        logging.error(f"An error occurred while copying file: {e}")


async def main(args):
    await read_folder(args.source_folder, args.output_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Sort files based on their extensions.")
    parser.add_argument("source_folder", help = "Path to the source folder")
    parser.add_argument("output_folder", help = "Path to the output folder")
    args = parser.parse_args()

    asyncio.run(main(args))

    # Example usage: python task_1.py source output