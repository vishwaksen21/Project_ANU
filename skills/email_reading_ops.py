"""
Email Reading Operations Skill for ANU
Read and manage emails using IMAP
"""

import imaplib
import email
from email.header import decode_header
import os
from datetime import datetime, timedelta

def read_recent_emails(num_emails=5, folder="INBOX"):
    """
    Read recent emails from inbox
    
    Args:
        num_emails: Number of recent emails to read (1-20)
        folder: Email folder to read from (default: INBOX)
    """
    try:
        # Get email credentials from environment
        email_address = os.environ.get("EMAIL_ADDRESS", "")
        email_password = os.environ.get("EMAIL_PASSWORD", "")
        imap_server = os.environ.get("IMAP_SERVER", "imap.gmail.com")
        
        if not email_address or not email_password:
            return "❌ Email credentials not configured. Please set EMAIL_ADDRESS and EMAIL_PASSWORD in your .env file.\n\nFor Gmail:\n- EMAIL_ADDRESS=your.email@gmail.com\n- EMAIL_PASSWORD=your_app_password\n- IMAP_SERVER=imap.gmail.com\n\nNote: For Gmail, use an App Password (not your regular password)."
        
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, email_password)
        
        # Select mailbox
        mail.select(folder)
        
        # Search for all emails
        status, messages = mail.search(None, "ALL")
        
        if status != "OK":
            return f"❌ Error accessing {folder} folder"
        
        email_ids = messages[0].split()
        
        if not email_ids:
            return f"📧 No emails found in {folder}"
        
        # Get the most recent emails
        recent_ids = email_ids[-num_emails:][::-1]  # Last N, reversed for newest first
        
        result = f"📧 Your {len(recent_ids)} Most Recent Emails:\n\n"
        
        for i, email_id in enumerate(recent_ids, 1):
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            
            if status != "OK":
                continue
            
            # Parse email
            msg = email.message_from_bytes(msg_data[0][1])
            
            # Decode subject
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
            
            # Get sender
            from_header = msg.get("From", "Unknown")
            
            # Get date
            date_header = msg.get("Date", "Unknown")
            
            # Get body preview
            body_preview = _get_email_body_preview(msg)
            
            result += f"{i}. **{subject}**\n"
            result += f"   From: {from_header}\n"
            result += f"   Date: {date_header}\n"
            result += f"   Preview: {body_preview}\n\n"
        
        mail.close()
        mail.logout()
        
        return result.strip()
        
    except imaplib.IMAP4.error as e:
        return f"❌ Email authentication error: {str(e)}\n\nFor Gmail:\n1. Enable 2-Step Verification\n2. Generate an App Password\n3. Use the App Password in EMAIL_PASSWORD"
    except Exception as e:
        return f"❌ Error reading emails: {str(e)}"


def check_unread_emails():
    """Check for unread emails and return count + summary"""
    try:
        email_address = os.environ.get("EMAIL_ADDRESS", "")
        email_password = os.environ.get("EMAIL_PASSWORD", "")
        imap_server = os.environ.get("IMAP_SERVER", "imap.gmail.com")
        
        if not email_address or not email_password:
            return "❌ Email credentials not configured. Set EMAIL_ADDRESS and EMAIL_PASSWORD in .env"
        
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, email_password)
        mail.select("INBOX")
        
        # Search for unread emails
        status, messages = mail.search(None, "UNSEEN")
        
        if status != "OK":
            return "❌ Error checking unread emails"
        
        unread_ids = messages[0].split()
        unread_count = len(unread_ids)
        
        if unread_count == 0:
            mail.close()
            mail.logout()
            return "✅ You have no unread emails. Your inbox is all caught up!"
        
        # Get details of recent unread emails (up to 5)
        result = f"📬 You have {unread_count} unread email{'s' if unread_count != 1 else ''}!\n\n"
        
        recent_unread = unread_ids[-5:][::-1]  # Last 5, newest first
        
        for i, email_id in enumerate(recent_unread, 1):
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            
            if status != "OK":
                continue
            
            msg = email.message_from_bytes(msg_data[0][1])
            
            # Decode subject
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
            
            from_header = msg.get("From", "Unknown")
            
            result += f"{i}. {subject}\n"
            result += f"   From: {from_header}\n\n"
        
        if unread_count > 5:
            result += f"...and {unread_count - 5} more unread emails"
        
        mail.close()
        mail.logout()
        
        return result.strip()
        
    except Exception as e:
        return f"❌ Error checking unread emails: {str(e)}"


def search_emails(query, num_results=10):
    """
    Search emails by keyword
    
    Args:
        query: Search keyword (searches in subject and body)
        num_results: Number of results to return (1-20)
    """
    try:
        email_address = os.environ.get("EMAIL_ADDRESS", "")
        email_password = os.environ.get("EMAIL_PASSWORD", "")
        imap_server = os.environ.get("IMAP_SERVER", "imap.gmail.com")
        
        if not email_address or not email_password:
            return "❌ Email credentials not configured."
        
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, email_password)
        mail.select("INBOX")
        
        # Search in subject
        status, subject_msgs = mail.search(None, f'SUBJECT "{query}"')
        
        # Search in body
        status2, body_msgs = mail.search(None, f'BODY "{query}"')
        
        # Combine results
        all_ids = set()
        if status == "OK" and subject_msgs[0]:
            all_ids.update(subject_msgs[0].split())
        if status2 == "OK" and body_msgs[0]:
            all_ids.update(body_msgs[0].split())
        
        if not all_ids:
            mail.close()
            mail.logout()
            return f"🔍 No emails found matching '{query}'"
        
        # Get most recent matches
        sorted_ids = sorted(list(all_ids), reverse=True)[:num_results]
        
        result = f"🔍 Found {len(all_ids)} email(s) matching '{query}'\n\nShowing {len(sorted_ids)} most recent:\n\n"
        
        for i, email_id in enumerate(sorted_ids, 1):
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            
            if status != "OK":
                continue
            
            msg = email.message_from_bytes(msg_data[0][1])
            
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
            
            from_header = msg.get("From", "Unknown")
            date_header = msg.get("Date", "Unknown")
            
            result += f"{i}. {subject}\n"
            result += f"   From: {from_header}\n"
            result += f"   Date: {date_header}\n\n"
        
        mail.close()
        mail.logout()
        
        return result.strip()
        
    except Exception as e:
        return f"❌ Error searching emails: {str(e)}"


def _get_email_body_preview(msg, max_length=100):
    """Extract a preview of the email body"""
    body = ""
    
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode()
                    break
                except:
                    continue
    else:
        try:
            body = msg.get_payload(decode=True).decode()
        except:
            body = ""
    
    # Clean up body
    body = body.strip().replace("\n", " ").replace("\r", "")
    
    # Return preview
    if len(body) > max_length:
        return body[:max_length] + "..."
    return body if body else "(No preview available)"


# Register the skill
def register():
    from core.skill import Skill
    
    class EmailReadingSkill(Skill):
        @property
        def name(self):
            return "email_reading_skill"
        
        def get_tools(self):
            return [
                {
                    "type": "function",
                    "function": {
                        "name": "read_recent_emails",
                        "description": "Read the most recent emails from inbox. Shows subject, sender, date, and preview.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "num_emails": {
                                    "type": "integer",
                                    "description": "Number of recent emails to read (1-20, default: 5)",
                                    "default": 5
                                },
                                "folder": {
                                    "type": "string",
                                    "description": "Email folder to read from (default: INBOX)",
                                    "default": "INBOX"
                                }
                            },
                            "required": []
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "check_unread_emails",
                        "description": "Check for unread emails and get a summary of recent unread messages",
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
                        "name": "search_emails",
                        "description": "Search emails by keyword in subject or body",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "Search keyword or phrase"
                                },
                                "num_results": {
                                    "type": "integer",
                                    "description": "Number of results to return (1-20, default: 10)",
                                    "default": 10
                                }
                            },
                            "required": ["query"]
                        }
                    }
                }
            ]
        
        def get_functions(self):
            return {
                "read_recent_emails": read_recent_emails,
                "check_unread_emails": check_unread_emails,
                "search_emails": search_emails
            }
    
    return EmailReadingSkill()
