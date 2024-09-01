import requests

def check_security_headers(url):
    print("Security Headers Checker")

    # Ensure the URL has a scheme
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    essential_headers = {
    'Strict-Transport-Security': 'Ensures HTTPS usage',
    'X-Frame-Options': 'Protects against clickjacking',
    'X-Content-Type-Options': 'Prevents MIME type sniffing',
    'Content-Security-Policy': 'Mitigates various attacks, including XSS',
    'X-XSS-Protection': "Enables browser's built-in XSS protection",
    'Referrer-Policy': 'Controls the Referer header',
    'Permissions-Policy': 'Controls browser features and APIs',
    'Feature-Policy': 'Controls which features can be used by the website',
    'Cache-Control': 'Directs caching mechanisms in browsers and proxies',
    'Pragma': 'Backward compatibility for caching',
    'Access-Control-Allow-Origin': 'Specifies which domains can access resources',
    'Access-Control-Allow-Methods': 'Specifies allowed HTTP methods in CORS requests',
    'Access-Control-Allow-Headers': 'Specifies allowed headers in CORS requests',
    'Access-Control-Max-Age': 'Sets the maximum time for caching preflight request results',
    'X-Permitted-Cross-Domain-Policies': 'Controls data handling across domains',
    'Expect-CT': 'Helps detect and prevent misuse of SSL/TLS certificates',
    'Clear-Site-Data': 'Clears browsing data (cookies, storage, cache) associated with the website',
    'Cross-Origin-Embedder-Policy': 'Prevents a document from loading any cross-origin resources that don\'t explicitly grant the document permission',
    'Cross-Origin-Opener-Policy': 'Ensures a top-level document does not share a browsing context group with cross-origin documents',
    'Cross-Origin-Resource-Policy': 'Prevents other domains from reading the response of the resources to which this header is applied',
    'Public-Key-Pins': 'Prevents MITM attacks with forged certificates',
    'Server': 'Often recommended to be removed or obscured to avoid revealing server information',
    'X-Powered-By': 'Often recommended to be removed to avoid revealing technology stack',
    'X-Download-Options': 'Prevents Internet Explorer from executing downloads in the site\'s context',
    'X-DNS-Prefetch-Control': 'Controls browser DNS prefetching',
    'Set-Cookie': 'Sets an HTTP cookie with security attributes',
}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Checking security headers for {url}\n")

        missing_headers = []
        for header, description in essential_headers.items():
            if header not in response.headers:
                missing_headers.append(f"{header}: {description}")

        if missing_headers:
            print("Missing essential security headers:")
            for header in missing_headers:
                print(f"- {header}")
        else:
            print("All essential security headers are present.")

        print("\nCurrent headers:")
        for header, value in response.headers.items():
            print(f"{header}: {value}")

    except requests.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    website = input("Enter the website URL to check: ")
    check_security_headers(website)