from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Step 1: Connect Python to Edge inside Docker
options = webdriver.EdgeOptions()
options.add_argument("--headless")  # Runs without opening a visible browser

driver = webdriver.Remote(
    command_executor="http://localhost:4444/wd/hub",
    options=options
)

# Step 2: Open LinkedIn Jobs Page
driver.get("https://www.linkedin.com/jobs/search/?keywords=mechanical%20design%20engineer")

# Step 3: Wait until job results load
try:
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//ul[@class='jobs-search__results-list']")))
except:
    print("❌ Error: Job listings did not load.")
    driver.quit()
    exit()

# Step 4: Find all job listings
jobs = driver.find_elements(By.XPATH, "//ul[@class='jobs-search__results-list']/li")

job_list = []

# Step 5: Extract Job Details
for job in jobs[:10]:  # Extract first 10 jobs
    try:
        title = job.find_element(By.XPATH, ".//h3").text.strip()
        company = job.find_element(By.XPATH, ".//h4").text.strip()
        location = job.find_element(By.XPATH, ".//span[contains(@class, 'job-search-card__location')]").text.strip()
        link = job.find_element(By.TAG_NAME, "a").get_attribute("href")

        job_list.append({
            "Title": title,
            "Company": company,
            "Location": location,
            "Link": link
        })

    except Exception as e:
        print("⚠️ Warning: Skipped a job due to missing fields:", e)

# Step 6: Save Data to Excel
df = pd.DataFrame(job_list)
df.to_excel("linkedin_jobs.xlsx", index=False)

print("✅ Job listings saved successfully! Check 'linkedin_jobs.xlsx'.")

# Step 7: Close the browser
driver.quit()