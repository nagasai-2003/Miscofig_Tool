import re
import requests
from urllib.parse import urlparse

def check_exposed_debug_info(url):
    print("Checking for exposed debug information...")
    # Ensure the URL starts with 'http://' or 'https://' if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url  # Default to HTTPS

    try:
        # Fetch the response content from the URL
        response = requests.get(url)
        response_content = response.text
        
        # Initialize flags
        debug_info_exposed = False
        exposed_elements = []

        # Parse the URL
        parsed_url = urlparse(url)

        # Check for common debug endpoints
        debug_endpoints = ['/debug', '/phpinfo.php', '/info.php', '/test.php', '/dev']
        if any(endpoint in parsed_url.path for endpoint in debug_endpoints):
            debug_info_exposed = True
            exposed_elements.append(f"Suspicious debug endpoint: {parsed_url.path}")

        # Check content for common debug information patterns
        debug_patterns = [
            r'<title>phpinfo\(\)</title>',
            r'PHP Version',
            r'System',
            r'Build Date',
            r'Server API',
            r'PHP Extensions',
            r'PHP Configuration',
            r'Environment',
            r'_SERVER\["[^"]+"\]',
            r'_ENV\["[^"]+"\]',
            r'DOCUMENT_ROOT',
            r'DEBUG:',
            r'VERBOSE:',
            r'Stack trace:',
            r'<pre>.*?Exception.*?</pre>'
        ]

        for pattern in debug_patterns:
            if re.search(pattern, response_content, re.IGNORECASE | re.DOTALL):
                debug_info_exposed = True
                exposed_elements.append(f"Debug info detected: {pattern}")

        # Check for development logs
        log_patterns = [r'\.log$', r'/logs/', r'/debug\.log', r'/error\.log', r'/access\.log']
        if any(re.search(pattern, parsed_url.path, re.IGNORECASE) for pattern in log_patterns):
            debug_info_exposed = True
            exposed_elements.append(f"Potential log file access: {parsed_url.path}")

        # Return results
        result = {
            "url": url,
            "vulnerable": debug_info_exposed,
            "severity": "High" if debug_info_exposed else "Low",
            "details": "Debug information exposed" if debug_info_exposed else "No obvious debug information exposed",
            "exposed_elements": exposed_elements if debug_info_exposed else []
        }
        print(f"Result: {result}")
        return result

    except requests.RequestException as e:
        print( "error", f"Error fetching the URL: {e}")
        return {"error", f"Error fetching the URL: {e}"}

if __name__ == "__main__":
    url = input("Enter the URL to check: ").strip()
    result = check_exposed_debug_info(url)
    print(f"Result: {result}")
