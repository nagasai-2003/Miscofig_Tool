import requests
from urllib.parse import urlparse
from http.cookiejar import Cookie

def check_cookie_security(url):
    print("Checking cookie security...")
    def analyze_cookie(cookie):
        issues = []
        details = []

        # Check Secure flag
        if not cookie.secure:
            issues.append("Not set to secure (HTTPS only)")
        details.append(f"Secure: {'Yes' if cookie.secure else 'No'}")

        # Check HttpOnly flag
        if not cookie.has_nonstandard_attr('HttpOnly'):
            issues.append("Missing HttpOnly flag")
        details.append(f"HttpOnly: {'Yes' if cookie.has_nonstandard_attr('HttpOnly') else 'No'}")

        # Check SameSite attribute
        samesite = cookie.get_nonstandard_attr('SameSite')
        if not samesite:
            issues.append("Missing SameSite attribute")
            details.append("SameSite: Not set")
        elif samesite.lower() not in ['strict', 'lax']:
            issues.append(f"Weak SameSite value: {samesite}")
            details.append(f"SameSite: {samesite}")
        else:
            details.append(f"SameSite: {samesite}")

        # Check domain
        if cookie.domain_specified and cookie.domain.startswith('.'):
            issues.append(f"Overly broad domain: {cookie.domain}")
        details.append(f"Domain: {cookie.domain if cookie.domain else 'Not specified'}")

        # Check path
        details.append(f"Path: {cookie.path}")

        # Check expiration
        if cookie.expires:
            from datetime import datetime
            expiry_date = datetime.fromtimestamp(cookie.expires)
            details.append(f"Expires: {expiry_date}")
        else:
            details.append("Expires: Session cookie")

        return issues, details

    try:
        # Ensure the URL has a scheme
        if not urlparse(url).scheme:
            url = 'https://' + url

        # Send a GET request to the website
        response = requests.get(url, allow_redirects=True, timeout=10)
        
        # Analyze cookies
        results = []
        for cookie in response.cookies:
            issues, details = analyze_cookie(cookie)
            results.append({
                'name': cookie.name,
                'issues': issues,
                'details': details
            })

        # Print results
        if not results:
            print("No cookies found on this website.")
        else:
            print(f"Found {len(results)} cookie(s):")
            for result in results:
                print(f"\nCookie: {result['name']}")
                if result['issues']:
                    print("Issues:")
                    for issue in result['issues']:
                        print(f"- {issue}")
                print("Details:")
                for detail in result['details']:
                    print(f"- {detail}")

        return results

    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        return [{'name': 'Connection Error', 'issues': [str(e)], 'details': []}]

if __name__ == "__main__":
    url = input("Enter the website URL to check for cookie security: ")
    check_cookie_security(url)