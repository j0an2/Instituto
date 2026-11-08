"""Edita una imagen con Qwen-Image-Edit-2511 (GGUF + Lightning 4 pasos) en ComfyUI (127.0.0.1:8000)
y le quita el fondo con BiRefNet. Sirve para cambiar pose/gesto de la mascota manteniendo su forma.

Uso: python editar_imagen.py base.png "instrucción" salida.png [seed]
Guarda salida.png (RGBA, fondo transparente) y salida_raw.png (imagen original).
"""
import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import uuid

from PIL import Image

URL = "http://127.0.0.1:8000"
base, prompt, salida = sys.argv[1], sys.argv[2], sys.argv[3]
seed = int(sys.argv[4]) if len(sys.argv) > 4 else 7


def call(path, data=None):
    req = urllib.request.Request(URL + path, data=json.dumps(data).encode() if data else None,
                                 headers={"Content-Type": "application/json"})
    try:
        return urllib.request.urlopen(req, timeout=60).read()
    except urllib.error.HTTPError as e:
        sys.exit(f"ComfyUI {e.code}: {e.read().decode(errors='replace')[:2000]}")


def subir(ruta):
    # Sube la imagen base a la carpeta input de ComfyUI (multipart a mano para no depender de requests)
    limite = uuid.uuid4().hex
    nombre = f"editar_{limite[:8]}.png"
    with open(ruta, "rb") as f:
        datos = f.read()
    cuerpo = (f"--{limite}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{nombre}\"\r\n"
              f"Content-Type: image/png\r\n\r\n").encode() + datos + f"\r\n--{limite}--\r\n".encode()
    req = urllib.request.Request(URL + "/upload/image", data=cuerpo,
                                 headers={"Content-Type": f"multipart/form-data; boundary={limite}"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())["name"]


wf = {
    "1": {"class_type": "UnetLoaderGGUF", "inputs": {"unet_name": "qwen-image-edit-2511-Q5_K_M.gguf"}},
    "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors", "type": "qwen_image"}},
    "3": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_vae.safetensors"}},
    "4": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0], "strength_model": 1.0,
                                                          "lora_name": "Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors"}},
    "5": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["4", 0], "shift": 3.0}},
    "6": {"class_type": "LoadImage", "inputs": {"image": subir(base)}},
    "7": {"class_type": "ImageScaleToTotalPixels", "inputs": {"image": ["6", 0], "upscale_method": "lanczos", "megapixels": 1.0,
                                                            "resolution_steps": 8}},
    "8": {"class_type": "TextEncodeQwenImageEditPlus", "inputs": {"clip": ["2", 0], "vae": ["3", 0], "image1": ["7", 0], "prompt": prompt}},
    "9": {"class_type": "TextEncodeQwenImageEditPlus", "inputs": {"clip": ["2", 0], "vae": ["3", 0], "image1": ["7", 0], "prompt": ""}},
    "10": {"class_type": "FluxKontextMultiReferenceLatentMethod", "inputs": {"conditioning": ["8", 0], "reference_latents_method": "index_timestep_zero"}},
    "11": {"class_type": "FluxKontextMultiReferenceLatentMethod", "inputs": {"conditioning": ["9", 0], "reference_latents_method": "index_timestep_zero"}},
    "12": {"class_type": "VAEEncode", "inputs": {"pixels": ["7", 0], "vae": ["3", 0]}},
    "13": {"class_type": "KSampler", "inputs": {"model": ["5", 0], "seed": seed, "steps": 4, "cfg": 1.0,
                                                "sampler_name": "euler", "scheduler": "simple",
                                                "positive": ["10", 0], "negative": ["11", 0],
                                                "latent_image": ["12", 0], "denoise": 1.0}},
    "14": {"class_type": "VAEDecode", "inputs": {"samples": ["13", 0], "vae": ["3", 0]}},
    "15": {"class_type": "SaveImage", "inputs": {"images": ["14", 0], "filename_prefix": "manim_edit_raw"}},
    "16": {"class_type": "LoadBackgroundRemovalModel", "inputs": {"bg_removal_name": "birefnet.safetensors"}},
    "17": {"class_type": "RemoveBackground", "inputs": {"bg_removal_model": ["16", 0], "image": ["14", 0]}},
    "18": {"class_type": "MaskToImage", "inputs": {"mask": ["17", 0]}},
    "19": {"class_type": "SaveImage", "inputs": {"images": ["18", 0], "filename_prefix": "manim_edit_mask"}},
}

pid = json.loads(call("/prompt", {"prompt": wf}))["prompt_id"]
t0 = time.time()
while True:
    hist = json.loads(call(f"/history/{pid}"))
    if pid in hist:
        break
    if time.time() - t0 > 900:
        sys.exit("timeout")
    time.sleep(2)
st = hist[pid].get("status", {})
if st.get("status_str") == "error":
    sys.exit(json.dumps(st, indent=1)[:2000])


def bajar(node):
    im = hist[pid]["outputs"][node]["images"][0]
    q = urllib.parse.urlencode({"filename": im["filename"], "subfolder": im["subfolder"], "type": im["type"]})
    return Image.open(io.BytesIO(call(f"/view?{q}")))


raw = bajar("15").convert("RGB")
mask = bajar("19").convert("L")
os.makedirs(os.path.dirname(os.path.abspath(salida)), exist_ok=True)
raw.save(salida.replace(".png", "_raw.png"))
rgba = raw.copy()
rgba.putalpha(mask)
rgba.save(salida)
print(f"{salida}  ({time.time() - t0:.0f}s)")
