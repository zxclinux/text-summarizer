import os
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

DEFAULT_LENGTH_PRESETS: Mapping[str, str] = MappingProxyType({
    "Very short (1-2 sentences)": "The summary must be 1-2 sentences long.",
    "Short (3-5 sentences)": "The summary must be 3-5 sentences long.",
    "Detailed (one paragraph)": "The summary must be one comprehensive paragraph covering all key points of the text.",
})


@dataclass(frozen=True)
class Settings:
    model: str = "gpt-4o-mini"
    temperature: float = 0.2
    max_input_chars: int = 30_000
    request_timeout: float = 60.0
    length_presets: Mapping[str, str] = field(default_factory=lambda: DEFAULT_LENGTH_PRESETS)
    default_length: str = "Short (3-5 sentences)"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            model=os.getenv("SUMMARIZER_MODEL", cls.model),
            temperature=float(os.getenv("SUMMARIZER_TEMPERATURE", cls.temperature)),
            max_input_chars=int(os.getenv("SUMMARIZER_MAX_INPUT_CHARS", cls.max_input_chars)),
            request_timeout=float(os.getenv("SUMMARIZER_REQUEST_TIMEOUT", cls.request_timeout)),
        )
