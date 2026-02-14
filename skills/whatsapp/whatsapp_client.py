import time
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from .driver import WhatsAppDriver


class WhatsAppClient:
    def __init__(self):
        self.driver = None
        self.wait = None

    def send_message(self, phone_number, message):
        """
        Sends a message to a specific phone number via WhatsApp Web.
        Returns dict with success status.
        """
        try:
            print(f"\n{'='*60}")
            print(f"Sending WhatsApp message to {phone_number}")
            print(f"Message: {message}")
            print(f"{'='*60}\n")

            # Get driver
            self.driver = WhatsAppDriver.get_driver()
            self.wait = WebDriverWait(self.driver, 30)

            # Open WhatsApp Web if not already open
            if "web.whatsapp.com" not in self.driver.current_url:
                print("Opening WhatsApp Web...")
                self.driver.get("https://web.whatsapp.com")
                print("Scan QR if not logged in...")
                time.sleep(5)

            # Wait for WhatsApp main UI
            try:
                self.wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//div[@contenteditable="true"]')
                    )
                )
                print("WhatsApp loaded!")
            except TimeoutException:
                return {
                    "success": False,
                    "error": "WhatsApp Web did not load."
                }

            # Open chat via direct URL
            encoded_message = urllib.parse.quote(message)
            chat_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}"
            self.driver.get(chat_url)

            time.sleep(5)

            # Find message box
            try:
                message_box = self.wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//div[@contenteditable="true"][@role="textbox"]')
                    )
                )
            except TimeoutException:
                return {
                    "success": False,
                    "error": "Message input box not found."
                }

            # Clear and type message
            message_box.clear()
            time.sleep(0.5)
            message_box.send_keys(message)
            time.sleep(1)

            # Send message
            try:
                send_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//span[@data-icon="send"]')
                    )
                )
                send_button.click()
            except:
                message_box.send_keys(Keys.ENTER)

            time.sleep(2)

            return {
                "success": True,
                "message": f"Message sent to {phone_number}"
            }

        except Exception as e:
            print(f"Critical error: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def close(self):
        """Close the WhatsApp client"""
        if self.driver:
            try:
                self.driver.quit()
                print("Driver closed successfully.")
            except Exception as e:
                print(f"Error closing driver: {e}")
