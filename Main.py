from Tools.Directory_Listing import check_directory_listing as dir_listing #1
from Tools.Sensitive_data import check_sensitive_files as sensitive_files #2
from Tools.Know_server import get_server_info as server_info #3
from Tools.Missing_security_Headers import check_security_headers as security_headers #4
from Tools.Port_Scanner import run_port_scanner as port_scanner #5
from Tools.Insecure_Cookies import check_cookie_security as insecure_cookies #6
from Tools.Weak_SSL_TLS_Checker import check_ssl_tls as weak_ssl_tls #7
from Tools.Error_Message_Revealing import check_revealing_error_messages as error_messages #8
from Tools.Default_Settings import insecure_default_settings_checker as default_settings #9
from Tools.Cross_Orign_Resource_Sharing import check_cors_misconfiguration as cross_origin_resource_sharing #10
from Tools.Debug_Info import check_exposed_debug_info as debug_info #11
# from Tools.Insecure_Cookies import check_cookie_security as cookie_security #12
#from Tools.Unrestricted_File_Uploads import check_unrestricted_file_uploads as check_unrestricted_file_uploads; #12

if __name__ == "__main__":
    choice = {1: dir_listing, 2: sensitive_files, 3: server_info, 4: security_headers, 5: port_scanner,
              6: insecure_cookies,7: weak_ssl_tls,8: error_messages,9: default_settings, 10: cross_origin_resource_sharing,
        11: debug_info,} #12:check_unrestricted_file_uploads}
    
url = input("Enter the URL to check: ").strip().lower()
# Ensure the URL has a scheme
if not url.startswith('http://') and not url.startswith('https://'):
    url = 'https://' + url
print("Do you want full scan or custom scan? Press 1 for full scan or 2 for custom scan")
sel = int(input("Select: "))
if sel!= 1 and sel!= 2:
    print("Invalid option. Please try again.")
    exit()
loop = True
while loop:
    if sel == 1:
        for i in choice:
            choice[i](url)
    else:
        print("Select an option:")
        for key, value in choice.items():
            print(f"{key}: {value.__name__}")
        choose = list(map(int,input("Enter Your Choice With Space Seperated::  ").split()))
        print(choose)

        for i in choose:
            choice[int(i)](url)

    print("Scanning completed.")
    print("Do You Want TO Scan Again")
    print("Yes - 1")
    print("No - 2")
    again = int(input("Enter Your Choice "))
    if again == 1:
        loop = True
    elif again == 2:
        loop = False
    else:
        print("Invalid Option. Please Try Again.")
        exit()

    
