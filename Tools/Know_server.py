import requests
def get_server_info(base_url):
    print(f"Getting server information for {base_url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Ensure the URL includes a scheme
    if not base_url.startswith(('http://', 'https://')):
        base_url = 'http://' + base_url

    try:
        response = requests.get(base_url, headers=headers, allow_redirects=False)
        server_info = {
            'Server': response.headers.get('Server', 'Not found'),
            'X-Powered-By': response.headers.get('X-Powered-By', 'Not found'),
            'Server-Version': 'Unknown',
            'Additional-Info': None
        }

        # Extract server version if present
        if server_info['Server']:
            parts = server_info['Server'].split('/')
            if len(parts) > 1:
                server_info['Server-Version'] = parts[1]

        # Check known status pages for additional details
        status_pages = {
            'apache': '/server-status',
            'nginx': '/nginx_status',
            'iis': '/iisreset',
            'lighttpd': '/server-status'
        }

        for server_type, status_page in status_pages.items():
            if server_info['Server'].lower().startswith(server_type):
                status_url = base_url.rstrip('/') + status_page
                try:
                    status_response = requests.get(status_url, headers=headers)
                    if status_response.status_code == 200:
                        server_info['Additional-Info'] = f"Contents of {status_page}: {status_response.text[:500]}..."
                except requests.RequestException as e:
                    server_info['Additional-Info'] = f"Error retrieving status page: {e}"
                break

        # Print server information
        print("Server Information:")
        print(f"Server: {server_info['Server']}")
        print(f"X-Powered-By: {server_info['X-Powered-By']}")
        print(f"Server Version: {server_info['Server-Version']}")
        if server_info['Additional-Info']:
            print(f"Additional Info: {server_info['Additional-Info']}")
        else:
            print("No additional server details found.")
        
    except requests.RequestException as e:
        print(f"[ERROR] Unable to retrieve server information - Exception: {e}")


if __name__ == "__main__":
    base_url = input("Enter the base URL of the website: ").strip()
    get_server_info(base_url)
    