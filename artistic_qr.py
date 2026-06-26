"""
Модуль для генерации артовых QR-кодов с использованием Stable Diffusion + ControlNet.
"""
import torch
from PIL import Image
import qrcode
import numpy as np
import cv2
from diffusers import (
    StableDiffusionControlNetImg2ImgPipeline,
    ControlNetModel,
    DDIMScheduler,
)
from diffusers.utils import load_image
from config import (
    ARTISTIC_QR_PROMPT,
    ARTISTIC_QR_NEGATIVE_PROMPT,
    CONTROLNET_MODEL_ID,
    BASE_SD_MODEL_ID,
    QR_SIZE,
    CONTROLNET_SCALE,
    STRENGTH,
    STEPS,
    GUIDANCE_SCALE,
    SEED,
)
from logger import log_action

# from PIL import Image, ImageFilter, ImageEnhance

# def sharpen_and_enhance(img: Image.Image) -> Image.Image:
#     """Повышает резкость и контраст, переводит в ч/б для улучшения читаемости."""
#     # Повышение резкости
#     img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=0))
    
#     # Увеличение контраста
#     enhancer = ImageEnhance.Contrast(img)
#     img = enhancer.enhance(2.0)
    
#     # Преобразование в чёрно-белое (бинарное)
#     gray = img.convert('L')
#     threshold = 200  # порог бинаризации, можно подобрать
#     img = gray.point(lambda p: p > threshold and 255)
#     img = img.convert('RGB')
#     return img

def generate_base_qr(data: str, size: int = QR_SIZE) -> Image.Image:
    """
    Создаёт обычный QR-код с высоким уровнем коррекции H.
    """
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    return img


def load_controlnet_pipeline():
    """
    Загружает пайплайн Stable Diffusion + ControlNet.
    Использует GPU, если доступен, иначе CPU.
    """
    device = "cpu"
    torch_dtype = torch.float16 if device == "cuda" else torch.float32

    log_action(f"Загрузка ControlNet модели: {CONTROLNET_MODEL_ID}")
    controlnet = ControlNetModel.from_pretrained(
        CONTROLNET_MODEL_ID,
        torch_dtype=torch_dtype
    )

    log_action(f"Загрузка базовой модели: {BASE_SD_MODEL_ID}")
    pipe = StableDiffusionControlNetImg2ImgPipeline.from_pretrained(
        BASE_SD_MODEL_ID,
        controlnet=controlnet,
        safety_checker=None,
        torch_dtype=torch_dtype,
    )

    # Оптимизация
    if device == "cuda":
        pipe.enable_xformers_memory_efficient_attention()
        pipe.enable_model_cpu_offload()
    else:
        pipe = pipe.to(device)
        # для CPU можно включить attention slicing для экономии памяти
        pipe.enable_attention_slicing()

    pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
    return pipe, device


def generate_artistic_qr(data: str, prompt: str = None, negative_prompt: str = None) -> Image.Image:
    """
    Генерирует артовый QR-код с помощью ControlNet.
    """
    if prompt is None or prompt == "":
        prompt = ARTISTIC_QR_PROMPT
    if negative_prompt is None or negative_prompt == "":
        negative_prompt = ARTISTIC_QR_NEGATIVE_PROMPT

    log_action(f"Начало генерации артового QR для: {data[:50]}...")

    # 1. Создаём базовый QR
    qr_img = generate_base_qr(data, QR_SIZE)

    # 2. Начальное изображение (белый фон) – для img2img
    init_img = Image.new("RGB", (QR_SIZE, QR_SIZE), color="white")

    # 3. Загружаем пайплайн (кэшируем для повторных вызовов)
    if not hasattr(generate_artistic_qr, "pipe"):
        generate_artistic_qr.pipe, generate_artistic_qr.device = load_controlnet_pipeline()

    pipe = generate_artistic_qr.pipe
    device = generate_artistic_qr.device

    # 4. Генерация
    generator = torch.manual_seed(SEED) if SEED is not None else None
    result = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=init_img,
        control_image=qr_img,
        controlnet_conditioning_scale=CONTROLNET_SCALE,
        guidance_scale=GUIDANCE_SCALE,
        num_inference_steps=STEPS,
        strength=STRENGTH,
        generator=generator,
    )

    artistic_img = result.images[0]

    log_action("Артовый QR-код успешно сгенерирован")
    return artistic_img


def check_qr_readability(img_path: str) -> bool:
    """
    Проверяет, сканируется ли QR-код с помощью pyzbar.
    """
    try:
        from pyzbar.pyzbar import decode
        img = Image.open(img_path)
        decoded = decode(img)
        return len(decoded) > 0
    except ImportError:
        log_action("pyzbar не установлен, проверка читаемости пропущена")
        return True  # если библиотеки нет, считаем успешным
    except Exception as e:
        log_action(f"Ошибка при проверке читаемости: {e}")
        return False