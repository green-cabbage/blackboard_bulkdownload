from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

#USER NEEDED INPUT
filenames = ["L068.csv","L080.csv", "L085.csv", "L108.csv" ] # names of files from which the code can obtain students' names

#######################################################################################################################################

#get list of names of students from csv file
# we assume the file has columns named "First Name" and "Last Name"
with open('executor_url.txt', 'r') as f:
    executor_url = f.read()
with open('session_id.txt', 'r') as f:
    session_id = f.read()
driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
driver.close() #close the dummy browser
driver.session_id = session_id
bulk_download_page = driver.current_url # assumes that the starting page is the main grading page

for filename in filenames:
    name_df = pd.read_csv(filename)
    #get list of student names of bulk download
    names = []
    for i in range (len(name_df["Last Name"])):
        names.append("'" + name_df["Last Name"][i] + ", " + name_df["First Name"][i] + "'") #ie 'Doe, John'


    # driver.get(url)
    error_names = []
    for student in names:
        try:
            checkbox = driver.find_element_by_xpath("//th[contains(text(),"+ student + ")]") #ie: "//th[contains(text(),'Doe, John')]"
            driver.execute_script("arguments[0].click();", checkbox)
        except:
            error_names.append(student)



    submit = driver.find_element_by_name("bottom_Submit")
    submit.click()
    driver.implicitly_wait(15)
    download_link = driver.find_element_by_xpath("//a[contains(text(),'Download assignments now.')]")
    download_link.click()
    print("Downloading for "+ filename)
    print("Students whose grades were not available from "+ filename+ ": ", error_names)
    driver.get(bulk_download_page)
    # driver.implicitly_wait(15)
print("Done ! Now please log out and close the browser")