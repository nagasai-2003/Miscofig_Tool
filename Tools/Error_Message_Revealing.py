import requests
import re
from urllib.parse import urlparse

def check_revealing_error_messages(url):
    print("Checking for revealing error messages...")
    
    # Ensure the URL starts with 'http://' or 'https://' if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url  # Default to HTTPS

    # Define common endpoints to check for error messages
    endpoints = [
        "/nonexistentpage",
        "/test",
        "/404",
        "/error",
        "/admin",
        "/api/v1/resource"  # Add relevant API endpoints here
    ]

    # Patterns that might indicate sensitive information in error messages
    sensitive_patterns = [
        r"stack trace",
        r"database error",
        r"server (info|details)",
        r"(username|password) incorrect",
        r"internal server error",
        r"debug (info|mode)",
        r"(file|directory) not found: /",
    ]

    found_errors = []

    for endpoint in endpoints:
        full_url = url + endpoint
        try:
            response = requests.get(full_url)
            # Check for 4xx and 5xx responses
            if response.status_code >= 400:
                found_errors.append((full_url, response.status_code, response.text))
        except requests.RequestException as e:
            print(f"Error checking {full_url}: {e}")

    # Print results and analyze error messages
    if found_errors:
        print("Potential error messages revealing sensitive information found:")
        for url, status_code, error_message in found_errors:
            print(f"[WARNING] URL: {url} | Status Code: {status_code}")
            print(f"Error Message Snippet: {error_message[:100]}...")  # Show a snippet of the error message
            
            # Check for sensitive information in the error message
            sensitive_info_found = any(re.search(pattern, error_message, re.IGNORECASE) for pattern in sensitive_patterns)
            if sensitive_info_found:
                print("Warning: Error message may reveal sensitive information. Please review and sanitize.")
            else:
                print("Error message appears to be safe.\n")
    else:
        print("No revealing error messages found.")

if __name__ == "__main__":
    target_url = input("Enter the website URL to check for revealing error messages: ").strip()
    check_revealing_error_messages(target_url)
