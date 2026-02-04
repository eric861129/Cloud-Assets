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
    掃描所有 WebP 圖片並生成 GALLERY.md 索引檔。
    """
    print("正在生成 GALLERY.md ...")
    
    lines = ["# 📂 圖片索引 (Gallery)", "", "自動生成的圖片清單，包含 CDN 連結與引用語法。", ""]
    
    # 收集所有 webp 檔案
    images = []
    for root, dirs, files in os.walk(directory):
        if ".git" in root:
            continue
        for filename in files:
            if filename.lower().endswith(".webp"):
                # 取得相對路徑，並將 Windows 反斜線換成正斜線
                rel_path = os.path.relpath(os.path.join(root, filename), directory).replace("\\", "/")
                images.append(rel_path)
    
    # 排序 (讓最新的圖片可能排在某個順序，這裡先用路徑排序)
    images.sort()
    
    if not images:
        lines.append("目前沒有圖片。")
    else:
        for img_path in images:
            # 建立各種連結格式
            full_url = f"{CDN_BASE_URL}/{img_path}"
            filename = os.path.basename(img_path)
            
            lines.append(f"## 🖼️ {filename}")
            lines.append(f"![{filename}]({full_url})")
            lines.append("")
            lines.append("| 類型 | 語法 (點擊複製) |")
            lines.append("| :--- | :--- |")
            lines.append(f"| **CDN Link** | `{full_url}` |")
            lines.append(f"| **Markdown** | `![{filename}]({full_url})` |")
            lines.append(f"| **HTML** | `<img src=\"{full_url}\" alt=\"{filename}\" loading=\"lazy\">` |")
            lines.append("")
            lines.append("---")
            lines.append("")

    with open("GALLERY.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"GALLERY.md 生成完畢，共收錄 {len(images)} 張圖片。")

if __name__ == "__main__":
    optimize_images()
    generate_gallery()
