import cv2
import numpy as np

cap = cv2.VideoCapture('tráfico01.mp4')

frame_width = 640
frame_height = 480

min_area = 800  
offset = 10    

fgbg = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50, detectShadows=True)  

# Configuración de carriles con colores personalizados
lanes = [
    {"name": "Carril 1", "lines": [
        {"position": 400, "start": 425, "end": 430},
        {"position": 420, "start": 350, "end": 500}
    ], "counter": 0, "centers": [], "color": (0, 0, 255)},   
    {"name": "Carril 2", "lines": [
        {"position": 450, "start": 100, "end": 300}
    ], "counter": 0, "centers": [], "color": (0, 255, 0)},   
    {"name": "Carril 3", "lines": [
        {"position": 350, "start": 460, "end": 600}
    ], "counter": 0, "centers": [], "color": (255, 0, 0)}   
]

# Función para verificar si un centro es nuevo
def is_new_car(center, centers, min_distance=30):
    for c, lifetime in centers:
        if np.linalg.norm(np.array(center) - np.array(c)) < min_distance: 
            return False
    return True

while True:
    ret, frame = cap.read()  
    if not ret:
        break
    frame = cv2.resize(frame, (frame_width, frame_height))  
    fgmask = fgbg.apply(frame)  

    _, fgmask = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    for lane in lanes:
        for line in lane["lines"]:
            cv2.line(frame, (line["start"], line["position"]),
                     (line["end"], line["position"]), lane["color"], 2)

    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < min_area:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        center_x = x + w // 2
        center_y = y + h // 2

        # Dibujar el rectángulo y centro
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)

        # Verificar cruce en cada carril
        for lane in lanes:
            for line in lane["lines"]:
                if (line["start"] <= center_x <= line["end"] and
                        (line["position"] - offset) <= center_y <= (line["position"] + offset)):
                    if is_new_car((center_x, center_y), lane["centers"]):
                        lane["counter"] += 1
                        lane["centers"].append(((center_x, center_y), 15))  
    for lane in lanes:
        lane["centers"] = [(c, life - 1) for c, life in lane["centers"] if life > 1]  

    for i, lane in enumerate(lanes):
        cv2.putText(frame, f'{lane["name"]}: {lane["counter"]}', (10, 50 + i * 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, lane["color"], 2)

    cv2.imshow("Frame", frame)
    cv2.imshow("Máscara", fgmask)

    if cv2.waitKey(30) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()

