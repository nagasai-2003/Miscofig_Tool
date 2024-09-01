import requests

def check_directory_listing(url):
    print("Directory Listing Checker")
    # List of common directories that might reveal directory listing
    common_paths = [
    '/',
    '/index.html',
    '/default.html',
    '/default.asp',
    '/index.php',
    '/uploads/',
    '/files/',
    '/documents/',
    '/media/',
    '/attachments/',
    '/admin/',
    '/config/',
    '/cgi-bin/',
    '/manager/',
    '/webadmin/',
    '/backup/',
    '/old/',
    '/data/',
    '/dump/',
    '/archives/',
    '/temp/',
    '/test/',
    '/dev/',
    '/sandbox/',
    '/staging/',
    '/public/',
    '/static/',
    '/assets/',
    '/resources/',
    '/application/',
    '/app/',
    '/src/',
    '/lib/',
    '/includes/',
    '/plugins/',
    '/modules/',
    '/wordpress/',
    '/wp-content/',
    '/wp-admin/',
    '/drupal/',
    '/sites/',
    '/joomla/',
    '/mediawiki/',
    '/tests/',
    '/integration/',
    '/qa/',
    '/conf/',
    '/logs/',
    '/log/',
    '/settings/',
    '/configurations/',
    '/backups/',
    '/repository/',
    '/scripts/',
    '/bin/',
    '/cgi/',
    '/docs/',
    '/manual/',
    '/help/',
    '/tmp/',
    
    # Additional directories:
    
    # Framework-specific directories
    '/laravel/',
    '/codeigniter/',
    '/yii/',
    '/symfony/',
    '/zend/',
    '/cakephp/',

    # Database directories
    '/db/',
    '/database/',
    '/mysql/',
    '/postgres/',
    '/sql/',
    '/oracle/',

    # API directories
    '/api/',
    '/api/v1/',
    '/api/v2/',
    '/rest/',
    '/soap/',
    '/graphql/',

    # User directories
    '/users/',
    '/user/',
    '/profile/',
    '/account/',

    # Error directories
    '/error/',
    '/errors/',
    '/404/',
    '/500/',
    
    # Miscellaneous directories
    '/stats/',
    '/analytics/',
    '/reports/',
    '/charts/',
    '/graphs/',
    '/images/',
    '/videos/',
    '/audio/',
    '/fonts/',
    '/icons/',
    '/favicons/',
    '/img/',
    '/css/',
    '/js/',
    '/javascript/',
    '/styles/',
    '/theme/',
    '/skins/',
    '/cache/',
    '/downloads/',
    '/export/',
    '/imports/',
    '/newsletter/',
    '/mail/',
    '/smtp/',
    '/webmail/',
    '/sftp/',
    '/ssh/',
    '/telnet/',
    '/rpc/',
    '/xmlrpc/',
    '/ws/',
    '/svn/',
    '/git/',
    '/cvs/',
    '/bitbucket/',
    '/gitlab/',
    '/jenkins/',
    '/build/',
    '/ci/',
    '/live/',
    '/beta/',
    '/alpha/',
    '/legacy/',
    '/old_site/',
    '/new_site/',
    '/test_site/',
    '/dev_site/',

    # Newly Added Directories
    '/config_backup/',  # Backup configuration files
    '/old_versions/',  # Old versions of files or applications
    '/restore/',       # Restore points or backups
    '/uploads/temp/',  # Temporary upload files
    '/scripts/temp/',  # Temporary script files
    '/public_html/',   # Publicly accessible directory (common in shared hosting)
    '/private/',       # Private or sensitive information
    '/secure/',        # Secure or protected directories
    '/securefiles/',   # Directory for secure files
    '/maintenance/',   # Maintenance-related files or folders
    '/hidden/',        # Hidden or less obvious directories
    '/hidden_files/',  # Hidden files or directories
    '/settings_backup/', # Backup settings files

    # Additional Newly Added Directories
    '/cache_backup/',  # Backup for caching directories
    '/assets_backup/', # Backup for assets directories
    '/tmp_files/',     # Temporary files directory
    '/private_data/',  # Private or sensitive data
    '/server_backups/', # Server backup files
    '/local/',         # Local environment directories
    '/temp_files/',    # Temporary files
    '/logs_backup/',   # Backup for log files
    '/debug_logs/',    # Debugging log files
    '/test_data/',     # Test-related data directories
    '/app_data/',      # Application-specific data
    '/system/',        # System directories

     # Newly added directories
    '/vendor/',         # Common directory for dependencies in PHP projects
    '/node_modules/',   # Common directory for Node.js dependencies
    '/bower_components/', # Common directory for Bower dependencies
    '/dist/',           # Common directory for distributed files
    '/build/',          # Common directory for build output
    '/out/',            # Another common directory for build output
    '/coverage/',       # Common directory for test coverage reports
    '/migrations/',     # Common directory for database migrations
    '/seeds/',          # Common directory for database seeds
    '/cronjobs/',       # Directory for scheduled tasks
    '/tasks/',          # Another directory for scheduled or automated tasks
    '/batch/',          # Directory for batch processing files
    '/queue/',          # Directory related to job queues
    '/workers/',        # Directory related to background workers
    '/websockets/',     # Directory for WebSocket related files
    '/certificates/',   # Directory for SSL/TLS certificates
    '/keys/',           # Directory for cryptographic keys
    '/tokens/',         # Directory potentially containing access tokens
    '/sessions/',       # Directory for session data
    '/cookies/',        # Directory potentially containing cookie data
    '/temp_files/',     # Another temporary file directory
    '/uploads_old/',    # Old uploads directory
    '/configs_old/',    # Old configurations directory
    '/deprecated/',     # Directory for deprecated code or files
    '/experimental/',   # Directory for experimental features
    '/beta_features/',  # Directory for beta features
    '/alpha_features/', # Directory for alpha features
    '/prototypes/',     # Directory for prototype code or features
    '/sketches/',       # Directory potentially containing design sketches
    '/mockups/',        # Directory potentially containing design mockups
    '/wireframes/',     # Directory potentially containing wireframes
    '/locales/',        # Directory for internationalization files
    '/translations/',   # Another directory for language files
    '/i18n/',           # Common abbreviation for internationalization
    '/l10n/',           # Common abbreviation for localization
    '/blueprints/',     # Directory potentially containing application blueprints
    '/schemas/',        # Directory for database schemas
    '/fixtures/',       # Directory for test fixtures
    '/stubs/',          # Directory for stub files (often used in testing)
    '/mocks/',          # Directory for mock objects (often used in testing)
    '/containers/',     # Directory related to containerization (e.g., Docker)
    '/kubernetes/',     # Directory related to Kubernetes configurations
    '/ansible/',        # Directory for Ansible playbooks
    '/terraform/',      # Directory for Terraform configurations
    '/chef/',           # Directory for Chef recipes
    '/puppet/',         # Directory for Puppet manifests
    '/saltstack/',      # Directory for SaltStack states
    '/helm/',           # Directory for Helm charts (Kubernetes package manager)
    '/istio/',          # Directory for Istio service mesh configurations
    '/envoy/',          # Directory for Envoy proxy configurations
    '/nginx/',          # Directory for Nginx configurations
    '/apache/',         # Directory for Apache configurations
    '/iis/',            # Directory for IIS configurations
    '/tomcat/',         # Directory for Tomcat configurations
    '/jetty/',          # Directory for Jetty configurations
    '/rabbitmq/',       # Directory related to RabbitMQ
    '/kafka/',          # Directory related to Kafka
    '/redis/',          # Directory related to Redis
    '/memcached/',      # Directory related to Memcached
    '/elasticsearch/',  # Directory related to Elasticsearch
    '/solr/',           # Directory related to Solr
    '/cassandra/',      # Directory related to Cassandra
    '/mongodb/',        # Directory related to MongoDB
    '/neo4j/',          # Directory related to Neo4j
    '/grafana/',        # Directory related to Grafana
    '/prometheus/',     # Directory related to Prometheus
    '/kibana/',         # Directory related to Kibana
    '/logstash/',       # Directory related to Logstash
    '/fluentd/',        # Directory related to Fluentd
    '/nagios/',         # Directory related to Nagios
    '/zabbix/',         # Directory related to Zabbix
    '/splunk/',         # Directory related to Splunk
    '/sentry/',         # Directory related to Sentry
    '/newrelic/',       # Directory related to New Relic
    '/datadog/',        # Directory related to Datadog

     # Even More Newly Added Directories
   '/archive/',       # Archived files or data
   '/vault/',         # Secure storage for sensitive data
   '/protected/',    # Protected or restricted access directories
   '/restricted/',   # Restricted access directories
   '/confidential/', # Confidential or sensitive information
   '/internal/',     # Internal or non-public facing directories
   '/private_data/', # Private or sensitive data storage
   '/sensitive/',    # Sensitive or confidential information
   '/top_secret/',   # Highly sensitive or confidential information
   '/debug/',        # Debugging or testing directories
   '/experimental/', # Experimental or testing directories
   '/beta_testing/', # Beta testing directories
   '/alpha_testing/', # Alpha testing directories
   '/staging_area/', # Staging area for deployments or testing
   '/qa_environment/', # QA environment for testing
   '/dev_environment/', # Development environment for testing

   # FTP 
   '/ftp/',

   # WebDAV
   '/dav/',

]


    # Headers to avoid being mistaken for a bot
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Ensure the URL starts with 'http://' if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url  # Default to HTTPS


    for path in common_paths:
        full_url = url.rstrip('/') + path
        try:
            response = requests.get(full_url, headers=headers)
            if response.status_code == 200 and ('Index of' in response.text or 'Directory listing for' in response.text):
                print(f"Possible directory listing found at: {full_url}")
            else:
                print(f"No directory listing found at: {full_url}")
        except requests.RequestException as e:
            print(f"Error checking {full_url}: {e}")

if __name__ == "__main__":
    # Replace with the target website URL
    website_url = input("Enter the target website URL: ").strip()
    check_directory_listing(website_url)
