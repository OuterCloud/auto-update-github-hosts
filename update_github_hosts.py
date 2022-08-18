import os
import requests
import re
import logging
from os.path import abspath, dirname


class GitHubHostsUpdater:
    def __init__(self, hosts_file_path, log_dir_path):
        """
        Init method
        :param hosts_file_path: path of the hosts file
        :param log_dir_path: path of the directory of the log file
        """
        self.hosts_file_path = hosts_file_path
        self.log_dir_path = log_dir_path
        self.logger = None
        self.init_logger()

    def init_logger(self) -> None:
        """
        Init the log module
        :return: None
        """
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

    def run_cmd(self, command: str) -> None:
        """
        Execute the command in terminal
        :param command: command string
        :return: None
        """
        with os.popen(command) as a:
            self.logger.info(a.read())

    def flush_dns_cache(self) -> None:
        """
        Flush the local cache of dns
        :return: None
        """
        self.run_cmd("killall -HUP mDNSResponder")
        self.run_cmd("killall mDNSResponderHelper")
        self.run_cmd("dscacheutil -flushcache")

    def sync_github_hosts_to_remote(self) -> None:
        """
        Sync the local hosts content of GitHub to remote
        :return: None
        """
        r = requests.get("https://hosts.gitcdn.top/hosts.txt")
        self.update_github_hosts(r.text)

    def clear_github_hosts(self) -> None:
        """
        Clear the local hosts content of GitHub
        :return:
        """
        self.update_github_hosts("# fetch-github-hosts begin\n# fetch-github-hosts end")

    def update_github_hosts(self, replace_text: str) -> None:
        """
        According to the resolution: https://github.com/Licoy/fetch-github-hosts
        :return:
        """
        with open(self.hosts_file_path, "r") as rf:
            content = rf.read()
            new_content = re.sub(r"# fetch-github-hosts begin(.|\n)+# fetch-github-hosts end", replace_text, content)
            new_content = new_content.rstrip()
        if not new_content:
            self.logger.info("no new content")
            return
        if new_content == content:
            self.logger.info("no change to update")
            return
        self.logger.info(f"changes updated\noriginal:\n{content}\nnew:\n{new_content}")
        with open(self.hosts_file_path, "w") as wf:
            wf.write(new_content)
        self.flush_dns_cache()

    def show_local_hosts(self) -> None:
        """
        Show local hosts
        :return:
        """
        with open(self.hosts_file_path, "r") as rf:
            content = rf.read()
            self.logger.info(content)


if __name__ == '__main__':
    curr_dir_path = abspath(dirname(__file__))
    updater = GitHubHostsUpdater(
        hosts_file_path="/etc/hosts",
        log_dir_path=curr_dir_path)
    updater.sync_github_hosts_to_remote()
    updater.show_local_hosts()
