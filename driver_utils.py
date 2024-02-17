from platform import platform, architecture
from bs4 import BeautifulSoup
from requests import get
from os.path import realpath, join, dirname, exists
from os import makedirs
from os import remove, system
import sys
import zipfile


### GET ARCHITECTURE ###
def get_os():
    plat = platform().lower()
    if plat.startswith('darwin') or plat.startswith('macos'):
        return 'mac'
    elif plat.startswith('linux'):
        return 'linux'
    elif plat.startswith('win'):
        return 'win'

def get_os_and_architecture():
    plat = platform().lower()
    if plat.startswith('darwin') or plat.startswith('macos'):
        os = 'mac'
        # Only 64 bit architecture is available for mac since version 2.23
        if 'x' in plat:
            arch = 'x64'
        else:
            arch = 'arm64'
    elif plat.startswith('linux'):
        os = 'linux'
        arch = architecture()[0][:-3]
    elif plat.startswith('win'):
        os = 'win'
        arch = '32'
    else:
        raise Exception('Unsupported platform: {0}'.format(plat))
    return os, arch


### ENV PATHS ###

def drivers_dir():
    pth = realpath(join(WD, '../binaries/'))
    if not exists(pth):
        makedirs(pth)
    return pth

WD = dirname(__file__)
CHROMIUM_ZIP_PATH = join(f'{drivers_dir()}/chrome-{get_os()}.zip')
CHROMEDRIVER_ZIP_PATH = join(f'{drivers_dir()}/chromedriver-{get_os()}.zip')


### DOWNLOAD PROPER CHROME VERSION ###

chrome_git_labs = 'https://googlechromelabs.github.io/chrome-for-testing/'


def get_chrome_drivers_stable_version():
    import requests
    response = requests.get(chrome_git_labs)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        stable_version = soup.find('code')  # by default it will be first value -> what we are looking for
        return stable_version.text
    else:
        print(f'Chrome Lab is response with code {response.status_code}.')

def chrome_url_builder():
    os, arch = get_os_and_architecture()
    version = get_chrome_drivers_stable_version()
    if os == 'mac':
        url = f'{chrome_git_labs}{version}/{os}-{arch}/chrome-{os}-{arch}.zip'
    else:
        url = f'{chrome_git_labs}{version}/{os}{arch}/chrome-{os}{arch}.zip'
    return url

def chromedriver_url_builder():
    os, arch = get_os_and_architecture()
    version = get_chrome_drivers_stable_version()
    if os == 'mac':
        url = f'{chrome_git_labs}{version}/{os}-{arch}/chromedriver-{os}-{arch}.zip'
    else:
        url = f'{chrome_git_labs}{version}/{os}{arch}/chromedriver-{os}{arch}.zip'
    return url

def download_chromium():
    version = get_chrome_drivers_stable_version()
    print(f'\033[94mStarting downloading Chromium version {version}\n\r')
    url = chrome_url_builder()
    resp = get(url=url, stream=True)
    print(f'\033[94m Downloading Chromium from {url}\n\r')
    with open(CHROMIUM_ZIP_PATH, 'wb') as f:
            total_length = resp.headers.get('content-length')
            dl = 0
            total_length = int(total_length)
            for data in resp.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.flush()
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                sys.stdout.flush()
    print('\n')
    print('\033[92m Chromium downloaded.\n\033[0m')

def download_chromedriver():
    version = get_chrome_drivers_stable_version()
    print(f'\033[94mStarting downloading Chromedriver version {version}\n\r')
    url = chromedriver_url_builder()
    resp = get(url=url, stream=True)
    print(f'\033[94m Downloading Chromedriver from {url}\n\r')
    with open(CHROMEDRIVER_ZIP_PATH, 'wb') as f:
            total_length = resp.headers.get('content-length')
            dl = 0
            total_length = int(total_length)
            for data in resp.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.flush()
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                sys.stdout.flush()
    print('\n')
    print('\033[92m Chromedriver downloaded.\n\033[0m')

def unzip_chromium():
    print(f'\033[94m Extracting Chromium\n\033[0m')
    if 'mac' or 'linux' in get_os():
        system(f"unzip -q -o {CHROMIUM_ZIP_PATH} -d {dirname(drivers_dir())}/binaries/")
        print(f'\033[94m Chromium extracted to {dirname(drivers_dir())}\n\033[0m')
    else:
        zf = zipfile.ZipFile(CHROMIUM_ZIP_PATH)
        zf.extractall(dirname(CHROMIUM_ZIP_PATH))
    remove(CHROMIUM_ZIP_PATH)

def unzip_chromedriver():
    print(f'\033[94m Extracting Chromedriver\n\033[0m')
    if 'mac' or 'linux' in get_os():
        system(f"unzip -q -o {CHROMEDRIVER_ZIP_PATH} -d {dirname(drivers_dir())}/binaries/")
        print(f'\033[94m Chromedriver extracted to {dirname(drivers_dir())}\n\033[0m')
    else:
        zf = zipfile.ZipFile(CHROMEDRIVER_ZIP_PATH)
        zf.extractall(dirname(CHROMEDRIVER_ZIP_PATH))
    remove(CHROMEDRIVER_ZIP_PATH)

def run():
    download_chromium()
    download_chromedriver()
    unzip_chromedriver()
    unzip_chromium()

if __name__ == '__main__':
    run()



