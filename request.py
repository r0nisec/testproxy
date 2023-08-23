import requests

def read_proxy_file(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file]

proxy_list = read_proxy_file("proxy.txt")

# Create a session to persist cookies and settings across requests
session = requests.Session()

def make_request(url):
    global proxy_list
    proxy = proxy_list.pop(0)  # Get the first proxy from the list
    proxy_list.append(proxy)   # Move the used proxy to the end of the list

    try:
        response = session.get(url, proxies={"http": proxy, "https": proxy}, timeout=10)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        return response.content
    except requests.RequestException as e:
        print(f"Request error using proxy {proxy}: {e}")
        return None

if __name__ == "__main__":
    target_url = "https://www.ubaldi.com/p/Js74kxh"
    for _ in range(len(proxy_list)):
        response_content = make_request(target_url)
        if response_content:
            print(response_content)
            break
    else:
        print("All proxies failed.")
