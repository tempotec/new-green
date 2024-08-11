import qrcode

# Criando o QR Code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# URL que o QR Code levará ao ser escaneado (exemplo)S
qr.add_data('http://localhost:5000/login')
qr.make(fit=True)

# Criando uma imagem para o QR Code
img = qr.make_image(fill='black', back_color='white')
img.show()
