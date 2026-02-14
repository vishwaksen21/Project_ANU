import time
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from .driver import WhatsAppDriver

class WhatsAppClient:
    def __init__(self):
        self.driver = None
        self.wait = None

    def send_message(self, phone_number, message):
        """
        Sends a message to a specific phone number via WhatsApp Web.
        Returns True if successful, False otherwise.
        """
        try:
            print(f"\n{'='*60}")
            print(f"📱 Sending WhatsApp message to {phone_number}")
            print(f"💬 Message: {message}")
            print(f"{'='*60}\n")
            
            # Get driver
            self.driver = WhatsAppDriver.get_driver()
            self.wait = WebDriverWait(self.driver, 30)
            
            # Step 1: Navigate to WhatsApp Web
            if "web.whatsapp.com" not in self.driver.current_url:
                print("🌐 Opening WhatsApp Web...")
                self.driver.get("https://web.whatsapp.com")
                print("⏳ Please scan QR code if not logged in...")
                time.sleep(3)
            
            # Step 2: Wait for WhatsApp to load (check for search box or side panel)
            print("⏳ Waiting for WhatsApp to load...")
            try:
                # Wait for the main interface to load - search box or chat list
                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]'))
                )
                print("✅ WhatsApp Web loaded!")
            except TimeoutException:
                return {"success": False, "error": "WhatsApp Web did not load. Please check if you're logged in."}
            
            # Step 3: Use direct URL to open chat
            print(f"🔗 Opening chat with {phone_number}...")
            encoded_message = urllib.parse.quote(message)
            chat_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}"
            self.driver.get(chat_url)
            
            # Step 4: Wait for chat to load and find the message input box
            print("⏳ Waiting for chat interface...")
            time.sleep(3)  # Give it time to load
            
            # Look for the message input box
            try:
                # Try multiple selectors for the message box
                message_box = None
                selectors = [
                    '//div[@contenteditable="true"][@data-tab="10"]',  # Primary
                    '//div[@contenteditable="true"][@role="textbox"]',  # Alternative
                    '//div[@contenteditable="true" and @title="Type a message"]',  # Title-based
                    '//div[contains(@class, "copyable-text")]//div[@contenteditable="true"]',  # Class-based
                ]
                
                for selector in selectors:
                    try:
                        message_box = self.wait.until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                        print(f"✅ Found message box using selector: {selector[:50]}...")
                        break
                    except:
                        continue
                
                if not message_box:
                    return {"success": False, "error": "Could not find message input box. Contact may not exist on WhatsApp."}
                
                # Step 5: Clear any existing text and type the message
                print("⌨️  Typing message...")
                message_box.clear()
                time.sleep(0.5)
                
                # Type message character by character for reliability
                for char in message:
                    message_box.send_keys(char)
                    time.sleep(0.02)  # Small delay for natural typing
                
                print("✅ Message typed!")
                time.sleep(1)
                
                # Step 6: Send the message
                print("📤 Sending message...")
                
                # Try multiple methods to send
                sent = False
                
                # Method 1: Click send button
                try:
                    send_button_selectors = [
                        '//span[@data-icon="send"]',
                        '//button[@aria-label="Send"]',
                        '//span[@data-testid="send"]',
                    ]
                    
                    for selector in send_button_selectors:
                        try:
                            send_btn = self.wait.until(
                                EC.element_to_be_clickable((By.XPATH, selector))
                            )
                            send_btn.click()
                            sent = True
                            print("✅ Message sent via button click!")
                            break
                        except:
                            continue
                except Exception as e:
                    print(f"⚠️  Button click failed: {e}")
                
                # Method 2: Press Enter key
                if not sent:
                    try:
                        message_box.send_keys(Keys.ENTER)
                        sent = True
                        print("✅ Message sent via Enter key!")
                    except Exception as e:
                        print(f"❌ Enter key failed: {e}")
                
                if not sent:
                    return {"success": False, "error": "Could not send message. Send button not found."}
                
                # Step 7: Verify message was sent
                time.sleep(2)
                print("✅ Message sent successfully!")
                
                return {
                    "success": True, 
                    "message": f"Message sent to {phone_number}",
                    "phone": phone_number,
                    "text": message
                }
                
            except TimeoutException:
                return {
                    "success": False, 
                    "error": f"Timeout waiting for chat. Number {phone_number} may not be on WhatsApp."
                }
            except Exception as e:
                return {"success": False, "error": f"Error in chat: {str(e)}"}
        
        except Exception as e:
            print(f"❌ Critical error in send_message: {e}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": f"Critical error: {str(e)}"}

    def close(self):
        """Close the WhatsApp client"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
