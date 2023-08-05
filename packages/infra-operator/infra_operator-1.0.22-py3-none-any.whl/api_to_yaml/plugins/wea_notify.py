#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import datetime
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from urllib import parse


def make_request(url):
    try:
        with urlopen(url, timeout=10) as response:
            print(response.status)
            return response.read(), response
    except HTTPError as error:
        print(error.status, error.reason)
    except URLError as error:
        print(error.reason)
    except TimeoutError:
        print("Request timed out")


def wea_notify(service_name, group_id, account_name, cluster_name):
    print(f"calling wea_notify({service_name}, {group_id})")
    prAuthor = os.getenv('AUTHOR_NAME')
    logURL = os.getenv('LOG_URL')
    baseLink = os.getenv('BASE_LINK')
    tz = datetime.timezone.utc
    startTime = datetime.datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S %z UTC')
    msg = f"""**[🟢  ECS Releasing Notification]**

**Account:** {account_name}

**Cluster:** {cluster_name}

**Service:** {service_name}

**ReleaseBy:** {prAuthor}

**Commit:** {baseLink}

**Log:** {logURL}

**ReleaseAt:** {startTime}
"""
    url = f"https://devops-api-prod.toolsfdg.net/weateams/devops-infra-bot/{group_id}/notify?msgType=markdown&msg={parse.quote_plus(msg)}"
    if os.environ.get("DEBUG"):
        print(f"url is {url}")
    make_request(url)


def release_notify_wea(service_name, config, account_name, cluster_name):
    tmp = ''
    wea_dict = config.get('wea_notifier', {})
    for reg in wea_dict.keys():
        if len(reg) > len(tmp) and re.match(reg, service_name):
            tmp = reg
    if os.environ.get("DEBUG"):
        print(f"regex: {tmp}")
    if tmp:
        wea_notify(service_name, wea_dict.get(
            f"{tmp}"), account_name, cluster_name)
