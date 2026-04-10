import os

def replace_in_file(filepath, old_str, new_str):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_str in content or "CryptoVault" in content:
        content = content.replace(old_str, new_str)
        # Also replace standalone CryptoVault with CryptoVault
        content = content.replace("CryptoVault", "CryptoVault")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        if 'venv' in root or '.git' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith(('.py', '.html', '.js', '.css', '.md')):
                replace_in_file(os.path.join(root, file), "CryptoVault", "CryptoVault")

process_directory('.')
