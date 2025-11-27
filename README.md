# 🚗 Contador de Vehículos por Carriles (OpenCV)

Este proyecto implementa un sistema sencillo de **detección y conteo de vehículos** en un vídeo de tráfico utilizando **Python**, **OpenCV** y técnicas de sustracción de fondo.

El script analiza un vídeo (`tráfico01.mp4`), identifica vehículos en movimiento y lleva un **conteo independiente por carril**, mostrando en pantalla tanto el vídeo procesado como la máscara de detección.

---

## 📌 Características

- Detección de movimiento con `BackgroundSubtractorMOG2`.
- Limpieza de ruido mediante operaciones morfológicas.
- Conteo de vehículos por carriles con líneas configurables.
- Identificación de vehículos mediante su centroide.
- Prevención de conteos duplicados usando distancias mínimas.
- Visualización en tiempo real del procesamiento.

---

## 📂 Requisitos

- Python 3.x  
- OpenCV  
- NumPy  

Instalación recomendada:

```bash
pip install opencv-python numpy
