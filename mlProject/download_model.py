import gdown
import os

# Google Drive file ID (replace with your actual file ID)
file_id = "1Y8-J68g3V0iPkzROftx7qEHjqejele5-"
url = f"https://drive.google.com/uc?id={file_id}"

# Output path
output_path = "mlProject/similarity.pkl"

# Check if the file already exists
if not os.path.exists(output_path):
    print("Downloading similarity.pkl from Google Drive...")
    gdown.download(url, output_path, quiet=False)
    print("Download complete!")
else:
    print("similarity.pkl already exists. No need to download.")
