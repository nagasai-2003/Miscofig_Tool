import ssl
import socket
from urllib.parse import urlparse
import OpenSSL

def check_ssl_tls(url):
    print("Checking SSL/TLS...")
    # Ensure the URL starts with 'http://' if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url  # Default to HTTPS

    parsed_url = urlparse(url)
    hostname = parsed_url.netloc
    port = parsed_url.port or 443

    try:
        # Create a secure SSL context
        context = ssl.create_default_context()
        
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
                cert = secure_sock.getpeercert()
                cipher = secure_sock.cipher()
                version = secure_sock.version()

        # Check for weak protocols
        weak_protocols = ['SSLv2', 'SSLv3', 'TLSv1', 'TLSv1.1']
        if version in weak_protocols:
            print(f"[WARNING] Weak protocol detected: {version}")

        # Check for weak ciphers
        weak_ciphers = ['RC4', 'DES', '3DES', 'MD5']
        if any(weak in cipher[0] for weak in weak_ciphers):
            print(f"[WARNING] Weak cipher detected: {cipher[0]}")

        # Additional checks using pyOpenSSL
        cert = ssl.get_server_certificate((hostname, port))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        
        # Check certificate expiration
        if x509.has_expired():
            print("[WARNING] Certificate has expired")

        # Check key length
        pubkey = x509.get_pubkey()
        key_length = pubkey.bits()
        if key_length < 2048:
            print(f"[WARNING] Weak key length: {key_length} bits")

        print(f"Protocol: {version}")
        print(f"Cipher: {cipher[0]}")
        print(f"Key Length: {key_length} bits")
        print("SSL/TLS configuration appears to be secure.")

    except ssl.SSLError as e:
        print(f"SSL Error: {e}")
    except socket.gaierror:
        print(f"Error: Unable to resolve hostname '{hostname}'. Please check the URL.")
    except socket.error as e:
        print(f"Connection Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    url = input("Enter the URL to check: ").strip()
    check_ssl_tls(url)
