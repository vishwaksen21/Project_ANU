# 📧 Email Reading Setup Guide for ANU

## 🎯 Quick Setup (Gmail)

### Step 1: Enable IMAP in Gmail
1. Go to Gmail Settings (gear icon → See all settings)
2. Click "Forwarding and POP/IMAP" tab
3. Enable IMAP
4. Click "Save Changes"

### Step 2: Create App Password
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** (if not already enabled)
3. Search for "App passwords" in settings
4. Select app: **Mail**
5. Select device: **Other (Custom name)** → Type "ANU"
6. Click **Generate**
7. **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

### Step 3: Add to .env File
Open `/Users/vishwaksen/Desktop/Project_JARVIS/.env` and add:

```env
# Email Configuration
EMAIL_ADDRESS=your.email@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop
IMAP_SERVER=imap.gmail.com
```

Replace:
- `your.email@gmail.com` with your actual Gmail address
- `abcd efgh ijkl mnop` with your generated App Password

### Step 4: Test Email Reading
Restart ANU and try:
```
"ANU, read my emails"
"ANU, check for unread emails"
"ANU, search emails about project"
```

---

## 📧 Setup for Other Email Providers

### Outlook/Hotmail
```env
EMAIL_ADDRESS=your.email@outlook.com
EMAIL_PASSWORD=your_password
IMAP_SERVER=outlook.office365.com
```

### Yahoo Mail
```env
EMAIL_ADDRESS=your.email@yahoo.com
EMAIL_PASSWORD=your_app_password
IMAP_SERVER=imap.mail.yahoo.com
```

### iCloud Mail
```env
EMAIL_ADDRESS=your.email@icloud.com
EMAIL_PASSWORD=your_app_password
IMAP_SERVER=imap.mail.me.com
```

### Custom Domain (e.g., company email)
```env
EMAIL_ADDRESS=you@yourcompany.com
EMAIL_PASSWORD=your_password
IMAP_SERVER=mail.yourcompany.com
```

---

## ✅ Test Your Email Setup

### Test 1: Read Recent Emails
```
"ANU, read my recent emails"
"ANU, show me my last 10 emails"
```

**Expected Output:**
```
📧 Your 5 Most Recent Emails:

1. **Project Update**
   From: boss@company.com
   Date: Thu, 14 Feb 2026 10:30:00
   Preview: Hi team, here's the latest update on the project...

2. **Meeting Reminder**
   From: calendar@google.com
   Date: Thu, 14 Feb 2026 09:15:00
   Preview: You have a meeting scheduled for tomorrow at 2 PM...
```

### Test 2: Check Unread Emails
```
"ANU, check my unread emails"
"ANU, do I have any new emails?"
```

**Expected Output:**
```
📬 You have 3 unread emails!

1. Important Notification
   From: notifications@service.com

2. Weekly Newsletter
   From: newsletter@company.com

3. Friend's Reply
   From: friend@gmail.com
```

### Test 3: Search Emails
```
"ANU, search my emails for invoice"
"ANU, find emails about meeting"
```

**Expected Output:**
```
🔍 Found 12 email(s) matching 'invoice'

Showing 10 most recent:

1. Invoice #12345
   From: billing@company.com
   Date: Wed, 13 Feb 2026 14:20:00

2. Payment Receipt
   From: payments@service.com
   Date: Tue, 12 Feb 2026 11:30:00
```

---

## 🐛 Troubleshooting

### Issue 1: "Email credentials not configured"
**Solution:**
1. Check `.env` file exists in project root
2. Verify EMAIL_ADDRESS and EMAIL_PASSWORD are set
3. Restart ANU after adding credentials

### Issue 2: "Email authentication error"
**Gmail Solution:**
1. Make sure 2-Step Verification is ON
2. Use App Password (not regular password)
3. Remove spaces from App Password
4. Try generating new App Password

**Other Providers:**
1. Check if IMAP is enabled
2. Verify IMAP server address is correct
3. For Yahoo/Outlook, may need App Password too

### Issue 3: "Error accessing INBOX folder"
**Solution:**
1. Log into email normally (web/app)
2. Check if IMAP is enabled
3. Verify no account lockouts
4. Try with fewer emails: `"read 3 emails"`

### Issue 4: Cannot decode subject/body
**Solution:**
- This is usually handled automatically
- Some emails may show "(No preview available)"
- This is normal for encrypted or HTML-only emails

---

## 🎯 Available Commands

### Read Emails:
- "Read my emails"
- "Show me my last 10 emails"
- "Read my recent emails"
- "What's in my inbox?"

### Check Unread:
- "Check my unread emails"
- "Do I have any new emails?"
- "Any unread messages?"
- "Check my inbox"

### Search:
- "Search my emails for [keyword]"
- "Find emails about [topic]"
- "Search inbox for [query]"
- "Look for emails from [person]"

---

## 🔐 Security Best Practices

### ✅ DO:
- Use App Passwords (not regular passwords)
- Keep .env file private (it's in .gitignore)
- Enable 2-Step Verification
- Regularly review app access
- Use strong, unique passwords

### ❌ DON'T:
- Share your .env file
- Commit credentials to Git
- Use regular password in EMAIL_PASSWORD
- Disable 2-Step Verification
- Use same password everywhere

---

## 📊 Features

### Current Features:
- ✅ Read recent emails (5, 10, 20, etc.)
- ✅ Check unread emails count + summary
- ✅ Search emails by keyword
- ✅ Show subject, sender, date, preview
- ✅ Handle multiple folders (INBOX, Sent, etc.)
- ✅ Decode special characters

### Coming Soon:
- ⏳ Reply to emails
- ⏳ Mark as read/unread
- ⏳ Delete emails
- ⏳ Move to folders
- ⏳ Read full email body
- ⏳ Download attachments
- ⏳ Send new emails

---

## 🎯 Success Criteria

Email reading is working if:
- ✅ Can authenticate with email account
- ✅ Can read recent emails
- ✅ Can check unread count
- ✅ Can search by keyword
- ✅ Subject and sender display correctly
- ✅ Date and preview show up
- ✅ No authentication errors
- ✅ Works with your email provider

---

## 💡 Pro Tips

1. **Test with test email first**: Send yourself a test email
2. **Use specific searches**: "Search for emails from boss" is better than just "search emails"
3. **Check unread regularly**: "ANU, check my unread emails" every morning
4. **Keep app password safe**: Store it only in .env file
5. **Multiple email accounts**: Can add more later with different skills

---

## 📋 Setup Checklist

- [ ] IMAP enabled in email account
- [ ] 2-Step Verification enabled (Gmail)
- [ ] App Password generated
- [ ] Credentials added to .env file
- [ ] .env file in project root
- [ ] ANU restarted after adding credentials
- [ ] Test: Read recent emails
- [ ] Test: Check unread emails
- [ ] Test: Search emails
- [ ] All tests passed

---

## 🚀 Quick Start Example

1. **Setup:**
```bash
# Edit .env file
nano .env

# Add these lines:
EMAIL_ADDRESS=yourname@gmail.com
EMAIL_PASSWORD=your_app_password_here
IMAP_SERVER=imap.gmail.com

# Save and exit (Ctrl+X, Y, Enter)
```

2. **Restart ANU:**
```bash
python3 main.py
```

3. **Test:**
```
"ANU, read my emails"
```

4. **Success!** 🎉

---

**Last Updated:** February 14, 2026
**Version:** 1.0
**For:** ANU - Your Caring AI Companion 🌸
