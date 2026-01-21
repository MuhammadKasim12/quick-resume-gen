"""
Resume Handler for Job Application MCP Server.
Manages resume files from a designated folder.
"""

import os
from typing import Optional
from dataclasses import dataclass
from pathlib import Path
import PyPDF2
from docx import Document


@dataclass
class ResumeInfo:
    """Information about a resume file."""
    filename: str
    filepath: str
    file_type: str
    size_bytes: int
    content: str = ""


class ResumeHandler:
    """Handles reading and managing resumes from a folder."""
    
    SUPPORTED_FORMATS = {'.pdf', '.docx', '.doc', '.txt'}
    
    def __init__(self, resume_folder: str):
        """
        Initialize the resume handler.
        
        Args:
            resume_folder: Path to the folder containing resume files
        """
        self.resume_folder = Path(resume_folder)
        self._resumes_cache: dict[str, ResumeInfo] = {}
        self._scan_resumes()
    
    def _scan_resumes(self) -> None:
        """Scan the resume folder for resume files."""
        if not self.resume_folder.exists():
            os.makedirs(self.resume_folder, exist_ok=True)
            return
        
        for file_path in self.resume_folder.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_FORMATS:
                try:
                    content = self._extract_content(file_path)
                    self._resumes_cache[file_path.name] = ResumeInfo(
                        filename=file_path.name,
                        filepath=str(file_path.absolute()),
                        file_type=file_path.suffix.lower(),
                        size_bytes=file_path.stat().st_size,
                        content=content
                    )
                except Exception as e:
                    print(f"Warning: Could not process resume {file_path.name}: {e}")
    
    def _extract_content(self, file_path: Path) -> str:
        """Extract text content from a resume file."""
        suffix = file_path.suffix.lower()
        
        if suffix == '.pdf':
            return self._extract_pdf_content(file_path)
        elif suffix in {'.docx', '.doc'}:
            return self._extract_docx_content(file_path)
        elif suffix == '.txt':
            return file_path.read_text(encoding='utf-8', errors='ignore')
        return ""
    
    def _extract_pdf_content(self, file_path: Path) -> str:
        """Extract text from a PDF file."""
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                return text.strip()
        except Exception as e:
            raise RuntimeError(f"Error reading PDF: {e}")
    
    def _extract_docx_content(self, file_path: Path) -> str:
        """Extract text from a DOCX file."""
        try:
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs]).strip()
        except Exception as e:
            raise RuntimeError(f"Error reading DOCX: {e}")
    
    def get_resume(self, filename: str) -> Optional[ResumeInfo]:
        """Get a specific resume by filename."""
        return self._resumes_cache.get(filename)
    
    def get_default_resume(self) -> Optional[ResumeInfo]:
        """Get the first/default resume if available."""
        if self._resumes_cache:
            return next(iter(self._resumes_cache.values()))
        return None
    
    def list_resumes(self) -> list[str]:
        """Get list of all available resume filenames."""
        return list(self._resumes_cache.keys())
    
    def get_resume_content(self, filename: str) -> Optional[str]:
        """Get the text content of a resume."""
        resume = self.get_resume(filename)
        return resume.content if resume else None
    
    def get_resume_path(self, filename: str) -> Optional[str]:
        """Get the file path of a resume."""
        resume = self.get_resume(filename)
        return resume.filepath if resume else None
    
    def reload_resumes(self) -> None:
        """Rescan the resume folder."""
        self._resumes_cache.clear()
        self._scan_resumes()
    
    def resumes_summary(self) -> dict:
        """Get a summary of available resumes."""
        return {
            "total_resumes": len(self._resumes_cache),
            "resumes": [
                {
                    "filename": r.filename,
                    "type": r.file_type,
                    "size_kb": round(r.size_bytes / 1024, 2)
                }
                for r in self._resumes_cache.values()
            ]
        }

