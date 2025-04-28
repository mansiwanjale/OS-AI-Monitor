import os

# SETTINGS
SCAN_EXTENSIONS = [
    '.tmp', '.log', '.bak', '.old', '.err', '.swp', '.dmp', '.dat', '.chk', '.db', '.sqlite', '.exe', '.msi', '.dmg', '.pkg', '.zip', '.tar', '.bak'
]

SCAN_FOLDERS = [
    'C:/Temp',
    'C:/Windows/Temp',
    'C:/Windows/Prefetch',
    'C:/Windows/SoftwareDistribution/Download',
    'C:/Users/Public/Downloads',
    'C:/$Recycle.Bin',
    'D:/Downloads',
    'C:/ProgramData/Microsoft/Search/Data',
    
]


def get_readable_size(size_in_bytes):
    """Convert byte size to a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.1f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.1f} TB"

def scan_files():
    """Scan specified folders for junk files."""
    found_files = []
    for folder in SCAN_FOLDERS:
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if any(file.endswith(ext) for ext in SCAN_EXTENSIONS):
                        file_path = os.path.join(root, file)
                        try:
                            size = os.path.getsize(file_path)
                        except Exception:
                            size = 0
                        found_files.append({
                            "name": file,
                            "path": file_path,
                            "size": get_readable_size(size)
                        })
    return found_files

def delete_files(paths):
    """Delete the given files and return the status of deletion."""
    deleted = []
    errors = []
    for path in paths:
        try:
            os.remove(path)
            deleted.append(path)
        except Exception as e:
            errors.append({"path": path, "error": str(e)})
    return deleted, errors

def delete_junk_files():
    """Delete all junk files identified in the scan."""
    junk_files = scan_files()  # Get list of junk files
    paths_to_delete = [file['path'] for file in junk_files]
    
    if not paths_to_delete:
        return "No junk files found."

    deleted, errors = delete_files(paths_to_delete)
    if deleted:
        return f"Successfully deleted {len(deleted)} files: {deleted}"
    elif errors:
        return f"Errors occurred while deleting some files: {errors}"

# Run the deletion function (you can trigger this manually or via an API)
if __name__ == "__main__":
    result = delete_junk_files()
    print(result)
