#!/usr/bin/env python3
# PERFEC System Release Automation
# make_zip.py
# copyright 2026, Tom Hoffman
# MIT License
# Directly packages uncompiled editable files straight into a single release zip.

import argparse
import shutil
import os
import sys
import tempfile
from pathlib import Path

# --- UNIFIED EXCLUSION LIST ---
# Ensures your release zip remains completely free of local scripting or cache clutter
SKIP = {"make.py", "make_release.py", "make_zip.py", "__pycache__", ".git", ".vscode"}

def main():
    parser = argparse.ArgumentParser(description="Directly compress allowed project files into a single release zip.")
    parser.add_argument("release_name", help="Name of this release tag (e.g., clock-v1.0.0-beta, final-release)")
    parser.add_argument("target_dir", help="Destination directory path where the zip should be saved (e.g., ../bin/)")
    
    args = parser.parse_args()
    
    # 1. Resolve source and output destination directories
    current_dir = Path(".").resolve()
    bin_base_dir = Path(args.target_dir).resolve()
    
    # Ensure target output directory exists
    bin_base_dir.mkdir(parents=True, exist_ok=True)
    
    # Target zip file descriptor path: ../bin/<release_name>.zip
    final_zip_target = bin_base_dir / args.release_name

    print("==================================================")
    print(f"Starting Direct Zip Package: {args.release_name}")
    print(f"Destination: {final_zip_target}.zip")
    print("==================================================\n")

    # 2. Utilize a safe background system temp folder to bundle files allocation-free
    with tempfile.TemporaryDirectory() as temp_workspace:
        temp_path = Path(temp_workspace)
        # Create an internal root folder matching the release name inside the zip file structure
        zip_root_dir = temp_path / args.release_name
        zip_root_dir.mkdir()
        
        print("Gathering allowed editable files...")
        for filename in os.listdir("."):
            if filename in SKIP:
                print(f" ✗ Skipping: {filename}")
                continue
                
            local_path = current_dir / filename
            remote_path = zip_root_dir / filename

            try:
                if local_path.is_dir():
                    # Copy directory trees while explicitly ignoring hidden pycache files
                    shutil.copytree(local_path, remote_path, ignore=shutil.ignore_patterns('__pycache__', '.*'))
                    print(f" ✓ Bundled directory: {filename}/")
                else:
                    # Copy editable source code files directly
                    shutil.copyfile(local_path, remote_path)
                    print(f" ✓ Bundled file: {filename}")
            except Exception as e:
                print(f" ! Warning: Failed to copy {filename} ({e})")

        print("\nCompressing into final release archive...")
        try:
            # Compress the temporary directory layout directly into the targeted destination directory
            actual_zip_path = shutil.make_archive(
                base_name=str(final_zip_target),
                format="zip",
                root_dir=str(temp_path),
                base_dir=args.release_name
            )
            print(f"✓ Success! Archive generated safely.")
            print(f"📦 Final Package: {Path(actual_zip_path).name} written to {bin_base_dir.name}/\n")
        except Exception as e:
            print(f" ✗ Compression failed: {e}")
            sys.exit(1)

    print("==================================================")
    print(" 🎉 CLOCK ZIP PRODUCTION COMPLETE! 🎉")
    print("==================================================")

if __name__ == "__main__":
    main()
