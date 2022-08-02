import os
import requests
import re
import logging
import difflib


class GithubHostsUpdater:
    def __init__(self, hosts_file_path, log_dir_path):
        self.hosts_file_path = hosts_file_path
        self.log_dir_path = log_dir_path
        self.logger = None
        self.init_logger()

    def init_logger(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        file_handler = logging.FileHandler(f'{self.log_dir_path}/update_github_hosts.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        self.logger = logger

    def run_cmd(self, command: str):
        with os.popen(command) as a:
            self.logger.info(a.read())

    def flush_dns_cache(self):
        self.run_cmd("killall -HUP mDNSResponder")
        self.run_cmd("killall mDNSResponderHelper")
        self.run_cmd("dscacheutil -flushcache")

    def update_github_hosts(self):
        """
        According to the resolution: https://github.com/Licoy/fetch-github-hosts
        :return:
        """
        # get the hosts content from remote
        r = requests.get("https://hosts.gitcdn.top/hosts.txt")
        # get the content from local hosts file
        with open(self.hosts_file_path, "r") as rf:
            content = rf.read()
            new_content = re.sub(r"# fetch-github-hosts begin(.|\n)+# fetch-github-hosts end", r.text, content)
            new_content = new_content.rstrip()
        if not new_content:
            self.logger.info("no new content")
            return
        if new_content == content:
            self.logger.info("no change to update")
            return
        # show the difference between old hosts and new hosts
        for line in difflib.unified_diff(content, new_content, fromfile='old_hosts', tofile='new_hosts', lineterm=''):
            self.logger.info(line)
        self.logger.info(f"changes updated\noriginal:\n{content}\nnew:\n{new_content}")
        # update the content of local hosts file
        with open(self.hosts_file_path, "w") as wf:
            wf.write(new_content)
        # flush the dns local cache
        self.flush_dns_cache()


if __name__ == '__main__':
    '''
        You need to modify the log_dir_path to your own custom path
    '''
    updater = GithubHostsUpdater(
        hosts_file_path="/etc/hosts",
        log_dir_path="/Users/tianyou.lan/Desktop")
    updater.update_github_hosts()
