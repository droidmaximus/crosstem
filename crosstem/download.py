"""
Download utility for optional etymology data.

The etymology data (~1 GB) is too large for PyPI, so it's hosted separately
on GitHub Releases and can be downloaded on demand.
"""

import json
import os
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


# GitHub Release URL for etymology data
ETYMOLOGY_URL = "https://github.com/droidmaximus/crosstem/releases/download/v0.2.0/etymology.json"
ETYMOLOGY_FILE = "etymology.json"


def get_data_dir() -> Path:
    """Get the data directory path."""
    return Path(__file__).parent / "data"


def is_etymology_downloaded() -> bool:
    """Check if etymology data is already downloaded."""
    data_dir = get_data_dir()
    etymology_path = data_dir / ETYMOLOGY_FILE
    return etymology_path.exists()


def get_etymology_size() -> int:
    """Get the size of etymology data to download (in bytes)."""
    try:
        req = Request(ETYMOLOGY_URL, method='HEAD')
        with urlopen(req, timeout=10) as response:
            return int(response.headers.get('Content-Length', 0))
    except (URLError, HTTPError, ValueError):
        # Fallback to approximate size
        return 1_075_000_000  # ~1.08 GB


def download_etymology(force: bool = False, verbose: bool = True) -> bool:
    """
    Download etymology data from GitHub Releases.
    
    Args:
        force: If True, re-download even if file exists
        verbose: If True, print progress messages
        
    Returns:
        bool: True if download successful, False otherwise
        
    Raises:
        URLError: If download fails
        IOError: If file cannot be written
    """
    data_dir = get_data_dir()
    etymology_path = data_dir / ETYMOLOGY_FILE
    
    # Check if already downloaded
    if etymology_path.exists() and not force:
        if verbose:
            print(f"✓ Etymology data already exists at: {etymology_path}")
            print("  Use force=True to re-download")
        return True
    
    # Ensure data directory exists
    data_dir.mkdir(parents=True, exist_ok=True)
    
    if verbose:
        print(f"Downloading etymology data (~1 GB) from GitHub Releases...")
        print(f"URL: {ETYMOLOGY_URL}")
        print(f"Destination: {etymology_path}")
    
    try:
        # Download with progress
        with urlopen(ETYMOLOGY_URL, timeout=30) as response:
            total_size = int(response.headers.get('Content-Length', 0))
            
            if verbose and total_size > 0:
                print(f"Size: {total_size / 1024 / 1024:.1f} MB")
            
            # Download in chunks with progress
            chunk_size = 8192
            downloaded = 0
            
            with open(etymology_path, 'wb') as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    # Show progress
                    if verbose and total_size > 0:
                        percent = (downloaded / total_size) * 100
                        mb_downloaded = downloaded / 1024 / 1024
                        mb_total = total_size / 1024 / 1024
                        print(f"\rProgress: {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)", end='')
        
        if verbose:
            print()  # New line after progress
            
        # Validate downloaded file
        if etymology_path.exists():
            # Quick validation: check if it's valid JSON
            try:
                with open(etymology_path, 'r', encoding='utf-8') as f:
                    # Just read first few bytes to check JSON structure
                    first_chars = f.read(100)
                    if not first_chars.strip().startswith('['):
                        raise ValueError("Downloaded file is not valid JSON")
                
                if verbose:
                    print(f"✓ Etymology data successfully downloaded!")
                    print(f"  Location: {etymology_path}")
                return True
                
            except (json.JSONDecodeError, ValueError) as e:
                if verbose:
                    print(f"✗ Downloaded file appears to be corrupted: {e}")
                # Remove corrupted file
                etymology_path.unlink()
                return False
        else:
            if verbose:
                print("✗ Download failed: file not created")
            return False
            
    except HTTPError as e:
        if verbose:
            print(f"\n✗ HTTP Error {e.code}: {e.reason}")
            if e.code == 404:
                print("  Etymology data not found at the release URL.")
                print("  This might mean the release hasn't been created yet.")
        raise
        
    except URLError as e:
        if verbose:
            print(f"\n✗ Network Error: {e.reason}")
            print("  Please check your internet connection and try again.")
        raise
        
    except IOError as e:
        if verbose:
            print(f"\n✗ File Error: {e}")
            print(f"  Could not write to: {etymology_path}")
        raise


def remove_etymology() -> bool:
    """
    Remove downloaded etymology data to free up disk space.
    
    Returns:
        bool: True if removed successfully
    """
    data_dir = get_data_dir()
    etymology_path = data_dir / ETYMOLOGY_FILE
    
    if etymology_path.exists():
        etymology_path.unlink()
        print(f"✓ Removed etymology data from: {etymology_path}")
        return True
    else:
        print("✗ Etymology data not found (nothing to remove)")
        return False


def get_download_instructions() -> str:
    """
    Get formatted instructions for downloading etymology data.
    
    Returns:
        str: Formatted instructions
    """
    return """
Etymology data is not included by default (it's ~1 GB).

To download etymology data:

    from crosstem import download_etymology
    download_etymology()

Or from command line:

    python -m crosstem.download

This is a one-time download. The data will be cached locally.
""".strip()


if __name__ == "__main__":
    # Allow running as: python -m crosstem.download
    import sys
    
    force = "--force" in sys.argv
    download_etymology(force=force, verbose=True)
