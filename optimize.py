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

if __name__ == "__main__":
    optimize_images()
    generate_gallery()
