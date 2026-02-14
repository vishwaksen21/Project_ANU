from core.skill import Skill
import json
import os
import subprocess
from skills.whatsapp.whatsapp_client import WhatsAppClient


class WhatsappSkill(Skill):
    """
    Skill for sending WhatsApp messages using Selenium and a local contact list.
    """

    def __init__(self):
        self.contacts_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "contacts.json"
        )
        self.contacts = self._load_contacts()
        self.client = None  # Lazy load

    @property
    def name(self):
        return "whatsapp_skill"

    def get_tools(self):
        """Return tool schemas for WhatsApp operations"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "send_whatsapp_message",
                    "description": "Send a WhatsApp message to a contact by name",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Contact name (from saved contacts)"
                            },
                            "message": {
                                "type": "string",
                                "description": "Message to send"
                            }
                        },
                        "required": ["name", "message"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "add_whatsapp_contact",
                    "description": "Add a new WhatsApp contact",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Contact name"
                            },
                            "phone_number": {
                                "type": "string",
                                "description": "Phone number with country code"
                            }
                        },
                        "required": ["name", "phone_number"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_whatsapp_contacts",
                    "description": "List all saved WhatsApp contacts",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "import_device_contacts",
                    "description": "Import contacts from macOS Contacts app",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
        ]

    def get_functions(self):
        """Return mapping of function names to actual methods"""
        return {
            "send_whatsapp_message": self.send_whatsapp_message,
            "add_whatsapp_contact": self.add_whatsapp_contact,
            "list_whatsapp_contacts": self.list_whatsapp_contacts,
            "import_device_contacts": self.import_device_contacts
        }

    def _load_contacts(self):
        try:
            if not os.path.exists(self.contacts_path):
                return {}

            with open(self.contacts_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading contacts: {e}")
            return {}

    def _save_contacts(self):
        try:
            with open(self.contacts_path, "w") as f:
                json.dump(self.contacts, f, indent=2)
        except Exception as e:
            print(f"Error saving contacts: {e}")

    def _get_client(self):
        if not self.client:
            self.client = WhatsAppClient()
        return self.client

    # ---------------- CONTACT MANAGEMENT ---------------- #

    def add_whatsapp_contact(self, name, phone_number):
        try:
            clean_name = name.lower().strip()
            clean_phone = phone_number.strip().replace(" ", "").replace("-", "")

            if not clean_phone.startswith("+"):
                clean_phone = "+91" + clean_phone  # Default India

            self.contacts[clean_name] = clean_phone
            self._save_contacts()

            return f"✓ Contact '{name.title()}' added with number {clean_phone}"

        except Exception as e:
            return f"Error adding contact: {e}"

    def list_whatsapp_contacts(self):
        if not self.contacts:
            return "No contacts saved yet."

        contact_list = "\n".join(
            [f"• {name.title()}: {phone}" for name, phone in self.contacts.items()]
        )

        return f"Your WhatsApp contacts:\n{contact_list}"

    # ---------------- IMPORT FROM MAC ---------------- #

    def import_device_contacts(self):
        try:
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

            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                return f"❌ Could not access Contacts app: {result.stderr}"

            contact_data = result.stdout.strip()
            if not contact_data:
                return "No contacts found."

            contacts_raw = contact_data.split(", ")

            imported_count = 0
            skipped_count = 0

            for entry in contacts_raw:
                if "|" not in entry:
                    continue

                name, phone = entry.split("|", 1)
                name = name.strip()
                phone = phone.strip()

                clean_phone = (
                    phone.replace(" ", "")
                    .replace("-", "")
                    .replace("(", "")
                    .replace(")", "")
                )

                if len(clean_phone) < 10:
                    skipped_count += 1
                    continue

                if not clean_phone.startswith("+"):
                    if len(clean_phone) == 10:
                        clean_phone = "+91" + clean_phone
                    else:
                        skipped_count += 1
                        continue

                self.contacts[name.lower()] = clean_phone
                imported_count += 1

            self._save_contacts()

            return (
                f"✅ Imported {imported_count} contacts. "
                f"{skipped_count} skipped. "
                f"Total contacts: {len(self.contacts)}"
            )

        except subprocess.TimeoutExpired:
            return "❌ Timeout while accessing Contacts app."
        except Exception as e:
            return f"❌ Error importing contacts: {str(e)}"

    # ---------------- SEND MESSAGE ---------------- #

    def send_whatsapp_message(self, name, message):
        clean_name = name.lower().strip()
        phone_number = self.contacts.get(clean_name)

        if not phone_number:
            if self.contacts:
                suggestions = ", ".join(
                    [n.title() for n in list(self.contacts.keys())[:5]]
                )
                return (
                    f"❌ '{name}' not found.\n"
                    f"Available contacts: {suggestions}\n"
                    f"Would you like to add it?"
                )
            else:
                return (
                    "❌ No contacts saved yet.\n"
                    "Tell me the phone number to add one."
                )

        try:
            client = self._get_client()
            result = client.send_message(phone_number, message)

            if isinstance(result, dict) and not result.get("success"):
                return f"❌ Failed: {result.get('error')}"

            return f"✅ Message sent to {name.title()}"

        except Exception as e:
            return f"❌ Error sending message: {str(e)}"


def register():
    """Register the WhatsApp skill"""
    return WhatsappSkill()
