
import requests
from loguru import logger
from typing import Any


class BaseCracker:
    
    # 破解器
    cracker_name = "base"
    
    # 破解版本
    cracker_version = "universal"
    
    # 必须参数列表
    must_check_params = []
    
    # 可选参数
    option_params = {}
    
    def __init__(
        self,    
        user_token: str = None,
        developer_id: str = "",   
        user_agent: str = "",
        proxy: str = None, 
        timeout: int = 30,
        debug: bool = False,
        check_useful: bool = False,
        max_retry_times: int = 3,
        internal_proxy=False,
        **kwargs
    ) -> None:
        """
        :param user_token: nocaptcha.io 用户 token
        :param developer_id: nocaptcha.io 用户上级代理 token
        :param user_agent: 请求流程使用 ua
        :param proxy: 请求流程代理, 不传默认使用系统代理, 某些强制要求代理一致或者特定区域的站点请传代理, 支持协议 http/https/socks5, 代理格式: {protocol}://{ip}:{port}（如有账号验证：{protocol}://{user}:{password}@{ip}:{port}）
        :param timeout: 破解接口超时时间(秒)
        :param debug: 是否开启 debug 模式
        :param check_useful: 检查破解是否成功
        :param max_retry_times: 最大重试次数
        :param internal_proxy: 是否使用国内代理
        """
        self.user_token = user_token
        if not self.user_token:
            raise Exception("缺少用户凭证")
        self.developer_id = developer_id
        self.user_agent = user_agent
        self.proxy = proxy
        self.timeout = timeout
        self.debug = debug
        self.check_useful = check_useful
        self.retry_times = 0
        self.max_retry_times = max_retry_times

        self.wanda_args = {
            "internal_proxy": internal_proxy
        }
        for k in self.must_check_params:
            v = kwargs.get(k)
            setattr(self, k, v)
            self.wanda_args.update({ k: v })
        for k, v in self.option_params.items():
            _v = kwargs.get(k, v)
            if not hasattr(self, k) or getattr(self, k) is None:
                setattr(self, k, _v)
            self.wanda_args.update({ k: _v })

        if not all(getattr(self, k) for k in self.must_check_params):
           raise AttributeError("缺少参数, 请检查")

    def response(self, result: Any):
        return result
        
    def check(self, ret):
        return True
    
    def crack(self):
        headers = {
            "User-Token": self.user_token
        }
        if self.developer_id:
            headers["Developer-Id"] = self.developer_id
        resp = requests.post(f"http://api.nocaptcha.io/api/wanda/{self.cracker_name}/{self.cracker_version}", headers=headers, json={
            **self.wanda_args,
            "user_agent": self.user_agent,
            "proxy": self.proxy
        }, timeout=self.timeout).json()
        if self.debug:
            logger.info(resp)
        wanda_ret = resp.get("data")
        if not wanda_ret:
            if self.debug:
                logger.error(resp.get("msg"))
            return
        ret = self.response(wanda_ret)
        if self.check_useful:
            if self.check(wanda_ret):
                if self.debug:
                    logger.success("crack success")
            else:
                self.retry_times += 1
                if self.retry_times < self.max_retry_times:
                    return self.crack()
                else:
                    logger.error("crack fail")
        return ret
