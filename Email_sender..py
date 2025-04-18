from flask import Flask, request, jsonify
import smtplib
import ssl
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from flask_cors import CORS

# Set up logging
logging.basicConfig(
    filename='email_sending.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Default email template
DEFAULT_EMAIL_TEMPLATE = """
Dear Candidate,

Thank you for applying for the internship position. We have received your application and resume.

Please fill out the Google Form to proceed to the first round:  
[https://docs.google.com/forms/d/1mubE2MraLkiYETS0vWjVuRjwocVnkuIMHb989Fir5jc/edit]

We will contact you for the next steps after reviewing your responses.

Best regards,  
Elint AI
"""

def mask_name(name):
    """Mask a name (e.g., 'Sumit Jha' -> 'S**** J**')"""
    if not name or not isinstance(name, str) or name.strip() == '':
        return "Unknown"
    
    parts = name.strip().split()
    masked_parts = []
    
    for part in parts:
        if len(part) > 0:
            masked = part[0] + '*' * (len(part) - 1)
            masked_parts.append(masked)
    
    return " ".join(masked_parts)

def mask_email(email):
    """Mask an email (e.g., 'sumitjha@gmail.com' -> 's*@g**.com')"""
    if not email or not isinstance(email, str) or email.strip() == '':
        return "unknown@email.com"
    
    try:
        username, domain = email.split('@')
        domain_parts = domain.split('.')
        
        masked_username = username[0] + '*' * (len(username) - 1)
        masked_domain = domain_parts[0][0] + '*' * (len(domain_parts[0]) - 1)
        masked_tld = domain_parts[1]
        
        return f"{masked_username}@{masked_domain}.{masked_tld}"
    except:
        return "m*@e**.com"

def send_email(service_type, sender_email, password, recipient_email, subject, body):
    """Send an email using SMTP based on the service type (gmail or godaddy)"""
    if not recipient_email or recipient_email.strip() == '':
        return False, "No recipient email provided"
    
    # Configure SMTP settings based on service type
    if service_type.lower() == 'gmail':
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
    elif service_type.lower() == 'godaddy':
        smtp_server = "smtpout.secureserver.net"
        smtp_port = 587
    else:
        return False, f"Unknown email service type: {service_type}"
        
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        
        return True, "Email sent successfully"
    except Exception as e:
        error_msg = f"Failed to send email: {str(e)}"
        logging.error(error_msg)
        return False, error_msg

@app.route('/api/send-email', methods=['POST'])
def send_emails_api():
    """API endpoint to send emails to multiple recipients"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400
            
        # Extract email service configuration
        service_type = data.get('service_type')  # 'gmail' or 'godaddy'
        sender_email = data.get('sender_email')
        password = data.get('password')
        
        if not service_type or not sender_email or not password:
            return jsonify({
                "status": "error", 
                "message": "Missing required fields: service_type, sender_email, or password"
            }), 400
            
        # Extract email content
        subject = data.get('subject', 'Your AI Position Application Results')
        email_template = data.get('email_template', DEFAULT_EMAIL_TEMPLATE)
        
        # Extract recipient emails
        recipients = data.get('recipients', [])
        if not recipients or not isinstance(recipients, list):
            return jsonify({"status": "error", "message": "No valid recipients provided"}), 400
            
        # Process each recipient
        results = []
        for recipient in recipients:
            email = recipient.get('email')
            name = recipient.get('name', '')
            
            if not email:
                results.append({
                    "email": "unknown@email.com",
                    "masked_email": "unknown@email.com",
                    "masked_name": "Unknown",
                    "status": "Failed: No email provided"
                })
                continue
                
            # Personalize email if needed
            personalized_body = email_template.format(
                masked_name=mask_name(name),
                **recipient
            ) if "{" in email_template else email_template
            
            # Send the email
            success, message = send_email(
                service_type, 
                sender_email, 
                password, 
                email, 
                subject, 
                personalized_body
            )
            
            # Log the result
            masked_email = mask_email(email)
            masked_name = mask_name(name)
            status = "Sent" if success else f"Failed: {message}"
            
            log_message = f"Email to {masked_email}: {status}"
            if success:
                logging.info(log_message)
            else:
                logging.error(log_message)
                
            results.append({
                "email": email,
                "masked_email": masked_email,
                "masked_name": masked_name,
                "status": status
            })
            
        return jsonify({
            "status": "success",
            "message": f"Processed {len(results)} emails",
            "results": results
        })
            
    except Exception as e:
        error_message = f"Error processing request: {str(e)}"
        logging.error(error_message)
        return jsonify({"status": "error", "message": error_message}), 500

@app.route('/api/test', methods=['GET'])
def test_api():
    """Simple endpoint to test if the API is running"""
    return jsonify({
        "status": "success",
        "message": "Email API is running!"
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)