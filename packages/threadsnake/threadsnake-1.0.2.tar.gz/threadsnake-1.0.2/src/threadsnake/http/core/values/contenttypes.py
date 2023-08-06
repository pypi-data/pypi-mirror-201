
from typing import Dict, List


contentTypes:Dict[str, List[str]] = {
    "text/": ["html", "css"],
    "text/javascript": ["js"],
    "text/html": ["htm"],
    "application/": ["json", "xml", "pdf", "exe"],
    "image/": ["gif", "png", "jpeg", "bmp", "webp"],
    "image/jpeg": ["jpg"],
    "image/x-icon": ["ico"],
    "audio/": ["mpeg", "webm", "ogg", "midi", "wav"],
    "text/plain": ["txt", "*"]
}