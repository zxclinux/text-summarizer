import gradio as gr
import openai

from config import Settings
from summarizer import InvalidInputError, Summarizer

EXAMPLE_UK = (
    "Фотосинтез — це процес, під час якого рослини, водорості та деякі бактерії перетворюють "
    "енергію світла на хімічну енергію. У хлоропластах за участі хлорофілу вуглекислий газ і вода "
    "перетворюються на глюкозу та кисень. Глюкоза слугує джерелом енергії та будівельним матеріалом "
    "для рослини, а кисень виділяється в атмосферу. Саме завдяки фотосинтезу на Землі підтримується "
    "склад атмосфери, придатний для дихання більшості живих організмів. Крім того, фотосинтез є "
    "основою майже всіх харчових ланцюгів: травоїдні тварини споживають рослини, а хижаки — "
    "травоїдних. Швидкість фотосинтезу залежить від інтенсивності освітлення, концентрації "
    "вуглекислого газу та температури."
)

EXAMPLE_EN = (
    "Remote work has changed how companies operate. Many employees report better focus and "
    "a healthier work-life balance because they no longer spend hours commuting. Companies, in "
    "turn, can hire talent from anywhere and save on office space. However, remote work also "
    "brings challenges: spontaneous collaboration becomes harder, new hires may struggle to learn "
    "the company culture, and some people feel isolated. As a result, many organizations are "
    "adopting hybrid models, where teams meet in the office a few days a week for collaboration "
    "and work from home the rest of the time."
)

API_ERROR_MESSAGES: dict[type[openai.OpenAIError], str] = {
    openai.AuthenticationError: "Invalid API key.",
    openai.RateLimitError: "Rate limit exceeded or account quota exhausted. Please try again later.",
    openai.APIConnectionError: "Could not connect to OpenAI. Please check your internet connection.",
}


def build_demo(settings: Settings, summarizer: Summarizer) -> gr.Blocks:
    def summarize(api_key: str, text: str, length: str) -> str:
        try:
            return summarizer(text, length, api_key)
        except InvalidInputError as e:
            raise gr.Error(str(e)) from e
        except openai.OpenAIError as e:
            message = next(
                (msg for exc_type, msg in API_ERROR_MESSAGES.items() if isinstance(e, exc_type)),
                "OpenAI API error. Please try again.",
            )
            raise gr.Error(message) from e

    with gr.Blocks(title="Text Summarizer") as demo:
        gr.Markdown(
            "# 📝 Text Summarizer\n\n"
            "Paste a text, choose the length and click **Summarize**: the service returns "
            "only a concise summary, in the same language as the input text.\n\n"
            f"- **Model:** `{settings.model}` (OpenAI), one API call per request.\n"
            "- **API key:** used only for the current request and **never stored**.\n"
            f"- **Limit:** up to {settings.max_input_chars} characters of text."
        )

        api_key = gr.Textbox(label="OpenAI API key", type="password", placeholder="sk-...")
        with gr.Row():
            with gr.Column():
                text = gr.Textbox(
                    label="Input text",
                    lines=10,
                    placeholder="Paste the text to summarize here...",
                )
                length = gr.Radio(
                    choices=list(settings.length_presets),
                    value=settings.default_length,
                    label="Summary length",
                )
                submit = gr.Button("Summarize", variant="primary")
            with gr.Column():
                output = gr.Textbox(label="Summary", lines=10, interactive=False, buttons=["copy"])

        gr.Examples(
            examples=[
                [EXAMPLE_UK, next(iter(settings.length_presets))],
                [EXAMPLE_EN, settings.default_length],
            ],
            inputs=[text, length],
            label="Examples",
        )

        submit.click(summarize, inputs=[api_key, text, length], outputs=output)

    return demo


settings = Settings.from_env()
demo = build_demo(settings, Summarizer(settings))

if __name__ == "__main__":
    demo.launch()
