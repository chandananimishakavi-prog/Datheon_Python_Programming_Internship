import os
import shutil
import logging
from pathlib import Path
logging.basicConfig(
    filename="organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
FILE_TYPES = {
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",
    ".xls": "Documents",
    ".xlsx": "Documents",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".avi": "Videos",
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".py": "Code",
    ".java": "Code",
    ".cpp": "Code",
    ".c": "Code",
    ".html": "Code",
    ".js": "Code",
}
def get_unique_path(destination):
    """Generate a unique filename if a file already exists."""
    if not destination.exists():
        return destination
    counter = 1
    while True:
        new_path = destination.with_name(
            f"{destination.stem}_{counter}{destination.suffix}"
        )
        if not new_path.exists():
            return new_path
        counter += 1
def organize_files(folder_path):
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        print("Invalid folder path!")
        return
    moved = 0
    skipped = 0
    failed = 0
    print("\nStarting File Organization...\n")
    with os.scandir(folder) as entries:
        for entry in entries:
            if not entry.is_file(follow_symlinks=False):
                continue
            file_path = Path(entry.path)

            # Find category based on extension
            category = FILE_TYPES.get(
                file_path.suffix.lower(),
                "Others"
            )

            destination_folder = folder / category

            try:
                # Create category folder
                destination_folder.mkdir(
                    parents=True,
                    exist_ok=True
                )

                # Avoid filename collisions
                destination = get_unique_path(
                    destination_folder / file_path.name
                )
                shutil.move(str(file_path), str(destination))
                moved += 1
                logging.info(
                    "Moved %s to %s",
                    file_path.name,
                    destination_folder
                )
                print(f"[SUCCESS] {file_path.name} -> {category}")
            except PermissionError:
                skipped += 1
                logging.warning(
                    "Permission denied: %s",
                    file_path
                )
                print(f"[SKIPPED] Permission denied: {file_path.name}")
            except (OSError, shutil.Error) as error:
                failed += 1
                logging.error(
                    "Failed to move %s: %s",
                    file_path,
                    error
                )
                print(f"[ERROR] {file_path.name}: {error}")
    print("\n========== ORGANIZATION SUMMARY ==========")
    print(f"Files successfully moved : {moved}")
    print(f"Files skipped            : {skipped}")
    print(f"Files failed             : {failed}")
    print("==========================================")
    logging.info(
        "Organization completed. Moved=%d, Skipped=%d, Failed=%d",
        moved, skipped, failed
    )
if __name__ == "__main__":
    folder_path = input(
        "Enter the folder path to organize: "
    )
    organize_files(folder_path)
