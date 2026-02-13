from core.skill import Skill
import json
import os
from skills.whatsapp.whatsapp_client import WhatsAppClient

class WhatsappSkill(Skill):
    """
    Skill for sending WhatsApp messages using Selenium and a local contact list.
    """
    
    def __init__(self):
        self.contacts = self._load_contacts()
        self.client = None # Lazy load the client

    @property
    def name(self):
        return "whatsapp_skill"
        
    def _load_contacts(self):
        contacts_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "contacts.json")
        try:
            with open(contacts_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading contacts: {e}")
            return {}

    def _get_client(self):
        if not self.client:
            self.client = WhatsAppClient()
        return self.client

    def get_tools(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "send_whatsapp_message",
                    "description": "Send a WhatsApp message to a specific person by name.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The name of the contact (e.g., 'Dad', 'Mom', 'Ananya')."
                            },
                            "message": {
                                "type": "string",
                                "description": "The message to send."
                            }
                        },
                        "required": ["name", "message"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "add_whatsapp_contact",
                    "description": "Add a new contact to WhatsApp contacts list.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The name of the contact."
                            },
                            "phone_number": {
                                "type": "string",
                                "description": "Phone number with country code (e.g., +91 for India, +1 for USA)."
                            }
                        },
                        "required": ["name", "phone_number"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "list_whatsapp_contacts",
                    "description": "List all WhatsApp contacts saved in the system.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "import_device_contacts",
                    "description": "Import all contacts from the device's Contacts app into WhatsApp contacts.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            }
        ]

    def get_functions(self):
        return {
            "send_whatsapp_message": self.send_whatsapp_message,
            "add_whatsapp_contact": self.add_whatsapp_contact,
            "list_whatsapp_contacts": self.list_whatsapp_contacts,
            "import_device_contacts": self.import_device_contacts
        }

    def add_whatsapp_contact(self, name, phone_number):
        """Add a new contact to the contacts list."""
        try:
            clean_name = name.lower().strip()
            
            # Clean phone number (remove spaces, dashes)
            clean_phone = phone_number.strip().replace(" ", "").replace("-", "")
            
            # Ensure it starts with +
            if not clean_phone.startswith("+"):
                # Assume India (+91) if no country code
                clean_phone = "+91" + clean_phone
            
            # Update contacts
            self.contacts[clean_name] = clean_phone
            
            # Save to file
            contacts_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "contacts.json")
            with open(contacts_path, 'w') as f:
                json.dump(self.contacts, f, indent=2)
            
            return f"✓ Contact '{name}' added with number {clean_phone}"
        except Exception as e:
            return f"Error adding contact: {e}"
    
    def list_whatsapp_contacts(self):
        """List all saved contacts."""
        if not self.contacts:
            return "No contacts saved yet. You can add contacts by saying 'Add Ananya's WhatsApp contact with number +91XXXXXXXXXX'"
        
        contact_list = "\n".join([f"• {name.title()}: {phone}" for name, phone in self.contacts.items()])
        return f"Your WhatsApp contacts:\n{contact_list}"
    
    def import_device_contacts(self):
        """Import all contacts from macOS Contacts app."""
        try:
            import subprocess
            
            # AppleScript to get all contacts with phone numbers
            applescript = '''
            tell application "Contacts"
                set contactList to {}
                repeat with aPerson in people
                    set personName to name of aPerson
                    repeat with aPhone in phones of aPerson
                        set phoneValue to value of aPhone
                        set end of contactList to personName & "|" & phoneValue
                    end repeat
                end repeat
                return contactList
            end tell
            '''
            
            # Execute AppleScript
            result = subprocess.run(
                ['osascript', '-e', applescript],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return f"❌ Could not access Contacts app. Error: {result.stderr}"
            
            # Parse results
            contact_data = result.stdout.strip()
            if not contact_data:
                return "No contacts found in your Contacts app."
            
            # Split by comma (AppleScript list format)
            contacts_raw = contact_data.split(", ")
            
            imported_count = 0
            skipped_count = 0
            
            for contact_entry in contacts_raw:
                try:
                    # Split name and phone
                    if "|" not in contact_entry:
                        continue
                    
                    name, phone = contact_entry.split("|", 1)
                    name = name.strip()
                    phone = phone.strip()
                    
                    # Clean phone number (remove spaces, dashes, parentheses)
                    clean_phone = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                    
                    # Skip if phone doesn't look valid
                    if len(clean_phone) < 10:
                        skipped_count += 1
                        continue
                    
                    # Ensure it starts with +
                    if not clean_phone.startswith("+"):
                        # Assume India (+91) if no country code and 10 digits
                        if len(clean_phone) == 10:
                            clean_phone = "+91" + clean_phone
                        else:
                            # Skip invalid numbers
                            skipped_count += 1
                            continue
                    
                    # Add to contacts
                    clean_name = name.lower().strip()
                    self.contacts[clean_name] = clean_phone
                    imported_count += 1
                    
                except Exception as e:
                    skipped_count += 1
                    continue
            
            # Save to file
            contacts_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "contacts.json")
            with open(contacts_path, 'w') as f:
                json.dump(self.contacts, f, indent=2)
            
            return f"✅ Successfully imported {imported_count} contacts from your device! {skipped_count} contacts were skipped (invalid numbers). You now have {len(self.contacts)} total contacts."
            
        except subprocess.TimeoutExpired:
            return "❌ Timeout while accessing Contacts app. Please try again."
        except Exception as e:
            return f"❌ Error importing contacts: {str(e)}"

    def send_whatsapp_message(self, name, message):
        """
        Sends a WhatsApp message to a contact by name.
        """
        # 1. Normalize name
        clean_name = name.lower().strip()
        
        # 2. Lookup Number
        phone_number = self.contacts.get(clean_name)
        
        if not phone_number:
            # Provide helpful error with suggestion
            available = ", ".join(list(self.contacts.keys())[:5])
            if available:
                return f"❌ I don't have '{name}' in your WhatsApp contacts. Available contacts: {available}. Would you like to add '{name}' first?"
            else:
                return f"❌ I don't have any WhatsApp contacts saved yet. Would you like to add '{name}'? Just tell me their phone number!"
            
        # 3. Send Message via Client
        try:
            client = self._get_client()
            result = client.send_message(phone_number, message)
            return f"✓ Message sent to {name.title()}: '{message}'"
        except Exception as e:
            return f"❌ Error sending message to {name}: {str(e)}"
