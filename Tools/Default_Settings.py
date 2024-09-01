import re
import requests

def insecure_default_settings_checker(url):
    print("Checking for the Insecure Defaut Settings")
    print("Insecure Default Settings Checker")

    # Ensure the URL has a scheme
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url  # Default to HTTPS

    try:
        response = requests.get(url)
        server_info = response.headers.get("Server", "Unknown Server")
        server_headers = response.headers

        # In a real scenario, the following server_config would require a way to fetch actual server settings
        server_config = {
            "DirectoryListing": "Off",  # Assume default setting
            "SSLProtocol": "TLSv1.2 TLSv1.3",  # Assume secure defaults
            "TraceEnable": "Off"  # Assume default setting
        }

        vulnerabilities = []
        severity = "Low"

        # Check server software and version
        if server_info:
            server_match = re.search(r"(\w+)(?:/(\d+\.\d+\.\d+))?", server_info)
            if server_match:
                server_name, server_version = server_match.groups()
                vulnerabilities.append(f"Server software exposed: {server_name}")
                if server_version:
                    vulnerabilities.append(f"Server version exposed: {server_version}")
                    severity = "Medium"

        # Check for common insecure headers
        insecure_headers = {
            "X-Powered-By": "Technology stack exposed",
            "Server": "Detailed server information exposed",
            "X-AspNet-Version": ".NET version exposed",
            "X-AspNetMvc-Version": "ASP.NET MVC version exposed"
        }

        for header, description in insecure_headers.items():
            if header in server_headers:
                vulnerabilities.append(f"{description}: {server_headers[header]}")
                severity = "Medium"

        # Check for missing security headers
        security_headers = [
            "Strict-Transport-Security",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Content-Security-Policy",
            "X-XSS-Protection"
        ]

        for header in security_headers:
            if header not in server_headers:
                vulnerabilities.append(f"Missing security header: {header}")
                severity = "High"

        # Check server configuration
        if server_config.get("DirectoryListing") == "On":
            vulnerabilities.append("Directory listing enabled")
            severity = "High"

        if "SSLProtocol" in server_config:
            ssl_protocols = server_config["SSLProtocol"].split()
            insecure_protocols = set(ssl_protocols) & {"SSLv2", "SSLv3", "TLSv1", "TLSv1.1"}
            if insecure_protocols:
                vulnerabilities.append(f"Insecure SSL/TLS protocols enabled: {', '.join(insecure_protocols)}")
                severity = "High"

        if server_config.get("TraceEnable") == "On":
            vulnerabilities.append("HTTP TRACE method enabled")
            severity = "Medium"

        # Determine overall severity
        if not vulnerabilities:
            severity = "Low"
        elif any("High" in vuln for vuln in vulnerabilities):
            severity = "High"
        elif any("Medium" in vuln for vuln in vulnerabilities):
            severity = "Medium"

        # Display results
        print(f"\nResult:")
        print(f"Vulnerable: {bool(vulnerabilities)}")
        print(f"Severity: {severity}")
        if vulnerabilities:
            print("Vulnerabilities:")
            for vuln in vulnerabilities:
                print(f"- {vuln}")
        else:
            print("No vulnerabilities detected.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")

if __name__ == "__main__":
    url = input("Enter website URL (e.g., 'example.com'): ").strip()
    insecure_default_settings_checker(url)
