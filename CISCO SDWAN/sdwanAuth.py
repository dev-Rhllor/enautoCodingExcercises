import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def authentication(vmanage_host, vmanage_port, username, password):
    api = '/j_security_check'
    base_url = f'https://{vmanage_host}:{vmanage_port}'
    url = base_url + api
    # Header Content-Type: application/x-www-form-urlencoded
    payload = {'j_username': username,
               'j_password': password}
    response = requests.post(url=url,
                             data=payload,
                             verify=False)
    try:
        cookies = response.headers["Set-Cookie"]
        jsessionid = cookies.split(";")
    except KeyError:
        print("No valid JSESSION ID returned\n")
        return False
    # Get the token with the cookie
    headers = {'Cookie': jsessionid[0]}
    api = "/dataservice/client/token"
    url = base_url + api
    response = requests.get(url=url,
                            headers=headers,
                            verify=False)
    if response.status_code == 200:
        token = response.text
        headers = {'Content-Type': "application/json",
                   'Cookie': jsessionid[0],
                   'X-XSRF-TOKEN': token}
        return headers
    else:
        return False
