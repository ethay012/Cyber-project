from selenium import webdriver
import time

def install_firefox_proxy(PROXY_HOST,PROXY_PORT):
    fp = webdriver.FirefoxProfile()
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.socks", PROXY_HOST)
    fp.set_preference("network.proxy.socks_port", int(PROXY_PORT))
    fp.set_preference("network.proxy.socks_remote_dns", True)
    fp.update_preferences()
    return webdriver.Firefox(firefox_profile=fp)


driver = install_firefox_proxy("127.0.0.1", 3200)
driver.get('about:config')


