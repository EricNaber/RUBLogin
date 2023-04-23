import argh
import requests


def get_credentials(path: str) -> dict:
    ''' Get file-path as input. 
        File should contain '<username>\n<password>\n'.
        Return Dict[String: String] containing username and password.
    '''
    with open(path, "r") as file:
        username = file.readline().strip()
        password = file.readline().strip()
    return {'username': username, 'password': password}


def login(url: str, credentials: dict):
    ''' Login on <url> with <credentials>
        Only working for RUB-login
    '''
    username, password = credentials["username"], credentials["password"]
    data = f"code=1&loginid={username}&password={password}&ipaddr=10.4.237.184&action=Login"
    response_text = requests.post(url, data).content.decode("utf-8")
    
    if "Authentisierung gelungen" in response_text:
        print(f"Successfully logged in as {username}")
    else:
        print(f"Failed to log in as {username}")


@argh.arg('login_path', help="Path to login credentials")
@argh.arg('url', default="https://login.ruhr-uni-bochum.de/cgi-bin/laklogin", help="URL to login-page")
def main(login_path, url):
    credentials = get_credentials(login_path)
    login(url, credentials)
    

if __name__=="__main__":
    try:
        argh.dispatch_command(main)
    except Exception as err:
        print(f"Something went wrong: {err}")
