import math

# --- TRUCO DE COMPATIBILIDAD UNIVERSAL ---
# Esto crea un tipo de dato "Comodín" que ComfyUI acepta conectar en cualquier lado.
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

# Instancia del comodín
any_type = AnyType("*")

class NanoSmartRatio:
    """
    Nodo personalizado con salida UNIVERSAL para forzar la conexión
    con el nodo de Nano Banana Pro.
    """
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {"default": 1024, "min": 1, "max": 16384, "forceInput": True}),
                "height": ("INT", {"default": 1024, "min": 1, "max": 16384, "forceInput": True}),
            },
        }

    # CAMBIO IMPORTANTE: La primera salida ahora es 'any_type' (Comodín)
    # Esto engaña a ComfyUI para que permita la conexión con el COMBO.
    RETURN_TYPES = (any_type, "STRING")
    RETURN_NAMES = ("aspect_ratio", "debug_info")
    FUNCTION = "calculate_ratio"
    CATEGORY = "Nano Banana/Utils" 

    def calculate_ratio(self, width, height):
        if height == 0: height = 1
        current_ratio = width / height
        
        # Lista de estándares (Nano Banana / Gemini)
        standards = {
            1.00: "1:1",
            1.33: "4:3",
            1.25: "5:4",
            1.50: "3:2",
            1.77: "16:9",
            2.33: "21:9",
            0.75: "3:4",
            0.80: "4:5",
            0.66: "2:3",
            0.56: "9:16",
            0.42: "9:21"
        }

        closest_value = min(standards.keys(), key=lambda x: abs(x - current_ratio))
        final_string = standards[closest_value]
        
        info = f"Input: {width}x{height} -> {final_string}"

        return (final_string, info)

NODE_CLASS_MAPPINGS = {
    "NanoSmartRatio": NanoSmartRatio
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "NanoSmartRatio": "🍌 Nano Smart Ratio (Universal Fix)"
}