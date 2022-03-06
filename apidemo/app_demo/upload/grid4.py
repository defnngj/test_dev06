from selenium import webdriver
from selenium.webdriver.common.by import By
dr = webdriver.Chrome()


# from selenium.webdriver.chromium.webdriver import ChromiumDriver
#
# dr = ChromiumDriver(browser_name='??', vendor_prefix='??')
# '''
# - browser_name - Browser name used when matching capabilities.
# - vendor_prefix - Company prefix to apply to vendor-specific WebDriver extension commands.
# '''


# from selenium.webdriver.common.by import By
# from selenium.webdriver import DesiredCapabilities
#
# dr = webdriver.Remote(command_executor='http://127.0.0.1:4444',
#                       desired_capabilities=DesiredCapabilities.CHROME.copy()
#                       )
dr.get("https://www.baidu.com")

dr.implicitly_wait(10)

dr.find_element(By.ID, "kw").send_keys("selenium grid4")
dr.find_element(By.ID, "su").click()

print("-->", dr.timeouts)
print("==>", dr.log)

dr.pin_script(script="??")
dr.unpin(script_key="??")
dr.get_pinned_scripts()

dr.quit()
