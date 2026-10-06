import streamlit as st
import spacy
from ultralytics import YOLO
import numpy as np
from PIL import Image, ImageDraw

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Scanner com Yolo",
    layout="centered"
)

# Título principal da interface
st.title("Scanner com Yolo")

# Otimização do carregamento dos modelos com cache do Streamlit
@st.cache_resource
def load_models():
    # Carrega o modelo YOLO v8 pequeno pré-treinado
    yolo_model = YOLO("yolov8n.pt")
    
    # Carrega o modelo de processamento de linguagem natural do spaCy
    try:
        nlp_model = spacy.load("pt_core_news_sm")
    except OSError:
        # Fallback para modelo em inglês caso o em português não esteja disponível
        nlp_model = spacy.load("en_core_web_sm")
        
    return yolo_model, nlp_model

# Carregamento dos modelos
yolo, nlp = load_models()

# Campo de entrada de texto para o usuário solicitar objetos/conceitos
user_input = st.text_input(
    "O que você gostaria de ver?",
    placeholder="Ex: pessoa, carro, cachorro..."
)

# Processamento da entrada do usuário e visualização
if user_input:
    # Processa o texto fornecido pelo usuário usando spaCy para extração de lemas/substantivos
    doc = nlp(user_input.lower())
    target_terms = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    
    st.info(f"Termos identificados para busca: {', '.join(target_terms) if target_terms else user_input}")

    # Criação/Geração automatizada de uma imagem canvas interativa para inferência
    canvas_width, canvas_height = 600, 400
    generated_image = Image.new("RGB", (canvas_width, canvas_height), color=(240, 240, 240))
    draw = ImageDraw.Draw(generated_image)
    
    #