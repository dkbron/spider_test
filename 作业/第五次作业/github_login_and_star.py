from selenium import webdriver

driver = webdriver.Chrome()

# 等待
driver.implicitly_wait(10)

url = 'https://github.com'

driver.get(url)

sign_in = driver.find_element_by_xpath('/html/body/div[1]/header/div/div[2]/div[2]/a[1]')

sign_in.click()

inputUserName = driver.find_element_by_xpath('//*[@id="login_field"]')
inputUserName.send_keys('账号')
inputPassword = driver.find_element_by_xpath('//*[@id="password"]')
inputPassword.send_keys('密码')

driver.find_element_by_xpath('//*[@id="login"]/form/div[3]/input[7]').click()
driver.get('https://github.com/scrapyhub/JSpider')
driver.find_element_by_xpath('//*[@id="js-repo-pjax-container"]/div[1]/div/ul/li[3]/div/form[2]/button').click()