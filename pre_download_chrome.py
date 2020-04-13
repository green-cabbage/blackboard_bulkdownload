from selenium import webdriver


driver = webdriver.Chrome()
executor_url = driver.command_executor._url
session_id = driver.session_id
with open('executor_url.txt', 'w') as f:
    f.write(executor_url)
with open('session_id.txt', 'w') as f:
    f.write(session_id)