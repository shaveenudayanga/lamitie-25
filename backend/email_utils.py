"""
=============================================================================
EMAIL UTILITIES MODULE
=============================================================================
This file handles:
1. QR Code generation (in-memory, no files saved to disk)
2. Email sending with HTML templates and attachments

How it works:
1. When a student registers, we generate a QR code with their index number
2. The QR code is created in memory (RAM), not saved as a file
3. We send an HTML email with the QR code attached as an image
4. The email includes event details and instructions

Libraries Used:
- qrcode: Creates QR code images
- Pillow (PIL): Image processing
- fastapi-mail: Sends emails asynchronously
=============================================================================
"""

import os
import io
import tempfile
from pathlib import Path
from dotenv import load_dotenv
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

# Load environment variables
load_dotenv()


# =============================================================================
# EMAIL CONFIGURATION
# =============================================================================

def get_mail_config() -> ConnectionConfig:
    """
    Get email configuration from environment variables.
    
    This function creates a configuration object that tells
    fastapi-mail how to connect to our email server.
    
    Returns:
        ConnectionConfig: Email server configuration
        
    Raises:
        ValueError: If required environment variables are missing
    """
    # Get configuration from environment
    mail_username = os.getenv("MAIL_USERNAME")
    mail_password = os.getenv("MAIL_PASSWORD")
    mail_server = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    mail_port = int(os.getenv("MAIL_PORT", "587"))
    mail_from_name = os.getenv("MAIL_FROM_NAME", "Lamitie 2025")
    
    # Validate required settings
    if not mail_username or not mail_password:
        raise ValueError(
            "Email configuration is incomplete! "
            "Please set MAIL_USERNAME and MAIL_PASSWORD in your .env file."
        )
    
    # Create and return configuration
    return ConnectionConfig(
        MAIL_USERNAME=mail_username,
        MAIL_PASSWORD=mail_password,
        MAIL_FROM=mail_username,
        MAIL_PORT=mail_port,
        MAIL_SERVER=mail_server,
        MAIL_FROM_NAME=mail_from_name,
        MAIL_STARTTLS=True,       # Use TLS encryption
        MAIL_SSL_TLS=False,       # Don't use SSL (we're using STARTTLS)
        USE_CREDENTIALS=True,     # Use username/password authentication
        VALIDATE_CERTS=True,      # Validate SSL certificates
    )


# =============================================================================
# QR CODE GENERATION
# =============================================================================

def generate_qr_code(data: str) -> bytes:
    """
    Generate a QR code image containing the provided data.
    
    The QR code is generated in memory and returned as PNG bytes.
    No files are saved to disk.
    
    Args:
        data: The string to encode in the QR code (e.g., index number)
        
    Returns:
        bytes: PNG image data of the QR code
        
    Example:
        qr_bytes = generate_qr_code("2024CS001")
        # qr_bytes now contains PNG image data
        
    Technical Details:
    - Error Correction Level H: Can recover up to 30% damage
    - Box Size 10: Each QR "square" is 10 pixels
    - Border 4: Standard white border around the QR code
    - High contrast colors for easy scanning
    """
    # Create QR code instance with settings optimized for reliability
    qr = qrcode.QRCode(
        version=1,  # Version 1 = 21x21 matrix (auto-adjusts if needed)
        error_correction=ERROR_CORRECT_H,  # Highest error correction
        box_size=10,  # Size of each box in pixels
        border=4,  # Standard border size
    )
    
    # Add the data to encode
    qr.add_data(data)
    qr.make(fit=True)  # Auto-adjust size if needed
    
    # Create the image with high contrast colors
    # Dark blue on white for easy scanning and nice appearance
    qr_image = qr.make_image(
        fill_color="#1a365d",  # Dark blue for the QR pattern
        back_color="white"     # White background
    )
    
    # Convert to PNG bytes in memory
    # BytesIO acts like a file but lives in RAM
    buffer = io.BytesIO()
    qr_image.save(buffer, format="PNG")
    buffer.seek(0)  # Reset to beginning so we can read it
    
    return buffer.getvalue()


# =============================================================================
# EMAIL SENDING
# =============================================================================

def create_email_html(student_name: str, index_number: str) -> str:
    """
    Create the HTML content for the invitation email.
    
    This generates a professional-looking HTML email with:
    - Event branding
    - Personalized greeting
    - Event details
    - Instructions for the QR code
    - Contact information
    
    Args:
        student_name: The student's full name for personalization
        index_number: The student's index number for reference
        
    Returns:
        str: Complete HTML email content
    """
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Invitation to Lamitie 2025</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width: 600px; margin: 0 auto; background-color: #ffffff;">
            <!-- Header Banner -->
            <tr>
                <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
                    <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: 700;">
                        🎉 LAMITIE 2025 🎉
                    </h1>
                    <p style="color: #e0e0e0; margin: 10px 0 0 0; font-size: 16px;">
                        University Cultural Festival
                    </p>
                </td>
            </tr>
            
            <!-- Main Content -->
            <tr>
                <td style="padding: 40px 30px;">
                    <!-- Greeting -->
                    <h2 style="color: #333333; margin: 0 0 20px 0; font-size: 24px;">
                        Dear {student_name},
                    </h2>
                    
                    <p style="color: #555555; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                        Congratulations! 🎊 Your registration for <strong>Lamitie 2025</strong> has been confirmed. 
                        We are thrilled to have you join us for this spectacular celebration!
                    </p>
                    
                    <!-- QR Code Section -->
                    <div style="background-color: #f8f9fa; border-radius: 12px; padding: 30px; text-align: center; margin: 30px 0;">
                        <h3 style="color: #333333; margin: 0 0 15px 0; font-size: 18px;">
                            📱 Your Entry Pass
                        </h3>
                        <p style="color: #666666; font-size: 14px; margin: 0 0 20px 0;">
                            Present this QR code at the entrance for quick check-in
                        </p>
                        <img src="cid:qr_code" alt="Your QR Code" style="max-width: 200px; height: auto; border: 4px solid #667eea; border-radius: 8px;">
                        <p style="color: #888888; font-size: 12px; margin: 15px 0 0 0;">
                            Index Number: <strong>{index_number}</strong>
                        </p>
                    </div>
                    
                    <!-- Instructions -->
                    <div style="margin: 30px 0;">
                        <h3 style="color: #333333; margin: 0 0 15px 0; font-size: 18px;">
                            📋 Important Instructions
                        </h3>
                        <ul style="color: #555555; font-size: 14px; line-height: 1.8; padding-left: 20px; margin: 0;">
                            <li>Save this email or take a screenshot of your QR code</li>
                            <li>Show the QR code at the registration desk upon arrival</li>
                            <li>Carry your student ID for verification</li>
                            <li>Arrive at least 15 minutes before the event starts</li>
                        </ul>
                    </div>
                    
                    <!-- Event Details -->
                    <div style="background-color: #667eea; border-radius: 12px; padding: 25px; margin: 30px 0;">
                        <h3 style="color: #ffffff; margin: 0 0 15px 0; font-size: 18px;">
                            📅 Event Details
                        </h3>
                        <table role="presentation" width="100%" cellspacing="0" cellpadding="5">
                            <tr>
                                <td style="color: #e0e0e0; font-size: 14px; width: 30%;">Date:</td>
                                <td style="color: #ffffff; font-size: 14px; font-weight: 600;">To Be Announced</td>
                            </tr>
                            <tr>
                                <td style="color: #e0e0e0; font-size: 14px;">Time:</td>
                                <td style="color: #ffffff; font-size: 14px; font-weight: 600;">To Be Announced</td>
                            </tr>
                            <tr>
                                <td style="color: #e0e0e0; font-size: 14px;">Venue:</td>
                                <td style="color: #ffffff; font-size: 14px; font-weight: 600;">To Be Announced</td>
                            </tr>
                        </table>
                    </div>
                    
                    <!-- Closing -->
                    <p style="color: #555555; font-size: 16px; line-height: 1.6; margin: 20px 0;">
                        We can't wait to see you there! Get ready for an unforgettable experience 
                        filled with music, dance, food, and memories. 🌟
                    </p>
                    
                    <p style="color: #555555; font-size: 16px; margin: 20px 0 0 0;">
                        Best regards,<br>
                        <strong style="color: #667eea;">The Lamitie 2025 Organizing Committee</strong>
                    </p>
                </td>
            </tr>
            
            <!-- Footer -->
            <tr>
                <td style="background-color: #333333; padding: 25px 30px; text-align: center;">
                    <p style="color: #999999; font-size: 12px; margin: 0;">
                        This is an automated email. Please do not reply directly to this message.
                    </p>
                    <p style="color: #999999; font-size: 12px; margin: 10px 0 0 0;">
                        © 2025 Lamitie - University Cultural Festival
                    </p>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


async def send_invitation_email(
    recipient_email: str,
    student_name: str,
    index_number: str
) -> bool:
    """
    Send an invitation email with a QR code to the student.
    
    This function:
    1. Generates a QR code with the student's index number
    2. Creates an HTML email with event details
    3. Attaches the QR code to the email
    4. Sends the email to the student
    
    Args:
        recipient_email: The student's email address
        student_name: The student's name (for personalization)
        index_number: The student's index number (encoded in QR)
        
    Returns:
        bool: True if email was sent successfully, False otherwise
        
    Note:
        This function is designed to run as a background task
        so it doesn't slow down the API response.
    """
    temp_file_path = None
    try:
        # Step 1: Generate the QR code and save to temp file
        qr_code_bytes = generate_qr_code(index_number)
        
        # Create a temporary file for the QR code
        # fastapi-mail requires a file path, not bytes
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, 
            suffix=f"_qr_{index_number}.png"
        )
        temp_file_path = temp_file.name
        temp_file.write(qr_code_bytes)
        temp_file.close()
        
        # Step 2: Create the HTML email content
        html_content = create_email_html(student_name, index_number)
        
        # Step 3: Get email configuration
        conf = get_mail_config()
        
        # Step 4: Create the email message with file path attachment
        message = MessageSchema(
            subject="🎉 Invitation to Lamitie 2025 - Your Entry Pass Inside!",
            recipients=[recipient_email],
            body=html_content,
            subtype=MessageType.html,
            attachments=[
                {
                    "file": temp_file_path,
                    "headers": {
                        "Content-ID": "<qr_code>",
                        "Content-Disposition": 'inline; filename="qr_code.png"',
                    },
                    "mime_type": "image",
                    "mime_subtype": "png",
                }
            ],
        )
        
        # Step 5: Send the email
        fm = FastMail(conf)
        await fm.send_message(message)
        
        print(f"✅ Email sent successfully to {recipient_email}")
        return True
        
    except Exception as e:
        # Log the error but don't crash the app
        print(f"❌ Failed to send email to {recipient_email}: {str(e)}")
        return False
    
    finally:
        # Clean up: Delete the temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception:
                pass
