import os
from PIL import Image

REPO_OWNER = "eric861129"
REPO_NAME = "Cloud-Assets"
BRANCH = "main"
CDN_BASE_URL = f"https://cdn.jsdelivr.net/gh/{REPO_OWNER}/{REPO_NAME}@{BRANCH}"

def optimize_images(directory=".", quality=80):
    """
    遞迴掃描目錄，將圖片轉為 WebP 並刪除原圖。
    """
    for root, dirs, files in os.walk(directory):
        if ".git" in root:
            continue
            
        for filename in files:
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                filepath = os.path.join(root, filename)
                base = os.path.splitext(filename)[0]
                output_path = os.path.join(root, f"{base}.webp")
                
                try:
                    # 轉檔
                    with Image.open(filepath) as img:
                        img.save(output_path, "WEBP", quality=quality, method=6)
                    print(f"優化成功: {filepath} -> {output_path}")
                    
                    # 刪除原圖
                    os.remove(filepath)
                    print(f"已刪除原圖: {filepath}")
                    
                except Exception as e:
                    print(f"處理 {filepath} 時出錯: {e}")

def generate_gallery(directory="."):
    """
    掃描所有 WebP 圖片並生成按資料夾分組的 GALLERY.md 索引檔。
    """
    print("正在生成 GALLERY.md ...")
    
    lines = ["# 📂 圖片索引 (Gallery)", "", "自動生成的圖片清單，包含 CDN 連結與引用語法。", ""]
    
    # 建立一個字典，key 是資料夾路徑，value 是該資料夾下的圖片清單
    gallery_data = {}
    
    for root, dirs, files in os.walk(directory):
        if ".git" in root:
            continue
        
        webp_files = [f for f in files if f.lower().endswith(".webp")]
        if webp_files:
            # 取得相對路徑作為分類標題
            rel_dir = os.path.relpath(root, directory).replace("\\", "/")
            if rel_dir == ".":
                rel_dir = "Root (根目錄)"
            gallery_data[rel_dir] = sorted(webp_files)
    
    if not gallery_data:
        lines.append("目前沒有圖片。")
    else:
        # 按資料夾名稱排序
        for folder in sorted(gallery_data.keys()):
            lines.append(f"## 📁 {folder}")
            lines.append("<details>")
            lines.append(f"<summary>點擊展開 / 摺疊 {folder} 中的圖片</summary>")
            lines.append("")
            
            for filename in gallery_data[folder]:
                # 還原完整相對路徑以產生連結
                if folder == "Root (根目錄)":
                    img_path = filename
                else:
                    img_path = f"{folder}/{filename}"
                
                full_url = f"{CDN_BASE_URL}/{img_path}"
                
                lines.append(f"### 🖼️ {filename}")
                lines.append(f"![{filename}]({full_url})")
                lines.append("")
                lines.append("| 類型 | 語法 (點擊複製) |")
                lines.append("| :--- | :--- |")
                lines.append(f"| **CDN Link** | `{full_url}` |")
                lines.append(f"| **Markdown** | `![{filename}]({full_url})` |")
                lines.append(f"| **HTML** | `<img src=\"{full_url}\" alt=\"{filename}\" loading=\"lazy\">` |")
                lines.append("")
                lines.append("---")
            
            lines.append("</details>")
            lines.append("")

    with open("GALLERY.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print("GALLERY.md 生成完畢。")

def generate_index_html(gallery_data):
    """
    根據圖片資料生成一個美觀的 index.html 靜態頁面。
    """
    print("正在生成 index.html ...")
    
    html_template = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloud-Assets 圖庫</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; padding-top: 50px; }
        .card { transition: transform 0.2s; margin-bottom: 20px; }
        .card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
        .img-preview { height: 200px; object-fit: contain; background: #eee; cursor: pointer; }
        .copy-btn { cursor: pointer; }
        .folder-section { margin-bottom: 40px; }
        details summary { font-size: 1.5rem; font-weight: bold; cursor: pointer; padding: 10px; background: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        details[open] summary { margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-5">
            <h1>📂 Cloud-Assets 圖庫</h1>
            <a href="https://github.com/eric861129/Cloud-Assets" class="btn btn-outline-dark">GitHub 專案庫</a>
        </div>

        <div id="gallery">
            {content}
        </div>
    </div>

    <script>
        function copyToClipboard(text, btn) {
            navigator.clipboard.writeText(text).then(() => {
                const originalText = btn.innerText;
                btn.innerText = "✅ 已複製";
                btn.classList.replace("btn-outline-primary", "btn-success");
                btn.classList.replace("btn-outline-secondary", "btn-success");
                setTimeout(() => {
                    btn.innerText = originalText;
                    btn.classList.replace("btn-success", "btn-outline-primary");
                    btn.classList.replace("btn-success", "btn-outline-secondary");
                }, 2000);
            });
        }
    </script>
</body>
</html>
"""
    
    sections = []
    for folder in sorted(gallery_data.keys()):
        cards = []
        for filename in gallery_data[folder]:
            if folder == "Root (根目錄)":
                img_path = filename
            else:
                img_path = f"{folder}/{filename}"
            
            full_url = f"{CDN_BASE_URL}/{img_path}"
            md_code = f"![{filename}]({full_url})"
            
            card_html = f"""
            <div class="col-md-3 col-sm-6">
                <div class="card h-100">
                    <img src="{full_url}" class="card-img-top img-preview" alt="{filename}" loading="lazy" onclick="window.open('{full_url}')">
                    <div class="card-body">
                        <p class="card-text text-truncate" title="{filename}"><strong>{filename}</strong></p>
                        <div class="d-grid gap-2">
                            <button class="btn btn-sm btn-outline-primary copy-btn" onclick="copyToClipboard('{full_url}', this)">複製 CDN 連結</button>
                            <button class="btn btn-sm btn-outline-secondary copy-btn" onclick="copyToClipboard('{md_code}', this)">複製 Markdown</button>
                        </div>
                    </div>
                </div>
            </div>
            """
            cards.append(card_html)
        
        section = f"""
        <div class="folder-section">
            <details open>
                <summary>📁 {folder} ({len(gallery_data[folder])} 張)</summary>
                <div class="row g-3 mt-2">
                    {"".join(cards)}
                </div>
            </details>
        </div>
        """
        sections.append(section)

    final_html = html_template.replace("{content}", "".join(sections))
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_html)
    
    print("index.html 生成完畢。")

if __name__ == "__main__":
    optimize_images()
    # 重新掃描以獲取最新的 WebP 資訊
    current_gallery_data = {}
    for root, dirs, files in os.walk("."):
        if ".git" in root: continue
        webp_files = [f for f in files if f.lower().endswith(".webp")]
        if webp_files:
            rel_dir = os.path.relpath(root, ".").replace("\\", "/")
            if rel_dir == ".": rel_dir = "Root (根目錄)"
            current_gallery_data[rel_dir] = sorted(webp_files)
            
    generate_gallery(".") # 這裡內部其實已經做過一次掃描，為了架構清晰，我們稍微重構一下
    generate_index_html(current_gallery_data)
