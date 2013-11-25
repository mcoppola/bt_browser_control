from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

browser = webdriver.Firefox()
browser.get('http://nytimes.com/')

action_chains = ActionChains(browser)
action_chains.key_down(Keys.TAB)
action_chains.key_up(Keys.TAB)
action_chains.key_down(Keys.SPACE)
action_chains.perform()
# window = browser.find_element_by_name('body')  # Find space
# window.send_keys(Keys.SPACE)