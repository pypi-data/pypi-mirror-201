import requests
import re
import random

class Proxy:
    def __init__(self, headers=None, cookies={}, proxy_mode="random"):
        
        assert proxy_mode in ["random", "order", "score"], f"Invalid proxy_mode: {proxy_mode}, must be 'random', 'order', or 'score'."
        
        self.headers = headers if headers else {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",        
        }
        self.cookies = cookies
        self.proxy_ips = self.get_proxy_ips()
        self.proxy_mode = proxy_mode
        
        if proxy_mode == "score":
            self.proxy_scores = {proxy_ip: 10 for proxy_ip in self.proxy_ips}
        self.success = {proxy_ip: 0 for proxy_ip in self.proxy_ips}
        self.failure = {proxy_ip: 0 for proxy_ip in self.proxy_ips}

    def get_proxy_ips(self):
        """從sslproxies.org網站取得代理IP列表"""
        response = requests.get("https://www.sslproxies.org/")
        assert response.status_code == 200, "Fails to get proxy IPs."
        proxy_ips = re.findall('\d+\.\d+\.\d+\.\d+:\d+', response.text)  #「\d+」代表數字一個位數以上
        return proxy_ips
    
    def request(self, 
                url, 
                method='GET', 
                data={},
                max_retries_per_proxy=3, 
                max_proxies_to_try=3,
                ignore_failure=True,
                use_local=False,
    ):
        """使用代理IP發送請求"""

        for proxy_ip in self.get_proxies(max_proxies_to_try):
            print(f"Trying proxy: {proxy_ip}")
            for i in range(max_retries_per_proxy):
                print(f"Retry {i+1}...", end="\r")
                try:
                    response = requests.request(
                        method=method, 
                        url=url, 
                        data=data,
                        headers=self.headers, 
                        cookies=self.cookies, 
                        proxies={'https': proxy_ip, 'http': proxy_ip}
                    )
                    response.raise_for_status()
                    self._record_success(proxy_ip)
                    return response
                except Exception as e:
                    self._record_failure(proxy_ip)
        
        if not ignore_failure:
            raise Exception("All proxies failed.")
        
        if use_local:
            print("All proxies failed, using local IP.")
            return requests.request(
                method=method, 
                url=url, 
                data=data,
                headers=self.headers, 
                cookies=self.cookies, 
            )
    
    def get_proxies(self, n=1):
        """取得要嘗試的代理IP
        Args:
            n (int): 要嘗試的代理IP數量
        Returns:
            proxies (list): 要嘗試的代理IP列表
        """
        n = min(n, len(self.proxy_ips))
        
        if self.proxy_mode == "random":
            proxies =  random.sample(self.proxy_ips, n)
        if self.proxy_mode == "order":
            proxies = self.proxy_ips[:n]
            self.proxy_ips = self.proxy_ips[n:] + self.proxy_ips[:n]
        if self.proxy_mode == "score":
            proxies = sorted(self.proxy_ips, key=lambda x: self.proxy_scores[x], reverse=True)[:n]
                
        return proxies
    
    def _record_success(self, proxy_ip):
        """記錄成功的代理IP"""
        self.success[proxy_ip] += 1
        if self.proxy_mode == "score":
            self.proxy_scores[proxy_ip] += 1
        
    def _record_failure(self, proxy_ip):
        """記錄失敗的代理IP"""
        self.failure[proxy_ip] += 1
        if self.proxy_mode == "score":
            self.proxy_scores[proxy_ip] -= 3
            
    def get_record(self):
        """取得代理IP的成功與失敗次數
        合併到一個dict
        """
        return {proxy_ip: {"success": self.success[proxy_ip], "failure": self.failure[proxy_ip]} for proxy_ip in self.proxy_ips}