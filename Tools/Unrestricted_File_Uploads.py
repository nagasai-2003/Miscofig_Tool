import os
import re
import requests
from urllib.parse import urlparse

def check_unrestricted_file_uploads(url):
    # Configuration
    UPLOAD_FOLDER = '/tmp/uploads'
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.pdf'}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

    # Ensure the upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    def allowed_file(filename):
        return os.path.splitext(filename.lower())[1] in ALLOWED_EXTENSIONS

    def check_file_content(file_path):
        file_extension = os.path.splitext(file_path.lower())[1]
        
        # Check if file has a safe extension
        if file_extension not in ALLOWED_EXTENSIONS:
            return False, f"File type not allowed: {file_extension}"

        with open(file_path, 'rb') as f:
            content = f.read()

        # Check for potential malicious patterns
        malicious_patterns = [
            b"<\?php",
            b"<script",
            b"eval(",
            b"system(",
            b"exec("
        ]

        for pattern in malicious_patterns:
            if re.search(pattern, content):
                return False, f"Potential malicious content detected: {pattern.decode(errors='ignore')}"
        
        return True, "File content looks safe"

    # Prepend 'http://' if the URL does not have a scheme
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = 'http://' + url

    try:
        # Simulate file upload by reading from a URL
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            file_size = int(response.headers.get('Content-Length', 0))

            if file_size > MAX_FILE_SIZE:
                return {"error": "File size exceeds the limit"}, 400
            
            filename = os.path.join(UPLOAD_FOLDER, os.path.basename(url))
            with open(filename, 'wb') as f:
                f.write(response.content)

            content_safe, message = check_file_content(filename)

            if not content_safe:
                os.remove(filename)  # Remove the unsafe file
                return {"error": message}, 400
            #print(f"Result: {result}")
            
            return {"message": "File uploaded successfully", "filename": os.path.basename(url)}, 200
        else:
            return {"error": "Failed to fetch the file from the URL"}, response.status_code
        

    except Exception as e:
        return {"error": str(e)}, 500

# Example usage
if __name__ == '__main__':
    url = input("Enter the file URL to upload: ").strip()
    result, status_code = check_unrestricted_file_uploads(url)
    
    print(f"Result: {result}")
