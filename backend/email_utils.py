"""
=============================================================================
EMAIL UTILITIES MODULE - L'AMITIÉ 2K25 (Lord of the Rings Theme)
=============================================================================
This file handles:
1. QR Code generation (in-memory, parchment-styled)
2. 2-Page PDF ticket generation (Cover + Personalized page)
3. Lord of the Rings themed HTML email sending

How it works:
1. When a student registers, we generate a QR code with their index number
2. A 2-page PDF is created: Page 1 = invitation cover, Page 2 = QR + details
3. We send a themed HTML email with the PDF attached
4. The email includes event details in LOTR-style language

Libraries Used:
- qrcode: Creates QR code images
- Pillow (PIL): Image processing and PDF generation
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
from PIL import Image, ImageDraw, ImageFont
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

# Load environment variables
load_dotenv()

# =============================================================================
# THEME CONSTANTS - LORD OF THE RINGS
# =============================================================================

# Colors - "Royal Blood" Palette
PARCHMENT_COLOR = (245, 235, 220)  # Creamy parchment background
INK_BROWN = "#3E2723"              # Dark Chocolate Brown (primary text)
BURGUNDY_ACCENT = "#800000"        # Deep Burgundy (accent text for dates/venue/names)
GOLD_ACCENT = "#C5A059"            # Metallic gold (kept for email theme)
DARK_SLATE = "#1a1a1a"             # Dark mode background
FOREST_GREEN = "#1a2f1a"           # Alternative dark background

# Asset paths
ASSETS_DIR = Path(__file__).parent / "assets"
INVITATION_PAGE1_PATH = ASSETS_DIR / "invitation_1.png"
INVITATION_PAGE2_PATH = ASSETS_DIR / "invitation_2.png"

# Event Details (Constants)
EVENT_DATE = "25th January 2026"
EVENT_TIME = "1.00 P.M"
EVENT_VENUE = "Willuda Inn"
EVENT_VENUE_SUB = "Godagama"


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
    mail_from_name = os.getenv("MAIL_FROM_NAME", "L'amitié 2k25")
    
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

def generate_qr_code(
    data: str, 
    size: tuple[int, int] = None,
    transparent: bool = False,
    parchment_style: bool = True
) -> Image.Image:
    """
    Generate a QR code image containing the provided data.
    
    The QR code is generated in memory and returned as a PIL Image.
    Can be styled to match the parchment/LOTR theme.
    
    Args:
        data: The string to encode in the QR code (e.g., index number)
        size: Optional tuple (width, height) to resize the QR code
        transparent: If True, makes the background transparent
        parchment_style: If True, uses parchment-friendly colors
        
    Returns:
        Image.Image: PIL Image of the QR code
        
    Example:
        qr_image = generate_qr_code("2024CS001", size=(300, 300))
        
    Technical Details:
    - Error Correction Level H: Can recover up to 30% damage
    - Box Size 10: Each QR "square" is 10 pixels
    - Border 2: Minimal border for cleaner integration
    - Theme-matched colors for the LOTR aesthetic
    """
    # Create QR code instance with settings optimized for reliability
    qr = qrcode.QRCode(
        version=1,  # Version 1 = 21x21 matrix (auto-adjusts if needed)
        error_correction=ERROR_CORRECT_H,  # Highest error correction
        box_size=10,  # Size of each box in pixels
        border=2,  # Smaller border for cleaner look
    )
    
    # Add the data to encode
    qr.add_data(data)
    qr.make(fit=True)  # Auto-adjust size if needed
    
    # Choose colors based on style
    if parchment_style:
        fill_color = INK_BROWN  # Dark brown ink
        back_color = PARCHMENT_COLOR if not transparent else (0, 0, 0, 0)
    else:
        fill_color = "#1a365d"  # Dark blue
        back_color = "white" if not transparent else (0, 0, 0, 0)
    
    # Create the image
    if transparent:
        qr_image = qr.make_image(
            fill_color=fill_color,
            back_color="transparent"
        ).convert("RGBA")
        # Make background truly transparent
        datas = qr_image.getdata()
        new_data = []
        for item in datas:
            if item[0] > 200 and item[1] > 200 and item[2] > 200:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        qr_image.putdata(new_data)
    else:
        qr_image = qr.make_image(
            fill_color=fill_color,
            back_color=back_color
        ).convert("RGB")
    
    # Resize if specified
    if size:
        qr_image = qr_image.resize(size, Image.LANCZOS)
    
    return qr_image


def generate_qr_code_bytes(data: str) -> bytes:
    """
    Generate a QR code and return as PNG bytes.
    Legacy function for backward compatibility.
    
    Args:
        data: The string to encode in the QR code
        
    Returns:
        bytes: PNG image data of the QR code
    """
    qr_image = generate_qr_code(data, parchment_style=False)
    buffer = io.BytesIO()
    qr_image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()


# =============================================================================
# PDF TICKET GENERATION
# =============================================================================

def get_fantasy_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """
    Get DejaVu Serif font for the PDF attachment.
    
    Args:
        size: Font size in pixels
        bold: Whether to use bold variant
        
    Returns:
        ImageFont: The loaded font
    """
    # List of DejaVu Serif fonts to try (in order of preference)
    font_candidates = [
        # DejaVu Serif (priority)
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        # Alternative paths
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        # Fallback to Liberation Serif
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        # macOS fonts
        "/System/Library/Fonts/Times.ttc",
        "/Library/Fonts/Times New Roman Bold.ttf" if bold else "/Library/Fonts/Times New Roman.ttf",
        # Windows fonts
        "C:/Windows/Fonts/timesbd.ttf" if bold else "C:/Windows/Fonts/times.ttf",
        "C:/Windows/Fonts/times.ttf",
    ]
    
    for font_path in font_candidates:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                continue
    
    # Fallback to default font
    try:
        return ImageFont.truetype("DejaVuSerif.ttf", size)
    except Exception:
        return ImageFont.load_default()


def get_standard_serif_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """
    Get a standard serif font (bypasses LOTR fonts) for decorative elements.
    Uses only system serif fonts for cleaner rendering of symbols.
    
    Args:
        size: Font size in pixels
        bold: Whether to use bold variant
        
    Returns:
        ImageFont: The loaded system serif font
    """
    font_candidates = [
        # Linux system fonts (serif)
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf" if bold else "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
        # macOS fonts
        "/System/Library/Fonts/Times.ttc",
        "/Library/Fonts/Times New Roman Bold.ttf" if bold else "/Library/Fonts/Times New Roman.ttf",
        # Windows fonts
        "C:/Windows/Fonts/timesbd.ttf" if bold else "C:/Windows/Fonts/times.ttf",
        "C:/Windows/Fonts/georgiab.ttf" if bold else "C:/Windows/Fonts/georgia.ttf",
    ]
    
    for font_path in font_candidates:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                continue
    
    # Fallback to default font
    try:
        return ImageFont.truetype("DejaVuSerif.ttf", size)
    except Exception:
        return ImageFont.load_default()


def generate_ticket_pdf(
    student_name: str,
    index_number: str,
    event_date: str = EVENT_DATE,
    event_time: str = EVENT_TIME,
    event_venue: str = EVENT_VENUE,
    event_venue_sub: str = EVENT_VENUE_SUB
) -> bytes:
    """
    Generate a 2-page PDF ticket for L'amitié 2k25.
    
    Page 1: invitation_1.png as background
    Page 2: invitation_2.png with QR code overlaid
    
    Args:
        student_name: The student's full name
        index_number: The student's index number (encoded in QR)
        event_date: Event date string (e.g., "01st February 2025")
        event_time: Event time string (e.g., "3.00 P.M")
        event_venue: Main venue name (e.g., "Willuda Inn")
        event_venue_sub: Sub-location (e.g., "Godagama")
        
    Returns:
        bytes: PDF file as bytes (ready for email attachment)
    """
    # Load background images for each page
    if INVITATION_PAGE1_PATH.exists():
        background1 = Image.open(INVITATION_PAGE1_PATH).convert("RGBA")
    else:
        # Create a fallback parchment if image not found
        background1 = Image.new("RGBA", (595, 842), (*PARCHMENT_COLOR, 255))
    
    if INVITATION_PAGE2_PATH.exists():
        background2 = Image.open(INVITATION_PAGE2_PATH).convert("RGBA")
    else:
        # Create a fallback parchment if image not found
        background2 = Image.new("RGBA", (595, 842), (*PARCHMENT_COLOR, 255))
    
    # Get dimensions from background
    page_width, page_height = background1.size
    center_x = page_width // 2
    
    # Load fonts at various sizes (2x increase for better readability)
    font_title_large = get_fantasy_font(104, bold=True)
    font_title = get_fantasy_font(84, bold=True)
    font_name = get_fantasy_font(96, bold=True)
    font_body = get_fantasy_font(64)
    font_body_small = get_fantasy_font(52)
    font_label = get_fantasy_font(48)
    font_event_detail = get_fantasy_font(76, bold=True)
    font_venue = get_fantasy_font(96, bold=True)
    font_venue_sub = get_fantasy_font(60)
    
    # Decorative divider font (standard serif, not LOTR)
    font_divider = get_standard_serif_font(52)
    
    # =========================================================================
    # PAGE 1: Use invitation_1.png as-is (no text overlay)
    # =========================================================================
    
    page1 = background1.convert("RGB")
    
    # =========================================================================
    # PAGE 2: QR Code Page with invitation_2.png background
    # =========================================================================
    
    page2 = background2.copy().convert("RGB")
    draw2 = ImageDraw.Draw(page2)
    
    # Starting Y position (after logo area)
    current_y = int(page_height * 0.32)
    
    # "SCAN ME AT THE ENTRANCE"
    draw2.text(
        (center_x, current_y),
        "Scan me at the Entrance",
        font=font_title,
        fill=INK_BROWN,
        anchor="mm"
    )
    current_y += 125
    
    # Generate QR code (transparent background to blend with parchment)
    qr_size = int(min(page_width, page_height) * 0.45)
    qr_image = generate_qr_code(
        index_number, 
        size=(qr_size, qr_size),
        transparent=True,
        parchment_style=True
    )
    
    # Paste QR code (centered horizontally)
    qr_x = center_x - qr_size // 2
    qr_y = current_y
    
    # Convert page2 to RGBA for transparent paste
    page2_rgba = page2.convert("RGBA")
    page2_rgba.paste(qr_image, (qr_x, qr_y), qr_image)
    page2 = page2_rgba.convert("RGB")
    draw2 = ImageDraw.Draw(page2)
    
    current_y = qr_y + qr_size + 105
    
    # "NAME : Student Name"
    draw2.text(
        (center_x, current_y),
        f"Name : {student_name.title()}",
        font=font_title,
        fill=INK_BROWN,
        anchor="mm"
    )
    current_y += 105
    
    # "INDEX No : AS2022605"
    draw2.text(
        (center_x, current_y),
        f"Index No : {index_number}",
        font=font_title,
        fill=INK_BROWN,
        anchor="mm"
    )
    
    # =========================================================================
    # SAVE AS PDF
    # =========================================================================
    
    pdf_buffer = io.BytesIO()
    
    # Save both pages as a PDF
    page1.save(
        pdf_buffer,
        format="PDF",
        save_all=True,
        append_images=[page2],
        resolution=150.0
    )
    
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()


# =============================================================================
# EMAIL HTML TEMPLATE - LORD OF THE RINGS THEME
# =============================================================================

def create_email_html(student_name: str, index_number: str) -> str:
    """
    Create the HTML content for the invitation email.
    
    This generates a Lord of the Rings themed HTML email with:
    - Dark mode aesthetic with gold and parchment accents
    - Ancient, adventurous language and phrasing
    - Fantasy-style typography
    - Clear instructions about the PDF attachment
    
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
        <title>Your Scroll Awaits - L'amitié 2k25</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');
        </style>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Crimson Text', Georgia, serif; background-color: #1a1614;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width: 650px; margin: 0 auto; background-color: #1a1614;">
            
            <!-- Decorative Top Border -->
            <tr>
                <td style="background: linear-gradient(90deg, #1a1614 0%, {GOLD_ACCENT} 50%, #1a1614 100%); height: 4px;"></td>
            </tr>
            
            <!-- Header Banner -->
            <tr>
                <td style="background: radial-gradient(ellipse at center, #2a2318 0%, #1a1614 70%); padding: 50px 30px; text-align: center; border-bottom: 1px solid #3a3228;">
                    <p style="color: {GOLD_ACCENT}; margin: 0 0 10px 0; font-size: 14px; letter-spacing: 8px; text-transform: uppercase; font-family: 'Cinzel', serif;">
                        ❧ The Fellowship Beckons ❧
                    </p>
                    <h1 style="color: {GOLD_ACCENT}; margin: 0; font-size: 42px; font-weight: 700; font-family: 'Cinzel', serif; letter-spacing: 4px; text-shadow: 0 0 20px rgba(197, 160, 89, 0.3);">
                        L'AMITIÉ 2K25
                    </h1>
                    <p style="color: #a89880; margin: 15px 0 0 0; font-size: 16px; font-style: italic;">
                        "Speak Friend, and Enter"
                    </p>
                </td>
            </tr>
            
            <!-- Main Content -->
            <tr>
                <td style="padding: 45px 35px; background-color: #1a1614;">
                    
                    <!-- Greeting -->
                    <h2 style="color: #E0D8C3; margin: 0 0 25px 0; font-size: 26px; font-family: 'Cinzel', serif; font-weight: 400;">
                        Greetings, Noble Traveler
                    </h2>
                    
                    <p style="color: #E0D8C3; font-size: 17px; line-height: 1.8; margin: 0 0 25px 0;">
                        The sacred records have bear your name, <strong style="color: {GOLD_ACCENT};">{student_name}</strong>. 
                        Your pass of entry through the gates of our realm has been granted.
                    </p>
                    
                    <p style="color: #E0D8C3; font-size: 17px; line-height: 1.8; margin: 0 0 30px 0;">
                        Behold! Attached to this raven's message lies your <em>Pass of Entry</em>; 
                        a sacred document bearing your unique seal. Guard it well, for it shall grant you 
                        entry to the grand celebration that awaits.
                    </p>
                    
                    <!-- Scroll/PDF Notice Box -->
                    <div style="background: rgba(255, 255, 255, 0.05); border: 3px double {GOLD_ACCENT}; border-radius: 8px; padding: 30px; margin: 35px 0; text-align: center;">
                        <p style="color: {GOLD_ACCENT}; margin: 0 0 10px 0; font-size: 13px; letter-spacing: 3px; text-transform: uppercase; font-family: 'Cinzel', serif;">
                            Your Sacred Pass
                        </p>
                        <h3 style="color: #E0D8C3; margin: 0 0 15px 0; font-size: 22px; font-family: 'Cinzel', serif;">
                            📜 Lamitie_2k25_Entry_Pass.pdf
                        </h3>
                        <p style="color: #B8A990; font-size: 15px; margin: 0 0 20px 0; line-height: 1.6;">
                            Open the attached document to reveal two pages:<br>
                            <span style="color: #E0D8C3;">Page One</span> — The cover of your invitation<br>
                            <span style="color: #E0D8C3;">Page Two</span> — Your QR seal and identity markings
                        </p>
                        <p style="color: #a89880; font-size: 13px; margin: 0; font-style: italic;">
                            Index Marking: <strong style="color: {GOLD_ACCENT};">{index_number}</strong>
                        </p>
                    </div>
                    
                    <!-- Instructions -->
                    <div style="margin: 35px 0;">
                        <h3 style="color: {GOLD_ACCENT}; margin: 0 0 20px 0; font-size: 18px; font-family: 'Cinzel', serif; letter-spacing: 2px;">
                            ❧ Instructions for the Journey
                        </h3>
                        <ul style="color: #E0D8C3; font-size: 16px; line-height: 2; padding-left: 25px; margin: 0; list-style-type: none;">
                            <li>❧ Download and safeguard the attached PDF document</li>
                            <li>❧ Present the <strong>QR seal (Page 2)</strong> at the realm's gates</li>
                            <li>❧ Arrive ere the sun reaches its appointed hour</li>
                            <li>❧ The document may be presented on parchment or glowing device</li>
                        </ul>
                    </div>
                    
                    <!-- Event Details Box -->
                    <div style="background: transparent; border-top: 2px solid {GOLD_ACCENT}; border-bottom: 2px solid {GOLD_ACCENT}; padding: 30px 20px; margin: 35px 0;">
                        <h3 style="color: {GOLD_ACCENT}; margin: 0 0 20px 0; font-size: 18px; font-family: 'Cinzel', serif; text-align: center; letter-spacing: 2px;">
                            🏰 The Grand Assembly
                        </h3>
                        <table role="presentation" width="100%" cellspacing="0" cellpadding="8">
                            <tr>
                                <td style="color: #B8A990; font-size: 15px; width: 35%;">When:</td>
                                <td style="color: #E0D8C3; font-size: 15px; font-weight: 600;">{EVENT_DATE}</td>
                            </tr>
                            <tr>
                                <td style="color: #B8A990; font-size: 15px;">Hour:</td>
                                <td style="color: #E0D8C3; font-size: 15px; font-weight: 600;">{EVENT_TIME}</td>
                            </tr>
                            <tr>
                                <td style="color: #B8A990; font-size: 15px;">Realm:</td>
                                <td style="color: #E0D8C3; font-size: 15px; font-weight: 600;">{EVENT_VENUE} - {EVENT_VENUE_SUB}</td>
                            </tr>
                        </table>
                    </div>
                    
                    <!-- Closing -->
                    <p style="color: #E0D8C3; font-size: 17px; line-height: 1.8; margin: 30px 0 25px 0;">
                        The fellowship awaits your presence. Tales shall be told, songs shall be sung, 
                        and memories forged in the fires of camaraderie. Until we meet at the gates...
                    </p>
                    
                    <p style="color: #a89880; font-size: 16px; font-style: italic; margin: 0 0 10px 0;">
                        "Not all those who wander are lost."
                    </p>
                    
                    <p style="color: #E0D8C3; font-size: 16px; margin: 25px 0 0 0;">
                        May your path be ever lit,<br>
                        <strong style="color: {GOLD_ACCENT}; font-family: 'Cinzel', serif;">The Council of L'amitié</strong>
                    </p>
                </td>
            </tr>
            
            <!-- Footer -->
            <tr>
                <td style="background-color: #0d0a08; padding: 30px; text-align: center; border-top: 1px solid #3a3228;">
                    <p style="color: {GOLD_ACCENT}; font-size: 10px; margin: 0 0 8px 0; letter-spacing: 4px; font-family: 'Cinzel', serif; opacity: 0.6; text-transform: uppercase;">
                        A Night to Remember
                    </p>
                </td>
            </tr>
            
            <!-- Decorative Bottom Border -->
            <tr>
                <td style="background: linear-gradient(90deg, #1a1614 0%, {GOLD_ACCENT} 50%, #1a1614 100%); height: 4px;"></td>
            </tr>
        </table>
    </body>
    </html>
    """


# =============================================================================
# EMAIL SENDING
# =============================================================================

async def send_invitation_email(
    recipient_email: str,
    student_name: str,
    index_number: str
) -> bool:
    """
    Send a Lord of the Rings themed invitation email with a PDF ticket.
    
    This function:
    1. Generates a 2-page PDF ticket (cover + personalized page with QR)
    2. Creates an HTML email with LOTR theme
    3. Attaches the PDF to the email
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
        # Step 1: Generate the 2-page PDF ticket
        pdf_bytes = generate_ticket_pdf(student_name, index_number)
        
        # Create a temporary file for the PDF
        # fastapi-mail requires a file path for attachments
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, 
            suffix=f"_Lamitie_2k25_Entry_Pass.pdf"
        )
        temp_file_path = temp_file.name
        temp_file.write(pdf_bytes)
        temp_file.close()
        
        # Step 2: Create the HTML email content
        html_content = create_email_html(student_name, index_number)
        
        # Step 3: Get email configuration
        conf = get_mail_config()
        
        # Step 4: Create the email message with PDF attachment
        message = MessageSchema(
            subject="📜 Your Scroll of Passage Awaits - L'amitié 2k25",
            recipients=[recipient_email],
            body=html_content,
            subtype=MessageType.html,
            attachments=[
                {
                    "file": temp_file_path,
                    "headers": {
                        "Content-Disposition": 'attachment; filename="Lamitie_2k25_Entry_Pass.pdf"',
                    },
                    "mime_type": "application",
                    "mime_subtype": "pdf",
                }
            ],
        )
        
        # Step 5: Send the email
        fm = FastMail(conf)
        await fm.send_message(message)
        
        print(f"✅ Scroll dispatched successfully to {recipient_email}")
        return True
        
    except Exception as e:
        # Log the error but don't crash the app
        print(f"❌ Failed to dispatch scroll to {recipient_email}: {str(e)}")
        return False
    
    finally:
        # Clean up: Delete the temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception:
                pass


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

async def send_test_email(recipient_email: str) -> bool:
    """
    Send a test invitation email for debugging purposes.
    
    Args:
        recipient_email: Email address to send the test to
        
    Returns:
        bool: True if successful
    """
    return await send_invitation_email(
        recipient_email=recipient_email,
        student_name="Frodo Baggins",
        index_number="SHIRE001"
    )
