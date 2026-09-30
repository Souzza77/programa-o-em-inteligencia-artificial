import cv2
import numpy as np
import streamlit as st
from streamlit_webrtc import VideoProcessorBase, webrtc_streamer, WebRtcMode
from ultralytics import YOLO

# Configuração visual do Streamlit
st.set_page_config(
    page_title="Detecção em Tempo Real - Câmera PC",
    page_icon="📷",
    layout="wide"
)

@st.cache_resource
def load_model():
    """Carrega o modelo YOLOv8 Nano otimizado para inferência em CPU."""
    return YOLO("yolov8n.pt")

model = load_model()

# Classe de processamento de quadros de vídeo em tempo real
class RealTimeObjectDetector(VideoProcessorBase):
    def __init__(self):
        self.conf_threshold = 0.45

    def recv(self, frame):
        # Converte o frame do WebRTC para formato array OpenCV (BGR)
        img = frame.to_ndarray(format="bgr24")

        # Inferência do YOLO em CPU
        results = model.predict(
            source=img,
            conf=self.conf_threshold,
            device="cpu",
            verbose=False
        )

        # Desenha as detecções (boxes, labels e scores) no frame
        annotated_frame = results[0].plot()

        # Retorna o frame processado de volta para o navegador
        return frame.from_ndarray(annotated_frame, format="bgr24")


# Interface do Streamlit
st.title("📷 Identificação de Objetos em Tempo Real via Câmera")
st.markdown(
    "Teste sua webcam e identifique objetos no ambiente ao vivo utilizando **YOLOv8** e **Streamlit**."
)

# Controles na barra lateral
st.sidebar.header("Parâmetros do Detector")
conf_threshold = st.sidebar.slider(
    "Limiar de Confiança (Confidence Threshold)",
    min_value=0.1,
    max_value=1.0,
    value=0.45,
    step=0.05
)

# Streamer WebRTC para captura da webcam
ctx = webrtc_streamer(
    key="realtime-object-detection",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=RealTimeObjectDetector,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

# Atualização dinâmicas do parâmetro de confiança
if ctx.video_processor:
    ctx.video_processor.conf_threshold = conf_threshold