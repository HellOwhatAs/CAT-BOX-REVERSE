import json
import os
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

def generate_data():
    json_path = '649821 猫箱反转.json'
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Clean up data to only what we need to safely expose
    comic_data = {
        "id": data.get("id"),
        "title": data.get("title"),
        "description": data.get("description"),
        "author": data.get("author"),
        "chapters": []
    }
    
    chapter_list = data.get("chapter_list", [])
    
    # Iterate and find folders
    for index, chapter in enumerate(chapter_list):
        chapter_index = index + 1
        # Construct folder name format: "0001 001 猫箱反转（上）"
        folder_prefix = f"{chapter_index:04d}"
        folder_name_candidate = f"{folder_prefix} {chapter['title']}"
        
        target_folder = None
        
        # Check if folder exists
        if os.path.exists(folder_name_candidate) and os.path.isdir(folder_name_candidate):
            target_folder = folder_name_candidate
        else:
             # Try to find folder starting with the prefix
            for f in os.listdir('.'):
                if f.startswith(folder_prefix) and os.path.isdir(f):
                    target_folder = f
                    break
        
        if target_folder:
            # Get images
            images = [f for f in os.listdir(target_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
            # Sort images naturally (1, 2, 10 instead of 1, 10, 2)
            images.sort(key=natural_sort_key)
            
            comic_data["chapters"].append({
                "index": chapter_index,
                "title": chapter["title"],
                "folderName": target_folder,
                "images": images  # Store actual filenames
            })
        else:
            print(f"Warning: Folder not found for chapter {index+1}: {folder_name_candidate}")
            comic_data["chapters"].append({
                "index": chapter_index,
                "title": chapter["title"],
                "folderName": None,
                "images": []
            })

    # Convert to JS file content
    js_content = f"const comicData = {json.dumps(comic_data, indent=2, ensure_ascii=False)};"
    
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print("data.js created successfully with explicit file lists.")

if __name__ == "__main__":
    generate_data()
