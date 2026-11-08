"""Genera una ilustración con Z-Image Turbo en ComfyUI (127.0.0.1:8000) y le quita el fondo con BiRefNet.

Uso: python comfy_gen.py "prompt" salida.png [seed] [ancho] [alto]
Guarda salida.png (RGBA, fondo transparente) y salida_raw.png (imagen original).
"""
import io
import json
import sys
import time
import urllib.parse
import urllib.request

from PIL import Image

URL = "http://127.0.0.1:8000"
prompt, salida = sys.argv[1], sys.argv[2]
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 7
w = int(sys.argv[4]) if len(sys.argv) > 4 else 1024
h = int(sys.argv[5]) if len(sys.argv) > 5 else 1024

wf = {
    "1": {"class_type": "UNETLoader", "inputs": {"unet_name": "z_image_turbo_bf16.safetensors", "weight_dtype": "default"}},
    "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "lumina2"}},
    "3": {"class_type": "VAELoader", "inputs": {"vae_name": "ae.safetensors"}},
    "4": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["1", 0], "shift": 3.0}},
    "5": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": prompt}},
    "6": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["5", 0]}},
    "7": {"class_type": "EmptySD3LatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
    "8": {"class_type": "KSampler", "inputs": {"model": ["4", 0], "seed": seed, "steps": 8, "cfg": 1.0,
                                               "sampler_name": "res_multistep", "scheduler": "simple",
                                               "positive": ["5", 0], "negative": ["6", 0],
                                               "latent_image": ["7", 0], "denoise": 1.0}},
    "9": {"class_type": "VAEDecode", "inputs": {"samples": ["8", 0], "vae": ["3", 0]}},
    "10": {"class_type": "SaveImage", "inputs": {"images": ["9", 0], "filename_prefix": "manim_raw"}},
    "11": {"class_type": "LoadBackgroundRemovalModel", "inputs": {"bg_removal_name": "birefnet.safetensors"}},
    "12": {"class_type": "RemoveBackground", "inputs": {"bg_removal_model": ["11", 0], "image": ["9", 0]}},
    "13": {"class_type": "MaskToImage", "inputs": {"mask": ["12", 0]}},
    "14": {"class_type": "SaveImage", "inputs": {"images": ["13", 0], "filename_prefix": "manim_mask"}},
}


def call(path, data=None):
    req = urllib.request.Request(URL + path, data=json.dumps(data).encode() if data else None,
                                 headers={"Content-Type": "application/json"})
    return urllib.request.urlopen(req, timeout=60).read()


pid = json.loads(call("/prompt", {"prompt": wf}))["prompt_id"]
t0 = time.time()
while True:
    hist = json.loads(call(f"/history/{pid}"))
    if pid in hist:
        break
    if time.time() - t0 > 600:
        sys.exit("timeout")
    time.sleep(2)
st = hist[pid].get("status", {})
if st.get("status_str") == "error":
    sys.exit(json.dumps(st, indent=1)[:2000])


def bajar(node):
    im = hist[pid]["outputs"][node]["images"][0]
    q = urllib.parse.urlencode({"filename": im["filename"], "subfolder": im["subfolder"], "type": im["type"]})
    return Image.open(io.BytesIO(call(f"/view?{q}")))


raw = bajar("10").convert("RGB")
mask = bajar("14").convert("L")
raw.save(salida.replace(".png", "_raw.png"))
rgba = raw.copy()
rgba.putalpha(mask)
rgba = rgba.crop(rgba.getbbox())  # recorta el margen transparente
rgba.save(salida)
print(f"OK en {time.time() - t0:.0f} s -> {salida} {rgba.size}")
