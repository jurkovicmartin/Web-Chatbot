from ollama import chat
import re

class Model:
    def __init__(self):
        """Ollama chatting model.
        """
        self.model = "deepseek-r1:1.5b"
        print(f"Model: {self.model}")


    def get_response(self, prompt: str, short: bool =False) -> str:
        """Get response from model.

        Args:
            prompt (str): users prompt
            short (bool, optional): if True skips the models thinking part (reasoning). Defaults to False.

        Returns:
            str: models response
        """
        self.short = short

        self.response = chat(model=self.model, messages=[
        {
            "role": "user",
            "content": prompt,
        },
        ])

        return self._format_html()


    def _format_html(self) -> str:
        """Formats basic formatting of string to html string. 

        Returns:
            str: formatted string
        """
        text = self.response.message.content

        if self.short:
            # Removes the <think> </think> text
            text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

        text = text.replace("\n", "<br>")

        # Bold counter
        self.bold = 0
        text = re.sub(r"\*\*", self._replace_bold, text)
        # Title counter
        self.title = 0
        text = re.sub(r"\#\#\#", self._replace_title, text)

        return text
    

    def _replace_bold(self, match) -> str:
        """Replacing with <strong> tags.

        Returns:
            str: tag
        """
        self.bold += 1
        return "<strong>" if self.bold % 2 else "</strong>"
    

    def _replace_title(self, match):
        """Replacing with <h3> tags.

        Returns:
            str: tag
        """
        self.title += 1
        return "<h3>" if self.title % 2 else "</h3>"
