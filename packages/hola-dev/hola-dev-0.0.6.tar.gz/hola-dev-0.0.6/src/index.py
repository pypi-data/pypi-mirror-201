import os
import json
import requests
import platform

from yachalk import chalk
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from src.utils.util import set_secret_manager_env

COMMON_PACKAGES = {
    'Google Chrome': 'brew install --cask google-chrome',
    'Firefox': 'brew install firefox',
    'KakaoTalk': 'mas install 869223134',
    'Zoom': 'brew install --cask zoom',
    'Slack': 'brew install --cask slack',
    'Notion': 'brew install --cask notion',
    '1Password': 'brew install --cask 1password',
    'Authy': 'brew install authy',
    'Microsoft Teams': 'brew install microsoft-teams'
}

DEV_PACKAGES = {
    'VSCode': 'brew install --cask visual-studio-code',
    'PhpStorm': 'brew install phpstorm',
    'PyCharm': 'brew install pycharm',
    'Postman': 'brew install --cask postman',
    'Docker': 'brew install docker',
    'iTerm2': 'brew install --cask iterm2',
    'XCode': 'mas install 497799835',
    'Zsh': 'brew install zsh zsh-completions zsh-syntax-highlighting zsh-autosuggestions',
    'Go': 'brew install go',
    'ElasticSearch': 'brew install elasticsearch',
    'Packer': 'brew install packer',
    'Terraform': 'brew install terraform',
    'Vault': 'brew install vault'
}


def main():
    try:
        set_secret_manager_env()
        print(chalk.green.bold("env 로드 성공"))
    except:
        print(chalk.red.bold("env 로드 실패"))
        return

    if platform.system() != 'Darwin':
        print('해당 CLI는 MAC에서만 작동합니다.')
        return

    if os.system('which brew') != 0:
        os.system('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
    
    if os.system('which mas') != 0:
        os.system('brew install mas')


    action = inquirer.select(
        message="실행할 옵션을 선택해주세요.",
        choices=["MAC 기본 패키지 설치", "개발 관련 패키지 설치", "개발환경 셋팅", "로컬 서버 접근 주소 얻기", "브라우저 자동화"],
        default=None,
    ).execute()

    if action == 'MAC 기본 패키지 설치':
        install_common_packages()
    elif action == '개발 관련 패키지 설치':
        install_dev_packages()
    elif action == '개발환경 셋팅':
        set_environment()
    elif action == '로컬 서버 접근 주소 얻기':
        get_localtunnel_address()
    elif action == '브라우저 자동화':
        browser_automation()
        

def install_common_packages():
    common_packages_answer = inquirer.checkbox(
        message="개발 환경 설정이 필요한 항목을 선택해주세요.",
        choices=COMMON_PACKAGES.keys(),
        instruction='(Space 버튼으로 선택)'
    ).execute()

    for item in common_packages_answer:
        installation_command = COMMON_PACKAGES[item]
        os.system(installation_command)


def install_dev_packages():
    dev_packages_answer = inquirer.checkbox(
        message="개발 환경 설정이 필요한 항목을 선택해주세요.",
        choices=DEV_PACKAGES.keys(),
        instruction='(Space 버튼으로 선택)'
    ).execute()

    for item in dev_packages_answer:
        installation_command = COMMON_PACKAGES[item]
        os.system(installation_command)


def set_environment():
    environment_answer = inquirer.checkbox(
        message="개발 환경 설정이 필요한 항목을 선택해주세요.",
        choices=['NodeJS 버전 설정', 'Python 버전 설정', 'Java 버전 설정', 'Git 계정 설정', 'AWS Credential 설정'],
        instruction='(Space 버튼으로 선택)'
    ).execute()

    if 'NodeJS 버전 설정' in environment_answer:
        node_version = inquirer.text(message="사용하실 NodeJS 버전:", default="14").execute()
        os.system('brew install nvm')
        os.system(f"nvm install {node_version}")
        os.system(f"nvm use {node_version}")
        
    if 'Python 버전 설정' in environment_answer:
        if os.system('which pyenv') != 0:
            os.system('brew install pyenv')
        os.system('pyenv ')

    if 'Java 버전 설정' in environment_answer:
        os.system('brew install gradle')

    if 'Git 계정 설정' in environment_answer:
        os.system('brew install gh')
        os.system(f"gh auth login")

    if 'AWS Credential 설정' in environment_answer:
        os.system('brew install awscli')
        os.system(f"aws configure")


def get_localtunnel_address():
    if os.system('which lt') != 0:
        os.system('brew install localtunnel')

    port = inquirer.text(message="연결할 Local 포트:", default="8000").execute()
    domain = inquirer.text(message="사용할 커스텀 도메인:", default="codenary").execute()
    os.system(f"lt --port {port} --subdomain {domain}")


def browser_automation():
    if not os.environ.get('JSONBIN_ENDPOINT', None):
        print('.env 파일을 확인해주세요.')
        return
    
    profile_list = requests.get(
        url = os.environ.get('JSONBIN_ENDPOINT'), 
        headers = {'X-Access-Key': os.environ.get('JSONBIN_ACCESSKEY')}
    ).json()

    selected_profile = inquirer.select(
        message="프로필을 선택해주세요.",
        choices=[
            Choice(profile, name=f'{profile["username"]} ({profile["company"]})') for profile in profile_list['record']['items']
        ],
        default=None,
    ).execute()

    open_browser(selected_profile)

    
def open_browser(profile):
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_experimental_option("detach", True)
    
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get(url=os.environ.get('BROWSER_ENDPOINT'))
    driver.execute_script(f"window.localStorage.setItem('userinfo','" + json.dumps(profile)+ "');")
    driver.refresh()

if __name__ == '__main__':
    main()