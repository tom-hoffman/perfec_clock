#!/usr/bin/env python3
# make_release.py

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

SUPPORTED_VERSIONS = ["10.0.3", "10.1.4", "10.2.1"]

def get_project_metadata() -> tuple[str, str]:
    """Resolves the current working directory name and application version string."""
    # Find project directory name (e.g., perfec_clock or perfec_euclidian)
    # If currently in 'src', step up one level to look for project name and version.txt
    current_dir = Path.cwd()
    if current_dir.name == "src":
        project_name = current_dir.parent.name
        version_file = current_dir.parent / "version.txt"
        if not version_file.exists():
            version_file = current_dir / "version.txt"
    else:
        project_name = current_dir.name
        version_file = current_dir / "version.txt"

    # Read application version or default safely
    app_version = "unknown"
    if version_file.exists():
        try:
            with open(version_file, "r") as f:
                app_version = f.read().strip()
        except Exception as e:
            print(f"⚠ Warning: Could not read version.txt: {e}")
            
    return project_name, app_version

def clean_stray_artifacts():
    """Wipes unexpected local workspace compiler residuals (.mpy artifacts)."""
    for item in Path(".").glob("*.mpy"):
        try:
            item.unlink()
        except Exception:
            pass

def main():
    parser = argparse.ArgumentParser(description="Generate production bundles for all supported versions.")
    parser.add_argument("platform", help="Platform name string (e.g., linux-amd64)")
    args = parser.parse_args()

    # Step up to check paths relative to 'src' directory location
    bin_dir = Path("../bin").resolve()
    temp_build_dir = Path("./build_release")

    # Clear out old releases
    if bin_dir.exists():
        print(f"🧹 Clearing existing assets inside release directory: {bin_dir}")
        shutil.rmtree(bin_dir)
    bin_dir.mkdir(parents=True, exist_ok=True)

    # Resolve names and version file contents
    project_name, app_version = get_project_metadata()
    print(f"📦 Project Name Detected: {project_name}")
    print(f"🏷️  App Version (version.txt): v{app_version}")
    print(f"🚀 Release mode active. Processing CircuitPython variants: {', '.join(SUPPORTED_VERSIONS)}")

    # Clean the current working directory before starting compiler tasks
    clean_stray_artifacts()

    for version in SUPPORTED_VERSIONS:
        if temp_build_dir.exists():
            shutil.rmtree(temp_build_dir)

        print(f"\n--- Building Release Variant for CircuitPython {version} ---")
        
        try:
            subprocess.run(
                [sys.executable, "make.py", args.platform, version, str(temp_build_dir)],
                check=True
            )
        except subprocess.CalledProcessError:
            print(f"❌ Build failed for CircuitPython variant {version}. Halting release pipeline.")
            if temp_build_dir.exists():
                shutil.rmtree(temp_build_dir)
            clean_stray_artifacts()
            sys.exit(1)

        # Output template: project_name-v{app_version}-CircuitPython{cp_version}.zip
        archive_name = f"{project_name}-v{app_version}-CircuitPython{version}"
        archive_target = bin_dir / archive_name
        
        shutil.make_archive(str(archive_target), 'zip', temp_build_dir)
        print(f"✓ Release ZIP saved to: {archive_target}.zip")

        if temp_build_dir.exists():
            shutil.rmtree(temp_build_dir)

    # Final post-build environment sanitization
    clean_stray_artifacts()
    print("\n🎉 All production variants bundled successfully!")

if __name__ == "__main__":
    main()
