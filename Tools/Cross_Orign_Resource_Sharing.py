import re
import requests

def check_cors_misconfiguration(url):
    print("Cross-Origin Resource Sharing (CORS) Misconfiguration Checker")
    # Ensure the URL starts with 'http://' or 'https://' if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url  # Default to HTTPS

    try:
        # Make a GET request to fetch the response headers
        response = requests.get(url)
        
        # Initialize result dictionary
        result = {
            "url": url,
            "vulnerable": False,
            "severity": "Low",
            "details": "CORS seems to be properly configured",
            "issues": []
        }

        # Check for presence of CORS headers
        cors_headers = {
            "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
            "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
            "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers"),
            "Access-Control-Allow-Credentials": response.headers.get("Access-Control-Allow-Credentials")
        }

        # Check Access-Control-Allow-Origin
        if cors_headers["Access-Control-Allow-Origin"] == "*":
            if "sensitive" in url or "api" in url:
                result["vulnerable"] = True
                result["severity"] = "High"
                result["issues"].append("Wildcard (*) ACAO header on potentially sensitive API")
            else:
                result["severity"] = "Medium"
                result["issues"].append("Wildcard (*) ACAO header detected")
        elif cors_headers["Access-Control-Allow-Origin"]:
            allowed_origins = cors_headers["Access-Control-Allow-Origin"].split(",")
            if len(allowed_origins) > 5:  # Arbitrary threshold, adjust as needed
                result["vulnerable"] = True
                result["severity"] = "Medium"
                result["issues"].append(f"Large number of allowed origins: {len(allowed_origins)}")
            for origin in allowed_origins:
                if origin.strip() == "null" or re.match(r"https?://.*", origin.strip()):
                    result["vulnerable"] = True
                    result["severity"] = "High"
                    result["issues"].append(f"Potentially unsafe origin allowed: {origin.strip()}")

        # Check Access-Control-Allow-Methods
        if cors_headers["Access-Control-Allow-Methods"]:
            methods = cors_headers["Access-Control-Allow-Methods"].split(",")
            unsafe_methods = set(methods) & {"PUT", "DELETE", "PATCH"}
            if unsafe_methods:
                result["vulnerable"] = True
                result["severity"] = "Medium"
                result["issues"].append(f"Potentially unsafe methods allowed: {', '.join(unsafe_methods)}")

        # Check Access-Control-Allow-Credentials
        if cors_headers["Access-Control-Allow-Credentials"] == "true":
            if cors_headers["Access-Control-Allow-Origin"] == "*":
                result["vulnerable"] = True
                result["severity"] = "High"
                result["issues"].append("Credentials allowed with wildcard origin")
            else:
                result["severity"] = "Medium"
                result["issues"].append("Credentials allowed, ensure origin is properly restricted")

        # Update details if vulnerabilities found
        if result["vulnerable"]:
            result["details"] = "CORS misconfiguration detected"
        print(f"Result for {result.get('url')}:")
        print(f"Vulnerable: {result['vulnerable']}")
        print(f"Severity: {result['severity']}")
        print(f"Details: {result['details']}")
        if result.get('issues'):
            print("Issues:")
            for issue in result['issues']:
                print(f"- {issue}")

        
        return result

    except requests.RequestException as e:
        return {"error": f"Error fetching the URL: {e}"}

if __name__ == "__main__":
    url = input("Enter the URL to check: ").strip()
    result = check_cors_misconfiguration(url)
    print(f"Result for {result.get('url')}:")
    print(f"Vulnerable: {result['vulnerable']}")
    print(f"Severity: {result['severity']}")
    print(f"Details: {result['details']}")
    if result.get('issues'):
        print("Issues:")
        for issue in result['issues']:
            print(f"- {issue}")
