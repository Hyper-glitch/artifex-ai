import random


class Preprocessor:
    _corporate_colors = {
        "neon_blue": "#D2FCF9",
        "screen_blue": "#1407DB",
        "purple": "#8800FF",
        "pink": "#FF68FD",
        "orange": "#FF5500",
        "yellow": "#F7F821",
        "neon_green": "#14FF00",
        "olive": "#879A00",
        "tobacco green": "#553D00",
        "maroon": "#831514",
        "brown": "#57473E",
        "beige": "#DFDFB3",
        "dark_grey": "#4E4E4E",
        "grey": "#919191",
        "light_grey": "#D9D9D9",
        "black": "#000000",
        "white": "#FFFFFF",
    }
    _lora_tag = "<ecomtechstyle>"

    def preprocess(self, base_prompt: str) -> str:
        return self._build_colored_prompt(base_prompt)

    @classmethod
    def _build_colored_prompt(cls, base_prompt: str):
        """Build prompt with corporate colors."""
        selected_colors = cls._get_random_colors()
        color_description = ", ".join(
            f"{name.replace('_', ' ')} ({hex_code})" for name, hex_code in selected_colors.items()
        )
        colored_prompt = (
            f"{base_prompt}. Use only the following corporate colors: {color_description}."
        )

        return colored_prompt + f" in {cls._lora_tag}"

    @classmethod
    def _get_random_colors(cls, min_colors=2, max_colors=4) -> dict:
        num_colors = random.randint(min_colors, max_colors)
        selected = random.sample(list(cls._corporate_colors.items()), num_colors)
        return dict(selected)
