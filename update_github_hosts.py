import requests
import re
import logging
import difflib
from pprint import pprint

desktop_path = "/Users/tianyou.lan/Desktop"
logging.basicConfig(
    filename=f'{desktop_path}/update_github_hosts.log',
    format='%(asctime)s %(message)s',
    level=logging.DEBUG)
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
        logging.info("no change to update")
        return
    d = difflib.Differ()
    diff = d.compare(content, new_content)
    pprint(list(diff))
    logging.info("changes updated")
    with open(host_file, "w") as wf:
        wf.write(new_content.strip("/n"))
    with open(host_file, "r") as rnf:
        logging.info(rnf.read())


if __name__ == '__main__':
    update_github_hosts()
