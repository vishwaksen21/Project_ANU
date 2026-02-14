from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os

class WhatsAppDriver:
    _instance = None
    _driver = None

    @classmethod
    def get_driver(cls):
        # Check if existing driver is valid
        if cls._driver is not None:
            try:
                # This will raise an exception if the window is closed/crashed
                _ = cls._driver.current_url
            except Exception:
                print("Driver found but unresponsive. cleanup...")
                try:
                    cls._driver.quit()
                except Exception:
                    pass
                cls._driver = None
                
        if cls._driver is None:
            cls._driver = cls._init_driver()
        return cls._driver

    @staticmethod
    def _init_driver():
        print("Initializing Chrome Driver...")
        try:
            # Use Chrome with webdriver_manager for automatic driver management
            chrome_options = Options()
            # chrome_options.add_argument('--headless')  # Uncomment for headless mode
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Set user data dir to persist WhatsApp Web session
            user_data_dir = os.path.expanduser("~/.whatsapp_chrome_profile")
            chrome_options.add_argument(f'user-data-dir={user_data_dir}')
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.maximize_window()
            
            print("✅ Chrome Driver initialized successfully!")
            return driver
        except Exception as e:
            print(f"❌ Failed to initialize Chrome: {e}")
            print("Tip: Make sure Chrome browser is installed on your system.")
            raise e
