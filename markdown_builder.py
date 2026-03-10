import os
import re
import json

from config import MARKDOWN_DIR, IMAGES_DIR
from spider.type_models import PostData

def convert_post_json_to_markdown(json_path: str) -> str:
    """
    将单个帖子 JSON 文件转换为 Markdown，并保存到 markdowns/ 下。
    
    Args:
        json_path: 如 'data/posts/安全标题_7833341768_see_lz.json'
    
    Returns:
        生成的 Markdown 文件路径
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        post_data = json.load(f)
    
    post_id = post_data['post_id']
    see_lz = post_data.get('see_lz', False)
    mode_suffix = "see_lz" if see_lz else "full"
    image_abs_dir = os.path.join(IMAGES_DIR, f"{post_id}_{mode_suffix}")
    
    md_content = _render_markdown_from_post_data(post_data, image_abs_dir)
    
    base_name = os.path.splitext(os.path.basename(json_path))[0]
    md_filename = f'{base_name}.md'
    md_path = os.path.join(MARKDOWN_DIR, md_filename)
    
    os.makedirs(MARKDOWN_DIR, exist_ok=True)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return md_path
    
def _render_markdown_from_post_data(post_data: PostData, image_abs_dir: str) -> str:
    """
    """
    lines = []
    
    title = post_data.get('title', '无标题')
    lines.append(f"# {title}\n")
    bar_name = post_data.get('bar', '未知吧名')
    original_url = post_data['url']
    mode = '只看楼主' if post_data.get('see_lz') else '完整版'
    crawl_time = post_data.get('crawl_time', '')
    total_pages = post_data['total_pages']
    total_floors = post_data['total_floors']
    lines.append(
        f"> **原始链接**: {original_url}  \n"
        f"> **帖子所在**: {bar_name}  \n"
        f"> **模式**: {mode}  \n"
        f"> **总楼层数**: {total_floors}  \n"
        f"> **总页数**: {total_pages}  \n"
        f"> **抓取时间**: {crawl_time}  \n"
    )
    lines.append('---\n')
    
    for floor in post_data["floors"]:
        floor_num = floor["floor_number"]
        author = floor["author"]
        post_time = floor.get("post_time", "")
        ip = floor.get("ip_location", "")
        content = floor.get("content", "")
        device = floor.get('device', '')
        
        meta_dict = {
        "时间": post_time,
        "IP": ip,
        "设备": device
            }
        meta_parts = [f"{k}：{v}" for k, v in meta_dict.items() if v.strip()]
        floor_meta = [f"{floor_num}楼"] + meta_parts
        floor_meta_str = " · ".join(floor_meta)
        
        lines.append(f"### {author} \n{floor_meta_str}\n")
        
        # 替换 [图片：xxx.jpg] 为 ![image](相对路径) 
        def replace_image_tag(match):
            img_filename = match.group(1)  # e.g., "12897d3e...jpg"
            img_abs_path = os.path.join(image_abs_dir, img_filename)

            if not os.path.exists(img_abs_path):
                return f"[图片：{img_filename} (未找到)]"

            # 计算相对于 markdown_posts/ 的路径
            rel_path = os.path.relpath(img_abs_path, MARKDOWN_DIR)
            rel_path = rel_path.replace("\\", "/")  # 统一为 Unix 风格
            return f"![image]({rel_path})"
        
        renderded_content = re.sub(r'\[图片：([^\]]+)\]', replace_image_tag, content)
        lines.append(renderded_content.strip() or '「该楼层无内容」')
        lines.append('\n---\n')
    
    return '\n'.join(lines)
        
