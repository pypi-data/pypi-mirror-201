from secrets import token_hex
from io import BytesIO
import qrcode

class MeetClient:
    def __init__(self) -> None:
        self.base_url = "https://brie.fi/ng"

    def create_meet(self):
        unique_id = token_hex(4)
        return f"{self.base_url}/{unique_id[:3:]}-{unique_id[3:6]}-{unique_id[6:]}"

    def create_qr_code(self):
        meet_link = self.create_meet()
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(meet_link)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        with BytesIO() as buffer:
            img.save(buffer, format="png")
            return buffer.getvalue()