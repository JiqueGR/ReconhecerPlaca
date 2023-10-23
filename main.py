import cv2
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\Tesseract.exe"
def trackbar_callback(value):
    return

imagem = cv2.imread("carro.jpg")

imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

cv2.namedWindow('Trackbar')
cv2.createTrackbar('Branco', 'Trackbar', 0, 255, trackbar_callback)
cv2.setTrackbarPos('Branco', 'Trackbar', 255)
cv2.createTrackbar('Preto', 'Trackbar', 0, 255, trackbar_callback)
cv2.setTrackbarPos('Preto', 'Trackbar', 180)

while True:
    limiarBranco = cv2.getTrackbarPos('Branco', 'Trackbar')
    limiarPreto = cv2.getTrackbarPos('Preto', 'Trackbar')

    ret, imagemBinaria = cv2.threshold(imagemCinza, limiarPreto, limiarBranco, cv2.THRESH_BINARY)

    cv2.imshow("Binarizacao", imagemBinaria)

    if cv2.waitKey(1) & 0xFF == 27:
        cv2.destroyAllWindows()
        break

contornos, hierarquia = cv2.findContours(imagemBinaria, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
maior_contorno = None
maior_area = 0

for contorno in contornos:
    perimetro = cv2.arcLength(contorno, True)
    if perimetro > 120:
        aprox = cv2.approxPolyDP(contorno, 0.03 * perimetro, True)
        if len(aprox) == 4:
            area = cv2.contourArea(contorno)
            if area > maior_area:
                maior_area = area
                maior_contorno = contorno

(x,y,altura,largura) = cv2.boundingRect(maior_contorno)
cv2.rectangle(imagem, (x,y), (x+altura,y+largura), (0,0,0), 2)

recorte = imagem[y:y+largura, x+15:x+altura-20]

imagem_redimensionada = cv2.resize(recorte, (altura * 5, largura * 5))

resultado = pytesseract.image_to_string(imagem_redimensionada, lang="eng")
print(resultado)
cv2.imshow("Pytesseract", imagem_redimensionada)
cv2.waitKey(0)
