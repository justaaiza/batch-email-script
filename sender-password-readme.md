# Email Script Configuration Guide

How to configure your `sender` and `password` to send emails using the Job Fair email script.

---

## 1. Sender Email (`sender`)

The `sender` field should be the email address you want to send emails from.

```python
sender = "yourname@gmail.com"
```

> Make sure it's the email account you will use to authenticate with SMTP.  

---

## 2. App Password (`password`)

Gmail and other providers require an App Password instead of your normal password for scripts and apps.

### Steps to Generate an App Password (Gmail)

1. Go to Google Account Security: (https://myaccount.google.com/security)
2. Enable 2-Step Verification if not already enabled.
3. Go to App Passwords: (https://myaccount.google.com/apppasswords).
4. Enter a name for your password, e.g., `Python Email Script`, then click Create.
5. Copy the 16-character password shown (remove spaces when pasting into code).

```python
password = "abcdefghijklmnop"  # 16-character app password
```

> ⚠️ Do not use your normal Google/FAST password.  
> 🔒 Keep this password secret and out of version control.

---

## 3. Putting It Together

In your script:

```python
sender   = "yourname@gmail.com"
password = "abcdefghijklmnop"
```

---

## 4. Quick Test

Before sending emails to all students:

1. Add your own email to `recipient_list.txt`
2. Run the script
3. Confirm you receive the test email

---

## 5. Important Notes

- Gmail daily limit: ~100–150 emails per account per day.
- Each App Password is account-specific.
- You can revoke App Passwords anytime from your Google Account settings.
- Never commit your `password` to a public repository — consider using environment variables or a `.env` file.