import os
from PIL import Image

def optimize_images(directory=".", quality=80):
    for root, dirs, files in os.walk(directory):
        # 排除 .git 資料夾
        if ".git" in root:
            continue
            
        for filename in files:
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                filepath = os.path.join(root, filename)
                base = os.path.splitext(filename)[0]
                output_path = os.path.join(root, f"{base}.webp")
                
                try:
                    with Image.open(filepath) as img:
                        img.save(output_path, "WEBP", quality=quality, method=6)
                    print(f"優化成功: {filepath} -> {output_path}")
                except Exception as e:
                    print(f"處理 {filepath} 時出錯: {e}")

if __name__ == "__main__":
    optimize_images()
