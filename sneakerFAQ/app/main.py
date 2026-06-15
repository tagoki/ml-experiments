import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # отключает логи

from sentence_transformers import SentenceTransformer
from app.log import print_log
from app.cfg import PATH_JSON, PATH_MODEL_PMML12V2, PATH_JSON_SNEAKERS

def load_model():
    try:
        model = SentenceTransformer(PATH_MODEL_PMML12V2)
    except OSError as e:
        print_log(level_log='warning', text='Не удалось загрузить локальную модель, пробую скачать из Hugging Face...')
        print_log(level_log='debug', text=f'{e}')
        model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        model.save('models/paraphrase-multilingual-MiniLM-L12-v2')
    return model

load_model()

def load_faq():
    with open(PATH_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    faq = {item["question"]: item["answer"] for item in data}
    return faq  # словарь: вопрос -> ответ

def load_faq_sneaker(product_name: str):
    path = os.path.join(PATH_JSON_SNEAKERS, f"{product_name}.json")

    if not os.path.exists(path):
        print_log(level_log='warning', text=f"FAQ для {product_name} не найден")
        return None

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    faq = {item["question"]: item["answer"] for item in data}
    return faq


def prepare_embeddings(path_model, faq_dict):
    model = SentenceTransformer(path_model)
    questions = list(faq_dict.keys())
    embeddings = model.encode(questions, convert_to_tensor=False)
    return embeddings, model


def answer_question(user_text, model, embeddings, faq_dict):
    query_emb = model.encode(user_text, convert_to_tensor=False)
    scores = cosine_similarity([query_emb], embeddings) 
    best_idx = np.argmax(scores)

    if scores[0][best_idx] < 0.7:
        return 'Я не уверен, что понял. Пожалуйста, переформулируйте вопрос'

    questions = list(faq_dict.keys())
    best_q = questions[best_idx]
    return faq_dict[best_q]

def run_pipeline(user_text, product_name=None):
    if product_name:
        faq_dict = load_faq_sneaker(product_name)
        if not faq_dict:
            return "FAQ для этого товара пока нет 😢"
    else:
        faq_dict = load_faq()

    embeddings, model = prepare_embeddings(PATH_MODEL_PMML12V2, faq_dict)
    result = answer_question(user_text, model, embeddings, faq_dict)
    return f'Ответ: {result}'