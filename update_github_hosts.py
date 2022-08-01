import requests
import re
import logging
import difflib
from pprint import pprint

desktop_path = "/Users/tianyou.lan/Desktop"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler(f'{desktop_path}/update_github_hosts.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
host_file = "/etc/hosts"


def update_github_hosts():
    """
    According to the resolution: https://github.com/Licoy/fetch-github-hosts
    :return:
    """
    r = requests.get("https://hosts.gitcdn.top/hosts.txt")
    with open(host_file, "r") as rf:
        content = rf.read()
        new_content = re.sub(r"# fetch-github-hosts begin(.|\n)+# fetch-github-hosts end", r.text, content)
    if not new_content:
        return
    new_content = new_content.rstrip()
    if new_content == content:
        logger.info("no change to update")
        return
    d = difflib.Differ()
    diff = d.compare(content, new_content)
    pprint(list(diff))
    logger.info(f"changes updated\noriginal:\n{content}\nnew:\n{new_content}")
    with open(host_file, "w") as wf:
        wf.write(new_content)
    with open(host_file, "r") as rnf:
        logger.info(rnf.read())


if __name__ == '__main__':
    update_github_hosts()
