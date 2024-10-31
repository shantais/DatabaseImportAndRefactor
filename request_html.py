import urllib.request
import urllib.error


def get_html(url):
    print('INFO: getting whole html from ' + url)

    try:
        with urllib.request.urlopen(url) as response:
            html_content = response.read().decode()
            # print(html_content)
            return html_content

    except urllib.error.URLError as e:
        print(f"An error occurred: {e}")
