from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

valid_name = "Zygfryd"
valid_lastname = "Kowalski"
valid_gender = "male"
valid_country_code = "+355"
invalid_phone_number = "123123123"
valid_email = "ofertydlams@gmail.com"
valid_password = "Babajaga321"
valid_country = "Albania"

invalid_phone_number = "abcd"


class WizzairRegistration(unittest.TestCase):
    def setUp(self):
        """ Preconditions """
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://wizzair.com/pl-pl#/")

    def tearDown(self):
        """ Cleanup after the test """
        self.driver.quit()

    def testInvalidTelephone(self):
        driver = self.driver
        # Setting: unconditional (maximum) waiting time for items
        driver.implicitly_wait(60)
        # 1. Click Log In
        zaloguj_btn = driver.find_element_by_css_selector('button[data-test="navigation-menu-signin"]')
        # Click on the item
        zaloguj_btn.click()
        # 2. Click on Registration
        driver.find_element_by_xpath('//button[@data-test="registration"]').click()
        # 3. Enter your first name
        name_input = driver.find_element_by_name("firstName")
        name_input.send_keys(valid_name)
        # 4. Enter your last name
        lastname_input = driver.find_element_by_name("lastName")
        lastname_input.send_keys(valid_lastname)
        actions = ActionChains(driver)
        # 5. Select gender
        if valid_gender == "female":
            female = driver.find_element_by_xpath('//label[@data-test="register-genderfemale"]')
            actions.move_to_element_with_offset(female, -200, 200)
            actions.click()
            actions.perform()
        else:
            male = driver.find_element_by_xpath('//label[@data-test="register-gendermale"]')
            actions.move_to_element_with_offset(male, 200, 200)
            actions.click()
            actions.perform()
        # 6. Enter the country code
        driver.find_element_by_xpath('//div[@data-test="booking-register-country-code"]').click()
        cc_input = driver.find_element_by_name('phone-number-country-code')
        cc_input.send_keys(valid_country_code, Keys.RETURN)
        # 7. Enter an invalid phone number
        driver.find_element_by_name('digits-phone-number-input').send_keys(invalid_phone_number)
        # 8. Enter a valid e-mail
        driver.find_element_by_name('email').send_keys(valid_email)
        # 9. Enter the password
        driver.find_element_by_name('password').send_keys(valid_password)
        # 10. Select a nationality
        nationality_input = driver.find_element_by_name('country-select')
        nationality_input.click()
        # countries - a list of WebElements
        countries = driver.find_elements_by_xpath('//div[@class="register-form__country-container__locations"]/label')
        for label in countries:
            # Search inside the label element
            country = label.find_element_by_tag_name("strong")
            if country.get_attribute("textContent") == valid_country:
                # Scroll to the country of your choice
                country.location_once_scrolled_into_view
                # Click on it
                country.click()
                # Look no more
                break
        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located(
            (By.XPATH, ("//div[@id='regmodal-scroll-hook-4']//div[@class='input-error']"))))

        error_messages = driver.find_elements_by_xpath('//span[@class="input-error__message"]/span')
        # Empty list for visible errors
        visible_error_messages = []
        # Check which errors are visible
        for error in error_messages:
            # Check if the error is visible
            if error.is_displayed():
                # If yes, add it to the list of visible bugs
                visible_error_messages.append(error)
        # Check if there is only one error
        print(len(visible_error_messages))
        for v in visible_error_messages:
            print(v.text)
        assert len(visible_error_messages) == 1
        # Check the content of this error
        self.assertEqual(visible_error_messages[0].text, "Wpisz właściwy numer telefonu")

if __name__ == "__main__":
    unittest.main(verbosity=2)
