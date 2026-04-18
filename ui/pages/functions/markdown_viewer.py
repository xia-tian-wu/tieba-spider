from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from pathlib import Path
from markdown_it import MarkdownIt
import uuid
import tempfile

class MarkdownViewer(QWidget):
    """Markdown 阅读器组件 - 使用 QWebEngineView 渲染"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_md_path = None
        self._temp_html_path = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        self.setLayout(layout)

    def load_markdown(self, md_path: Path, display_name: str = ""):
        """加载并渲染 Markdown 文件"""
        try:
            self.current_md_path = md_path

            if not md_path.exists():
                QMessageBox.warning(
                    self,
                    "文件不存在",
                    f"找不到 Markdown 文件：\n{md_path}"
                )
                return False

            md_text = md_path.read_text(encoding="utf-8")
            md = MarkdownIt("commonmark", {"html": True})
            html_body = md.render(md_text)
            html = self._build_html(html_body)

            self._cleanup_temp_file()

            temp_dir = tempfile.gettempdir()
            file_name = f"render_{uuid.uuid4().hex}.html"
            temp_file_path = Path(temp_dir) / file_name

            with open(temp_file_path, 'w', encoding='utf-8') as f:
                f.write(html)

            self._temp_html_path = temp_file_path

            base_url = QUrl.fromLocalFile(str(md_path.parent.absolute()) + "/")
            file_url = QUrl.fromLocalFile(temp_file_path)
            self.web_view.load(file_url)

            return True

        except Exception as e:
            QMessageBox.critical(
                self,
                "加载失败",
                f"无法加载 Markdown 文件：\n{str(e)}"
            )
            return False

    def _cleanup_temp_file(self):
        """删除临时文件"""
        if self._temp_html_path and self._temp_html_path.exists():
            try:
                self._temp_html_path.unlink()
            except Exception:
                pass
            self._temp_html_path = None

    def closeEvent(self, event):
        """窗口关闭时清理"""
        self._cleanup_temp_file()
        super().closeEvent(event)

    def __del__(self):
        """对象销毁时清理"""
        self._cleanup_temp_file()

    def _build_html(self, html_body: str) -> str:
        """构建完整的 HTML 文档，包含所有 CSS 和 JavaScript"""
        base_href = QUrl.fromLocalFile(str(self.current_md_path.parent.absolute()) + "/").toString()

        return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<base href="{base_href}">
<style>
/* --- 基础设置 --- */
body {{
    background: #eef1f5;
    margin: 0;
    padding: 20px;
    font-family: "Segoe UI","Microsoft YaHei",sans-serif;
    transition: background 0.3s ease;
}}

/* 布局容器：Flex 布局，左侧 TOC，右侧内容 */
.layout {{
    display: flex;
    justify-content: center;
    gap: 20px;
    max-width: 1200px;
    margin: 0 auto;
    align-items: flex-start;
}}

/* --- 侧边栏 TOC --- */
.toc-wrapper {{
    width: 140px;
    flex-shrink: 0;
    position: sticky;
    top: 20px;
    max-height: 93vh;
    overflow-y: auto;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 8px;
    padding: 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    direction: rtl;
}}

.toc {{
    display: flex;
    flex-direction: column;
    gap: 5px;
    direction: ltr;
}}

/* 自定义滚动条样式 */
.toc-wrapper::-webkit-scrollbar {{
    width: 6px;
}}
.toc-wrapper::-webkit-scrollbar-thumb {{
    background-color: #ccc;
    border-radius: 3px;
}}
.toc-wrapper::-webkit-scrollbar-track {{
    background: transparent;
}}

.toc a {{
    text-decoration: none;
    color: #555;
    font-size: 14px;
    padding: 6px 8px;
    border-radius: 4px;
    transition: all 0.2s;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}

.toc a:hover {{
    color: #4a90e2;
    background: rgba(74, 144, 226, 0.1);
}}

/* --- 主内容区域 --- */
.container {{
    flex: 1;
    max-width: 900px;
    min-width: 0;
}}

.container > p,
.container > ul,
.container > ol,
.container > blockquote,
.container > pre,
.container > img {{
    background: white;
    margin: 0;
    padding: 8px 20px;
    line-height: 1.6;
    color: #333;
    display: block;
}}

.container > ul, .container > ol {{ padding-left: 40px; }}
.container > blockquote {{
    border-left: 4px solid #ddd;
    margin: 0 0 20px 0;
    padding: 10px 16px;
    background: #fafafa;
    color: #666;
    border-radius: 6px;
}}

h1 {{
    text-align: center;
    color: #333;
    margin-bottom: 30px;
    border-radius: 8px 8px 0 0;
}}

/* 楼层标题 H3 */
h3 {{
    margin-top: 30px;
    margin-bottom: 0;
    padding: 15px 20px;
    background: #ffffff;
    border-left: 5px solid #4a90e2;
    border-radius: 8px 8px 0 0;
    font-size: 18px;
    color: #333;
    scroll-margin-top: 20px;
}}

h3 + p, h3 + ul, h3 + blockquote {{
    border-top: none;
}}

hr {{
    border: none;
    height: 1px;
    background: #ddd;
    position: relative;
}}

/* 图片样式 */
img {{
    display: block;
    margin: 0 auto;
    background: white;
    max-width: 100%;
    height: auto;
    padding: 10px 16px;
    border-radius: 6px;
    cursor: zoom-in;
    box-sizing: border-box;
    border: 1px solid #eee;
}}

/* --- 深色模式 --- */
body.dark-mode {{ background: #1a1a2e; }}

body.dark-mode .container > p,
body.dark-mode .container > ul,
body.dark-mode .container > ol,
body.dark-mode .container > blockquote,
body.dark-mode .container > pre,
body.dark-mode .container > img,
body.dark-mode h3 {{
    background: #2d2d44;
    color: #d0d0e0;
}}

body.dark-mode h3 {{ border-left-color: #7eb8ff; }}

body.dark-mode .toc-wrapper {{
    background: rgba(43, 43, 58, 0.95);
}}

body.dark-mode a {{
    color: #7eb8ff;
}}

body.dark-mode .toc a {{
    color: #b8b8d1;
}}

body.dark-mode .toc a:hover {{
    color: #7eb8ff;
    background: rgba(126, 184, 255, 0.15);
}}

body.dark-mode h1 {{
    color: #e8e8f0;
}}

body.dark-mode p,
body.dark-mode img,
body.dark-mode blockquote,
body.dark-mode pre {{
    background: #2d2d44;
    color: #d0d0e0;
}}

body.dark-mode blockquote {{
    border-left-color: #555577;
}}

body.dark-mode code {{
    background: #3d3d5c;
    color: #ff9ebb;
}}

body.dark-mode hr {{
    background: #444466;
}}

body.dark-mode img {{
    border-color: #444466;
}}

/* --- 灯箱 (Lightbox) --- */
.lightbox {{
    position: fixed;
    display: none;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.85);
    justify-content: center;
    align-items: center;
    z-index: 9999;
    opacity: 0;
    transition: opacity 0.3s ease;
}}

.lightbox.active {{
    display: flex;
    opacity: 1;
}}

.lightbox img {{
    max-width: 90%;
    max-height: 90%;
    background: transparent;
    padding: 0;
    border-radius: 4px;
    box-shadow: 0 0 20px rgba(0,0,0,0.5);
    cursor: zoom-out;
    transition: transform 0.2s ease;
}}

/* --- 日夜模式切换按钮 --- */
.theme-toggle {{
    position: fixed;
    top: 20px;
    right: 20px;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    border: none;
    cursor: pointer;
    background: #ffffff;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    z-index: 1000;
    transition: all 0.3s ease;
}}

.theme-toggle:hover {{
    transform: scale(1.1);
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}}

.sun-icon {{ display: block; }}
.moon-icon {{ display: none; }}

body.dark-mode .theme-toggle {{
    background: #2d2d44;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}}

body.dark-mode .sun-icon {{ display: none; }}
body.dark-mode .moon-icon {{ display: block; }}

.nav {{
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    font-size: 40px;
    background: rgba(255,255,255,0.1);
    border: none;
    color: white;
    cursor: pointer;
    padding: 20px 15px;
    border-radius: 8px;
    transition: all 0.2s;
    user-select: none;
}}

.nav:hover {{
    background: rgba(255,255,255,0.3);
}}

.prev {{ left: 20px; }}
.next {{ right: 20px; }}

.toolbar {{
    position: absolute;
    bottom: 30px;
    display: flex;
    gap: 10px;
    background: rgba(0,0,0,0.6);
    padding: 10px 15px;
    border-radius: 8px;
}}

.toolbar button {{
    padding: 8px 12px;
    font-size: 16px;
    background: rgba(255,255,255,0.2);
    border: none;
    color: white;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;
}}

.toolbar button:hover {{
    background: rgba(255,255,255,0.4);
}}

.image-counter {{
    position: absolute;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    color: white;
    font-size: 14px;
    background: rgba(0,0,0,0.6);
    padding: 6px 12px;
    border-radius: 4px;
}}

::-webkit-scrollbar {{
    width: 10px;
    height: 10px;
}}
::-webkit-scrollbar-track {{
    background: #e6e6e6;
    border-radius: 5px;
}}
::-webkit-scrollbar-thumb {{
    background: #888;
    border-radius: 5px;
    opacity: 0.8;
}}
::-webkit-scrollbar-thumb:hover {{
    background: #555;
    opacity: 1;
}}
</style>
</head>
<body>

<!-- 日夜模式切换按钮 -->
<button class="theme-toggle" id="themeToggle" title="切换日夜模式">
    <span class="sun-icon">☀️</span>
    <span class="moon-icon">🌙</span>
</button>

<div class="layout">
    <!-- 侧边栏目录 -->
    <div class="toc-wrapper">
        <div class="toc" id="toc">
            <div style="font-size:12px; color:#999; padding:10px;">加载中...</div>
        </div>
    </div>

    <!-- 主内容区 -->
    <div class="container">
        {html_body}
    </div>
</div>

<!-- 图片放大灯箱 -->
<div class="lightbox" id="lightbox">
    <button class="nav prev" id="prevBtn">◀</button>
    <div class="image-counter" id="imageCounter">1 / 1</div>
    <img id="lightbox-img" src="">
    <button class="nav next" id="nextBtn">▶</button>

    <div class="toolbar" id="toolbar">
    <button id="zoom-in">＋</button>
    <button id="zoom-out">－</button>
    <button id="rotate">⟳</button>
    <button id="flip-h">⇋</button>
    <button id="flip-v">⇅</button>
    <button id="reset">Reset</button>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', () => {{
    /* 1. 生成目录 */
    const headings = document.querySelectorAll("h1, h3");
    const tocContainer = document.getElementById("toc");
    tocContainer.innerHTML = "";

    if (headings.length === 0) {{
        tocContainer.innerHTML = '<div style="padding:10px; color:#999;">无楼层目录</div>';
    }} else {{
        const fragment = document.createDocumentFragment();
        headings.forEach((h, i) => {{
            const id = "floor_" + i;
            h.id = id;
            const a = document.createElement("a");
            a.href = "#" + id;
            a.textContent = h.tagName === "H1" ? "简介" : "楼层 " + i;
            a.onclick = (e) => {{
                e.preventDefault();
                h.scrollIntoView({{ behavior: 'auto', block: 'start' }});
            }};
            fragment.appendChild(a);
        }});
        tocContainer.appendChild(fragment);
    }}

    /* 2. 图片灯箱功能 */
    const imgs = document.querySelectorAll(".container img");
    const lightbox = document.getElementById("lightbox");
    const lightboxImg = document.getElementById("lightbox-img");
    const imageCounter = document.getElementById("imageCounter");

    let currentIndex = 0;
    let scale = 1;
    let rotate = 0;
    let flipH = 1;
    let flipV = 1;

    function updateTransform() {{
        lightboxImg.style.transform =
            `scale(${{scale}}) rotate(${{rotate}}deg) scaleX(${{flipH}}) scaleY(${{flipV}})`;
    }}

    function updateCounter() {{
        if (imgs.length > 0) {{
            imageCounter.textContent = (currentIndex + 1) + " / " + imgs.length;
        }}
    }}

    function showImage(index) {{
        if(index < 0) index = imgs.length - 1;
        if(index >= imgs.length) index = 0;
        currentIndex = index;
        lightboxImg.src = imgs[index].src;

        scale = 1;
        rotate = 0;
        flipH = 1;
        flipV = 1;
        updateTransform();
        updateCounter();
    }}

    /* 为每张图片绑定点击事件 */
    imgs.forEach((img, i) => {{
        img.onclick = (e) => {{
            e.stopPropagation();
            lightbox.classList.add("active");
            document.body.style.overflow = 'hidden';
            showImage(i);
        }}
    }});

    /* 灯箱背景点击关闭 */
    lightbox.onclick = (e) => {{
        if (e.target === lightbox) {{
            closeLightbox();
        }}
    }};

    /* 左右切换按钮 */
    document.getElementById("prevBtn").onclick = (e) => {{
        e.stopPropagation();
        showImage(currentIndex - 1);
    }}

    document.getElementById("nextBtn").onclick = (e) => {{
        e.stopPropagation();
        showImage(currentIndex + 1);
    }}

    /* 工具按钮 */
    document.getElementById("zoom-in").onclick = (e) => {{
        e.stopPropagation();
        scale *= 1.2;
        updateTransform();
    }}

    document.getElementById("zoom-out").onclick = (e) => {{
        e.stopPropagation();
        scale /= 1.2;
        updateTransform();
    }}

    document.getElementById("rotate").onclick = (e) => {{
        e.stopPropagation();
        rotate += 90;
        updateTransform();
    }}

    document.getElementById("flip-h").onclick = (e) => {{
        e.stopPropagation();
        flipH *= -1;
        updateTransform();
    }}

    document.getElementById("flip-v").onclick = (e) => {{
        e.stopPropagation();
        flipV *= -1;
        updateTransform();
    }}

    document.getElementById("reset").onclick = (e) => {{
        e.stopPropagation();
        scale = 1;
        rotate = 0;
        flipH = 1;
        flipV = 1;
        updateTransform();
    }}

    /* 关闭灯箱函数 */
    const closeLightbox = () => {{
        lightbox.classList.remove('active');
        setTimeout(() => {{
            lightboxImg.src = "";
        }}, 300);
        document.body.style.overflow = '';
    }};

    /* ESC 键关闭 */
    document.addEventListener('keydown', (e) => {{
        if (e.key === "Escape" && lightbox.classList.contains('active')) {{
            closeLightbox();
        }}
        if (lightbox.classList.contains('active')) {{
            if (e.key === "ArrowRight") {{
                showImage(currentIndex + 1);
            }}
            if (e.key === "ArrowLeft") {{
                showImage(currentIndex - 1);
            }}
        }}
    }});

    /* 3. 日夜模式切换 */
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;
    const savedTheme = localStorage.getItem('theme');

    if (savedTheme === 'dark') {{
        body.classList.add('dark-mode');
    }}

    themeToggle.onclick = () => {{
        body.classList.toggle('dark-mode');
        if (body.classList.contains('dark-mode')) {{
            localStorage.setItem('theme', 'dark');
        }} else {{
            localStorage.setItem('theme', 'light');
        }}
    }};
}});
</script>
</body>
</html>'''