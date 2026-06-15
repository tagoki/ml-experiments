# 📝 Fine-Tuning Hugging Face Model on Custom Dataset

Привет! 👋  
Этот репозиторий предназначен для **fine-tuning модели Hugging Face** на кастомном датасете новостных заголовков с их темами. Основная цель — обучить модель **классифицировать заголовки по категориям** на основе данных с Lenta.ru. 📰

---

## 📂 Структура репозитория

- **data/**  
  📑 Датасет с заголовками новостей и их темами, собранными с Lenta.ru.  

- **logging_config/**  
  🛠️ Конфигурации для логирования, чтобы удобно отслеживать обучение и предсказания.  

- **model/**  
  🤖 Готовая модель Hugging Face и ноутбук для fine-tuning.  

- **parsing/**  
  🔍 Скрипт для парсинга новостей и подготовки данных к обучению.  

---

## 🌐 Веб-версия проекта

Есть отдельная ветка с реализацией **веб-версии** проекта на **FastAPI + Streamlit**:  
[Перейти к ветке веб-версии](https://github.com/tagoki/transformer-news-finetune/tree/web_version) 🌟  

---

## 🤖 Модель и токенизатор

### Модель: `BertForSequenceClassification`

- Базируется на **`DeepPavlov/rubert-base-cased`**  
- Предназначена для **классификации текстов** (заголовков новостей)  
- Количество классов: **3 категории**  
- Используется с Hugging Face `Trainer` для fine-tuning  

Пример инициализации модели:  

```python
from transformers import BertForSequenceClassification

model = BertForSequenceClassification.from_pretrained(
    "DeepPavlov/rubert-base-cased",
    num_labels=3  # количество классов
)
```
### Токенизатор: `BertTokenizerFast`

- Основан на той же модели **`DeepPavlov/rubert-base-cased`**
- Преобразует **текстовые заголовки в числовые тензоры**, которые понимает модель
- Поддерживает fast-токенизацию с паддингом и маскингом

Пример использования токенизатора:
```python
from transformers import BertTokenizerFast

tokenizer = BertTokenizerFast.from_pretrained("DeepPavlov/rubert-base-cased")

inputs = tokenizer(
    "Пример заголовка новости",
    padding="max_length",
    truncation=True,
    return_tensors="pt"
)
```
💡 Результатом токенизации является словарь с тензорами input_ids, attention_mask и token_type_ids, готовый к подаче в модель.

## 📊 Метрики обучения
| Epoch | Training Loss | Validation Loss | Accuracy | Macro F1 |
| ----- | ------------- | --------------- | -------- | -------- |
| 1     | 0.0721        | 0.0681          | 0.9838   | 0.9851   |
| 2     | 0.1149        | 0.1396          | 0.9860   | 0.9871   |
| 3     | 0.0586        | 0.1384          | 0.9895   | 0.9903   |

## 💻 Использование
Для работы с проектом достаточно:
1) Открыть ноутбук, который находится в репозитории.
2) Заменить пути к данным и модели на свои.
3) Запустить ячейки — обучение и предсказание будут работать автоматически.

## 📝 Примечания
1) Датасет содержит заголовки новостей с Lenta.ru и их категории.
2) Модель можно дообучать на других новостных данных для улучшения качества.
3) Убедитесь, что пути к файлам корректны перед запуском ноутбука.

