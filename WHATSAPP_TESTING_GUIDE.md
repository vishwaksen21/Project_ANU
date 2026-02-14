# 📱 WhatsApp Testing Guide for ANU

## 🎯 Complete WhatsApp Setup & Testing Checklist

### ✅ Step 1: Import Your Contacts
```
"ANU, import all my contacts from my device"
```

This will:
- Access your macOS Contacts app
- Extract all contacts with phone numbers
- Format numbers with country codes (+91 for India)
- Save to `contacts.json`
- Report how many contacts were imported

**Expected Output:**
```
✅ Successfully imported 25 contacts from your device! 3 contacts were skipped (invalid numbers). You now have 25 total contacts.
```

---

### ✅ Step 2: Verify Contacts Were Imported
```
"ANU, list my WhatsApp contacts"
```

This will show all saved contacts like:
```
Your WhatsApp contacts:
• Mom: +919876543210
• Dad: +919876543211
• Ananya: +919876543212
...
```

---

### ✅ Step 3: Add a Contact Manually (Optional)
If someone is missing:
```
"ANU, add Ananya's WhatsApp contact with number +919876543210"
```

**Expected Output:**
```
✓ Contact 'Ananya' added with number +919876543210
```

---

### ✅ Step 4: Test Sending a Message

#### First Time Setup:
When you send your first message, WhatsApp Web will open and you'll need to:
1. Scan the QR code with your phone's WhatsApp
2. Keep WhatsApp Web logged in for ANU to work

#### Send a Test Message:
```
"ANU, send Ananya a message saying Hey, just testing ANU!"
```

**What Happens:**
1. ANU opens WhatsApp Web (Chrome/Selenium)
2. Searches for the contact "Ananya"
3. Opens the chat
4. Types the message
5. Sends it
6. Confirms success

**Expected Output:**
```
✅ Message sent to Ananya successfully!
```

---

### ✅ Step 5: Test Different Message Types

**Simple Message:**
```
"send Mom a WhatsApp message: I'll be home late"
```

**Longer Message:**
```
"message Dad on WhatsApp saying I'm at the store. Do you need anything? Let me know soon."
```

**Quick Check-in:**
```
"ANU, ask Ananya what she's doing"
```

---

## 🐛 Troubleshooting

### Issue 1: "Contact not found"
**Solution:**
1. Check if contact is in `contacts.json`
2. Try: `"ANU, list my contacts"`
3. If missing: `"ANU, add [name] contact [number]"`
4. Make sure name matches exactly (case-insensitive)

### Issue 2: WhatsApp Web QR Code
**Solution:**
1. Open WhatsApp on your phone
2. Go to Settings → Linked Devices
3. Scan the QR code shown by ANU
4. Keep "Stay signed in" checked

### Issue 3: "WhatsApp Web not responding"
**Solution:**
1. Close any existing WhatsApp Web tabs
2. Restart ANU
3. Try sending message again
4. If still fails, manually log out and log back in to WhatsApp Web

### Issue 4: Selenium/Chrome Driver Issues
**Solution:**
1. Make sure Chrome is installed
2. Check webdriver-manager is installed: `pip install webdriver-manager`
3. Update Chrome to latest version
4. Restart your computer if needed

### Issue 5: Phone Numbers Not Formatted Correctly
**Solution:**
- Indian numbers: Should start with +91 (automatically added for 10-digit numbers)
- US numbers: Should start with +1
- Manually add: `"ANU, add contact with number +91XXXXXXXXXX"`

---

## ✅ Complete Testing Checklist

- [ ] Import device contacts successfully
- [ ] List contacts shows all imported contacts
- [ ] Manually add a new contact
- [ ] Send first message (QR code login)
- [ ] Send message to different contact
- [ ] Send message with special characters
- [ ] Send long message (multi-line)
- [ ] Test with contact names (case-insensitive)
- [ ] Verify message delivered in actual WhatsApp

---

## 📋 Test Scenarios

### Scenario 1: Family Check-in
```
1. "ANU, import all my contacts"
2. "ANU, send Mom a message: Hey Mom, I'm home safe!"
3. "ANU, message Dad: Can you pick me up tomorrow?"
```

### Scenario 2: Friend Coordination
```
1. "ANU, add Ananya's contact +919876543210"
2. "ANU, send Ananya a WhatsApp: What time are we meeting?"
3. "ANU, message Rahul on WhatsApp: Running 10 minutes late"
```

### Scenario 3: Work Communication
```
1. "ANU, send Boss a message: Meeting notes sent via email"
2. "ANU, message Team on WhatsApp: Project update in Slack"
```

---

## 🎯 Success Criteria

WhatsApp integration is working if:
- ✅ Contacts imported from device
- ✅ Can list all contacts
- ✅ Can add contacts manually
- ✅ WhatsApp Web opens automatically
- ✅ Messages sent successfully
- ✅ Recipients receive messages
- ✅ No errors in ANU output
- ✅ Works with different contact names

---

## 🔧 Technical Details

### Files Involved:
- `skills/whatsapp_skill.py` - Main WhatsApp skill
- `skills/whatsapp/whatsapp_client.py` - Selenium automation
- `contacts.json` - Contact storage
- `.env` - API keys (not needed for WhatsApp)

### How It Works:
1. **Contact Import**: Uses AppleScript to read macOS Contacts
2. **Contact Storage**: JSON file with name → phone mapping
3. **Message Sending**: Selenium automates WhatsApp Web
4. **Driver Management**: webdriver-manager handles Chrome driver

---

## 💡 Pro Tips

1. **Keep WhatsApp Web Logged In**: Avoids QR code every time
2. **Use Full Names**: "Ananya Kumar" instead of just "Ananya" if you have multiple contacts
3. **Test with Yourself**: Send messages to your own number first
4. **Check Phone**: Verify messages are actually received
5. **Import Regularly**: Re-import contacts if you add new ones

---

## 🚀 Next Steps After Testing

Once WhatsApp works:
- [ ] Test group messages (coming soon)
- [ ] Test message scheduling (coming soon)
- [ ] Test reading WhatsApp messages (coming soon)
- [ ] Test sending images (coming soon)

---

## 📊 Report Results

After testing, check off what works:
- [ ] ✅ Contact import: WORKING / ❌ NOT WORKING
- [ ] ✅ Send message: WORKING / ❌ NOT WORKING
- [ ] ✅ Multiple contacts: WORKING / ❌ NOT WORKING
- [ ] ✅ QR code login: WORKING / ❌ NOT WORKING

**Notes:**
_Write any issues or observations here..._

---

**Last Updated:** February 14, 2026
**Version:** 1.0
**For:** ANU - Your Caring AI Companion 🌸
