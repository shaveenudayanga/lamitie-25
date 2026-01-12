def generate_qr_code(data: str) -> bytes:
    import qrcode
    from io import BytesIO

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def send_email(to_email: str, subject: str, body: str) -> None:
    from fastapi_mail import FastMail, MessageSchema
    from fastapi_mail import ConnectionConfig
    from pydantic import BaseModel

    class EmailConfig(BaseModel):
        MAIL_USERNAME: str
        MAIL_PASSWORD: str
        MAIL_FROM: str
        MAIL_PORT: int
        MAIL_SERVER: str
        MAIL_TLS: bool
        MAIL_SSL: bool

    conf = ConnectionConfig(
        MAIL_USERNAME="your_email@example.com",
        MAIL_PASSWORD="your_password",
        MAIL_FROM="your_email@example.com",
        MAIL_PORT=587,
        MAIL_SERVER="smtp.example.com",
        MAIL_TLS=True,
        MAIL_SSL=False,
    )

    message = MessageSchema(
        subject=subject,
        recipients=[to_email],
        body=body,
        subtype="html"
    )

    fm = FastMail(conf)
    fm.send_message(message)