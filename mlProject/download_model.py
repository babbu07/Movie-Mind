import gdown
import os

# Google Drive file ID (replace with your actual file ID)
file_id = "1Y8-J68g3V0iPkzROftx7qEHjqejele5-"
url1 = f"https://drive.google.com/uc?id={file_id}"
url2 = "https://drive.google.com/file/d/1cHROLPXs06irUICHfuOmwIKs4MYXI19b/view?usp=drive_link"
url3 = "https://drive.google.com/file/d/1kswSeoG6DIIY57eFVKpkO10yDzIHycEv/view?usp=drive_link"

# Output path
output_path1 = "mlProject/similarity.pkl"
output_path2 = "embeddingTitle.pkl"
output_path3 = "titleFindingModel.pkl"

# Check if the file already exists
if not os.path.exists(output_path1):
    print("Downloading similarity.pkl from Google Drive...")
    gdown.download(url1, output_path1, quiet=False)
else:
    print("similarity.pkl already exists. No need to download.")
    
if not os.path.exists(output_path2):
    print("Downloading embeddingTitle.pkl file...")
    gdown.download(url2, output_path2, quiet=False)
else:
    print("embeddingTitle.pkl already exists. No need to download.")

if not os.path.exists(output_path3):
    print("Downloading titleFindingModel.pkl file...")
    gdown.download(url3, output_path3, quiet=False)
else:
    print("titleFindingModel.pkl already exists. No need to download.")