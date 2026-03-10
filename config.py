import sys
from fake_useragent import UserAgent
from pathlib import Path

# basic settings
def get_base_path() -> Path:
    # PyInstaller
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)

    # Nuitka / frozen
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent

    # 开发模式
    return Path(__file__).parent

# 全局定义数据路径
BASE_PATH = get_base_path()
DATA_DIR = BASE_PATH / 'data'
POSTS_DIR = DATA_DIR / "posts"
IMAGES_DIR = DATA_DIR / "images"
MARKDOWN_DIR = DATA_DIR / "markdowns"

# 创建目录（现在会创建在 exe 同目录下！）
for directory in [DATA_DIR, POSTS_DIR, IMAGES_DIR, MARKDOWN_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# other configurations
MAX_RETRIES = 5
TIMEOUT = 10  
REQUEST_INTERVAL = 2  