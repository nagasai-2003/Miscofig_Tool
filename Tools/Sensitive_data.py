import requests

def check_sensitive_files(url):
    print("Sensitive Files Checker")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    found_files = []

    # List of sensitive files to check
    sensitive_files = [
    # Git-related files
    '.git/',
    '.git/config',
    '.git/HEAD',
    '.git/index',
    '.git/objects/',
    '.git/refs/',
    '.gitignore',
    '.gitattributes',
    '.gitmodules',

    # Configuration files
    'config.php',
    'config.inc.php',
    'wp-config.php',
    'web.config',
    'db_config.php',
    'settings.py',
    'config.json',
    'secrets.yml',
    'secrets.json',
    'config.local.php',
    'config.dev.php',
    'config.production.php',
    'database.yml',
    'settings.local.php',
    'database.php',
    'database.ini',
    'env.example',
    '.env.local',
    '.env',
    '.env.backup',
    '.env.dev',
    '.env.prod',
    'config.xml',
    'configuration.php',

    # Application-specific files
    'application.yml',
    'application.json',
    'appsettings.json',
    'appsettings.Development.json',
    'appsettings.Production.json',
    'composer.json',
    'package.json',
    'yarn.lock',
    'Gemfile',
    'requirements.txt',

    # System and environment files
    '.htaccess',
    '.bash_history',
    '.bashrc',
    '.profile',
    '.zshrc',
    '.ssh/id_rsa',
    '.ssh/id_dsa',
    '.ssh/id_ecdsa',
    '.ssh/id_ed25519',
    '.ssh/authorized_keys',
    '.bash_profile',
    '.inputrc',

    # Logs and backups
    'error.log',
    'access.log',
    'debug.log',
    'backup.sql',
    'backup.tar.gz',
    'backup.zip',
    'dump.sql',
    'database.sql',
    'backup.tar',
    'backup.sql.gz',
    'app.log',
    'server.log',
    'auth.log',

    # PHP and other language-specific
    'phpinfo.php',
    'info.php',
    'configurator.php',
    'install.php',
    'setup.php',
    'update.php',

    # Credentials and secrets
    'private.key',
    'public.key',
    'secrets.txt',
    'credentials.txt',
    'auth.txt',
    'user_secrets.txt',
    'secure_data.txt',
    'id_rsa',
    'id_dsa',
    'id_ecdsa',
    'id_ed25519',
    'oauth_token.json',
    'oauth.json',
    'api_secret.key',
    'oauth_secrets.txt',
    
    # Server Configuration
    'httpd.conf',
    'nginx.conf',
    'server.cfg',
    '.htpasswd',

    # CMS and Framework Files
    'wp-content/debug.log',
    'configuration.php',  # Joomla
    'config/database.yml',  # Ruby on Rails
    'app/config/parameters.yml',  # Symfony
    'local_settings.py',  # Django

    # Development and Debug Files
    'test.php',
    'debug.php',
    '.DS_Store',
    'Thumbs.db',

    # API Keys and Tokens
    'google_api_key.txt',
    'aws_credentials.txt',
    'stripe_api_key.txt',

    # Docker and Kubernetes
    'Dockerfile',
    'docker-compose.yml',
    'docker-compose.override.yml',
    'docker-compose.prod.yml',
    'docker-compose.dev.yml',
    'kubectl.conf',
    'kubeconfig',

    # Jenkins
    'jenkins.xml',
    'jenkins.plugins.publish_over_ssh.BapSshPublisherPlugin.xml',

    # Miscellaneous
    'robots.txt',
    'sitemap.xml',
    'crossdomain.xml',
    'clientaccesspolicy.xml',
    'phpMyAdmin/',
    'phpmyadmin/',
    'adminer.php',

    # More advanced targets
    '.well-known/security.txt',
    '.vscode/sftp.json',
    'sftp-config.json',
    'filezilla.xml',
    'WS_FTP.ini',
    'winscp.ini',
    'known_hosts',
    'id_rsa.pub',
    'config.gypi',
    'npm-debug.log',
    'yarn-error.log',
    'lerna-debug.log',

    # Infrastructure as Code (IaC) files
    'terraform.tfvars',
    'terraform.tfstate',
    '.terraform/',
    'ansible.cfg',
    'playbook.yml',
    'inventory.ini',
    'vault_pass.txt',

    # Distributed systems files
    'consul-config.json',
    'consul-data/',
    'etcd-data/',
    'zookeeper.out',
    'zookeeper-data/',
    'kafka-logs/',

    # Database configuration files
    'elasticsearch.yml',
    'kibana.yml',
    'logstash.conf',
    'redis.conf',
    'mongod.conf',

    # Server configuration files
    'supervisord.conf',
    'ngnix_status',
    'server-status',

    # Additional Version Control
    '.bzr/',

    # Additional Configuration Files
    'application.properties',
    'Pipfile',
    'poetry.lock',

    # Additional Logs
    'app.log',
    'server.log',
    'auth.log',

    # Additional Server Configuration
    'apache2.conf',
    'lighttpd.conf',
    'php.ini',
    'my.cnf',

    # Additional Development and Debug Files
    'Thumbs.db',

    # Additional Docker and Kubernetes
    '.dockerignore',

    # Additional CI/CD
    '.gitlab-ci.yml',
    '.travis.yml',
    'circle.yml',
    'appveyor.yml',
    'Jenkinsfile',

    # Additional Miscellaneous
    'README.md',
    'CHANGELOG.md',
    'LICENSE',

    # Cloud Service Provider
    'credentials',  # AWS
    'config',       # AWS
    'gcloud.json',  # Google Cloud
    'azureauth.json', # Azure

    # Frontend Build
    'dist/',
    'build/',
    'node_modules/',

    # Caches
    '.cache/',
    '__pycache__/',
    '*.pyc',

    # IDE and Editor Files
    '.idea/',
    '*.swp',
    '*.swo',
    '*.sublime-project',
    '*.sublime-workspace',

    # Temporary Files
    'tmp/',
    'temp/',
    '*.tmp',
    '*.bak',

    # Certificate Files
    '*.pem',
    '*.crt',
    '*.cer',
    '*.p12',
    '*.pfx',

    # Database Files
    '*.sqlite',
    '*.db',
    '*.mdb',

    # Compiled Binaries
    '*.exe',
    '*.dll',
    '*.so',
    '*.dylib',

    # Mobile App Development
    'google-services.json',  # Android
    'GoogleService-Info.plist',  # iOS

    # Blockchain and Cryptocurrency
    'wallet.dat',
    'keystore/',

    # Machine Learning
    'model.h5',
    'model.pkl',
    'checkpoint',

    # Internal Documentation
    'INTERNAL.md',
    'TODO.md',
    'NOTES.txt',

    # Additional Configuration Files
    'authconfig.yml',             # Authentication configuration
    'keystore.jks',              # Java KeyStore
    'truststore.jks',            # Java TrustStore
    'ssl_certificate.crt',       # SSL certificate
    'ssl_certificate.key',       # SSL private key
    'private_key.pem',           # Private key in PEM format
    'public_key.pem',            # Public key in PEM format
    'security_config.json',      # Security configuration in JSON format
    'service_account.json',      # Service account credentials
    'client_secret.json',        # Client secrets in JSON format
    'api_secret.key',            # API secret key
    'oauth_secrets.txt',         # OAuth secrets
    'keytab',                    # Kerberos keytab file
    'jceks',                     # Java Cryptography Extension KeyStore
    'kube-apiserver',            # Kubernetes API server configuration
    'kube-controller-manager',   # Kubernetes controller manager configuration
    'kube-scheduler',            # Kubernetes scheduler configuration
    'vault/',                    # HashiCorp Vault directory
    'vault-config.hcl',          # HashiCorp Vault configuration file
    'gpg-keys/',                 # GPG keys directory
    'gpg-config/',              # GPG configuration directory
    'ssh_config',                # SSH configuration file
    'ssh_host_rsa_key',          # SSH RSA host key
    'ssh_host_dsa_key',          # SSH DSA host key
    'ssh_host_ecdsa_key',        # SSH ECDSA host key
    'ssh_host_ed25519_key',      # SSH Ed25519 host key
    'user_passwd',               # User password file
    'user_shadow',               # Shadow password file
    'ssl_certificates/',         # SSL certificates directory
    'ssl_keys/',                 # SSL keys directory
]
    for file in sensitive_files:
        test_url = url.rstrip('/') + '/' + file.lstrip('/')
        # Ensure the URL starts with 'http://' or 'https://'
        if not test_url.startswith(('http://', 'https://')):
            test_url = 'https://' + test_url  # Default to HTTPS
        
        try:
            print(f"Checking URL: {test_url}")  # Debug print statement
            response = requests.get(test_url, headers=headers)
            if response.status_code == 200:
                print(f"[FOUND] {test_url} - Status Code: {response.status_code}")
                found_files.append(test_url)
            else:
                print(f"[NOT FOUND] {test_url} - Status Code: {response.status_code}")
        except requests.RequestException as e:
            print(f"[ERROR] {test_url} - Exception: {e}")

    # Print found files at the end
    if found_files:
        print("\nSensitive files found:")
        for file_url in found_files:
            print(file_url)
    else:
        print("\nNo sensitive files found.")

