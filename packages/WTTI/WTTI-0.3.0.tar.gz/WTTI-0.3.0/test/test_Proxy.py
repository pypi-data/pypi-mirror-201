#%%
from wtti import Proxy
import pytest
from unittest import mock
from requests.exceptions import HTTPError

#%%
# 測試代理IP是否可以正常取得
def test_get_proxy_ips():
    proxy = Proxy()
    assert len(proxy.get_proxy_ips()) > 0

# 測試代理IP是否可以正常發送請求
def test_request():
    proxy = Proxy()
    response = proxy.request("https://www.example.com")
    assert response.status_code == 200