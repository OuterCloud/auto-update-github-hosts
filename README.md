# AutoUpdateGithubHosts

## 简介

Auto update local GitHub hosts

自动更新本地 GitHub hosts 配置

- 本脚本原理来自 https://github.com/Licoy/fetch-github-hosts
- 依赖于服务接口 https://hosts.gitcdn.top/hosts.txt

## 环境

Python: 3.8.9

## 使用方法

```code=shell
sudo chmod 777 /etc/hosts
python3 update_github_hosts.py
```
