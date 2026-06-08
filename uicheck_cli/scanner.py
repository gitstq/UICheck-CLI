"""
File scanner and format detector for UICheck-CLI.

Scans directories for supported file types and detects
the format of each file (HTML, CSS, JSX, Vue SFC).
"""

import os
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Generator
from enum import Enum


class FileFormat(Enum):
    """Supported file formats for analysis."""

    HTML = "html"
    CSS = "css"
    JSX = "jsx"
    VUE_SFC = "vue"
    UNKNOWN = "unknown"


# File extension to format mapping
EXTENSION_MAP = {
    ".html": FileFormat.HTML,
    ".htm": FileFormat.HTML,
    ".css": FileFormat.CSS,
    ".jsx": FileFormat.JSX,
    ".tsx": FileFormat.JSX,
    ".js": FileFormat.JSX,  # Treat plain JS as JSX-like for scanning
    ".vue": FileFormat.VUE_SFC,
}

# Directories to skip during scanning
SKIP_DIRS = {
    "node_modules", ".git", "__pycache__", ".venv", "venv",
    "dist", "build", ".next", ".nuxt", "coverage", ".cache",
    ".tox", ".mypy_cache", ".pytest_cache", "vendor",
}

# Files to skip
SKIP_FILES = {
    ".DS_Store", "Thumbs.db", ".gitkeep",
}


@dataclass
class ScannedFile:
    """Represents a file that has been scanned.

    Attributes:
        path: Absolute file path.
        relative_path: Path relative to the scan root.
        format: Detected file format.
        size_bytes: File size in bytes.
        content: File content string.
    """

    path: str
    relative_path: str
    format: FileFormat
    size_bytes: int
    content: str = ""

    @property
    def extension(self) -> str:
        """Get the file extension."""
        return os.path.splitext(self.path)[1].lower()


class FileScanner:
    """Scans directories and individual files for supported formats.

    Usage:
        scanner = FileScanner()
        for scanned_file in scanner.scan("/path/to/project"):
            print(scanned_file.path, scanned_file.format)
    """

    def __init__(self, max_file_size: int = 1_000_000):
        """Initialize the scanner.

        Args:
            max_file_size: Maximum file size in bytes to read (default: 1MB).
        """
        self.max_file_size = max_file_size
        self._stats = {
            "total_files": 0,
            "scanned_files": 0,
            "skipped_dirs": 0,
            "skipped_files": 0,
            "errors": 0,
        }

    @property
    def stats(self) -> dict:
        """Return scanning statistics."""
        return dict(self._stats)

    def scan(self, target: str) -> List[ScannedFile]:
        """Scan a file or directory for supported files.

        Args:
            target: Path to a file or directory to scan.

        Returns:
            List of ScannedFile objects.
        """
        path = Path(target).resolve()

        if not path.exists():
            raise FileNotFoundError(f"Path not found: {target}")

        if path.is_file():
            result = self._scan_file(path, path.parent)
            return [result] if result else []

        if path.is_dir():
            return list(self._scan_directory(path))

        return []

    def _scan_directory(self, directory: Path) -> Generator[ScannedFile, None, None]:
        """Recursively scan a directory for supported files.

        Args:
            directory: Path to the directory to scan.

        Yields:
            ScannedFile objects for each supported file found.
        """
        for root, dirs, files in os.walk(directory):
            # Filter out skipped directories
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
            self._stats["skipped_dirs"] += len([d for d in dirs if d in SKIP_DIRS])

            # Sort for deterministic order
            dirs.sort()
            files.sort()

            for filename in files:
                if filename in SKIP_FILES:
                    self._stats["skipped_files"] += 1
                    continue

                file_path = Path(root) / filename
                scanned = self._scan_file(file_path, directory)
                if scanned:
                    yield scanned

    def _scan_file(self, file_path: Path, root: Path) -> Optional[ScannedFile]:
        """Scan a single file.

        Args:
            file_path: Path to the file.
            root: Root directory for relative path calculation.

        Returns:
            ScannedFile object, or None if the file should be skipped.
        """
        self._stats["total_files"] += 1

        # Check extension
        ext = file_path.suffix.lower()
        if ext not in EXTENSION_MAP:
            self._stats["skipped_files"] += 1
            return None

        # Check file size
        try:
            size = file_path.stat().st_size
            if size > self.max_file_size:
                self._stats["skipped_files"] += 1
                return None
        except OSError:
            self._stats["errors"] += 1
            return None

        # Read file content
        try:
            content = file_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            self._stats["errors"] += 1
            return None

        # Detect format
        fmt = self._detect_format(file_path, content)

        self._stats["scanned_files"] += 1

        return ScannedFile(
            path=str(file_path),
            relative_path=str(file_path.relative_to(root)),
            format=fmt,
            size_bytes=size,
            content=content,
        )

    def _detect_format(self, file_path: Path, content: str) -> FileFormat:
        """Detect the file format based on extension and content.

        Args:
            file_path: Path to the file.
            content: File content string.

        Returns:
            Detected FileFormat enum value.
        """
        ext = file_path.suffix.lower()

        # Use extension-based detection first
        if ext in EXTENSION_MAP:
            detected = EXTENSION_MAP[ext]

            # Special case: .vue files should be Vue SFC
            if ext == ".vue":
                return FileFormat.VUE_SFC

            # Special case: .tsx/.jsx should be JSX
            if ext in (".jsx", ".tsx"):
                return FileFormat.JSX

            return detected

        # Fallback: content-based detection
        if "<template>" in content and "<script>" in content:
            return FileFormat.VUE_SFC
        if re.search(r"<(div|span|section|header)[\s>]", content):
            return FileFormat.HTML
        if re.search(r"[.#][\w-]+\s*\{", content):
            return FileFormat.CSS

        return FileFormat.UNKNOWN

    def extract_sections(self, scanned_file: ScannedFile) -> Dict[str, str]:
        """Extract relevant sections from a scanned file based on format.

        For Vue SFC: extracts <template>, <script>, <style> sections.
        For JSX: extracts the return statement JSX.
        For HTML: returns full content.
        For CSS: returns full content.

        Args:
            scanned_file: The ScannedFile to extract from.

        Returns:
            Dictionary with keys 'html', 'css', 'js' containing extracted sections.
        """
        sections = {"html": "", "css": "", "js": ""}

        if scanned_file.format == FileFormat.VUE_SFC:
            # Extract <template> section
            template_match = re.search(
                r"<template[^>]*>(.*?)</template>",
                scanned_file.content, re.DOTALL | re.IGNORECASE
            )
            if template_match:
                sections["html"] = template_match.group(1)

            # Extract <style> section
            style_match = re.search(
                r"<style[^>]*>(.*?)</style>",
                scanned_file.content, re.DOTALL | re.IGNORECASE
            )
            if style_match:
                sections["css"] = style_match.group(1)

            # Extract <script> section
            script_match = re.search(
                r"<script[^>]*>(.*?)</script>",
                scanned_file.content, re.DOTALL | re.IGNORECASE
            )
            if script_match:
                sections["js"] = script_match.group(1)

        elif scanned_file.format == FileFormat.JSX:
            # Extract JSX from return statements
            return_matches = re.findall(
                r"return\s*\(\s*([\s\S]*?)\s*\)\s*;?",
                scanned_file.content
            )
            if return_matches:
                # Combine all return JSX
                sections["html"] = "\n".join(return_matches)

            # Extract CSS-in-JS or styled components
            css_matches = re.findall(
                r"(?:style\s*=\s*\{|styled\.[\w]+|css`|css\(\s*[`{])",
                scanned_file.content
            )
            if css_matches:
                sections["css"] = scanned_file.content  # Pass full content for CSS-in-JS analysis

            sections["js"] = scanned_file.content

        elif scanned_file.format == FileFormat.HTML:
            # Extract <style> blocks
            style_blocks = re.findall(
                r"<style[^>]*>(.*?)</style>",
                scanned_file.content, re.DOTALL | re.IGNORECASE
            )
            sections["css"] = "\n".join(style_blocks)
            sections["html"] = scanned_file.content

        elif scanned_file.format == FileFormat.CSS:
            sections["css"] = scanned_file.content

        return sections
