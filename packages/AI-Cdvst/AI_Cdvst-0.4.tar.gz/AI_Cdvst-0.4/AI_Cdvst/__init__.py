###-------------------###
###----- AI_Cdvst ----###
###-------------------###
import os
import openai
import tkinter as tk
from tkinter import messagebox
import logging


###----------------------###
###-- OpenAICodeEditor --###
###----------------------###
class OpenAICodeEditor:
    """
    Diese Klasse ermöglicht es, Code oder Texte mit Hilfe von OpenAI-Modellen zu bearbeiten.
    """

    def __init__(self):
        """
        Initialisiert die Klasse OpenAICodeEditor und setzt die API-Schlüssel von OpenAI.
        Wenn kein gültiger Schlüssel gefunden wird, wird der Benutzer aufgefordert, einen API-Schlüssel einzugeben.

        Args:
            None

        Returns:
            None
        """
        self.logger = logging.getLogger(__name__)
        api_key = os.getenv("OPENAI_API_KEY")

        if api_key is None:
            api_key = self.get_api_key()

        openai.api_key = api_key

    def edit_code(self, input_text, instruction_text, return_json=False):
        """
        Bearbeitet den gegebenen Code-Text unter Verwendung des code-davinci-edit-001-Modells von OpenAI.

        Args:
            input_text (str): Der Code-Text, der bearbeitet werden soll.
            instruction_text (str): Die Bearbeitungsanweisungen, die für den Code-Text verwendet werden sollen.
            return_json (bool): Gibt an, ob das Ergebnis als JSON-Objekt oder nur als Text zurückgegeben werden soll.

        Returns:
            Das bearbeitete Ergebnis als Text oder JSON-Objekt der Klasse Edit von OpenAI, oder None, wenn ein Fehler auftritt.
        """
        try:
            result = openai.Edit.create(
                model="code-davinci-edit-001",
                input=input_text,
                instruction=instruction_text
            )
            if return_json:
                return result
            else:
                return result["choices"][0]["text"]
        except Exception as e:
            self.logger.error(f"Fehler beim Bearbeiten des Codes: {e}")
            return None

    def edit_text(self, input_text, instruction_text, return_json=False):
        """
        Bearbeitet den gegebenen Text unter Verwendung destext-davinci-edit-001-Modells von OpenAI.

        Args:
            input_text (str): Der Text, der bearbeitet werden soll.
            instruction_text (str): Die Bearbeitungsanweisungen, die für den Text verwendet werden sollen.
            return_json (bool): Gibt an, ob das Ergebnis als JSON-Objekt oder nur als Text zurückgegeben werden soll.

        Returns:
            Das bearbeitete Ergebnis als Text oder JSON-Objekt der Klasse Edit von OpenAI, oder None, wenn ein Fehler auftritt.
        """
        try:
            result = openai.Edit.create(
                model="text-davinci-edit-001",
                input=input_text,
                instruction=instruction_text
            )
            if return_json:
                return result
            else:
                return result["choices"][0]["text"]
        except Exception as e:
            self.logger.error(f"Fehler beim Bearbeiten des Texts: {e}")
            return None

    def get_api_key(self):
        """
        Fordert den Benutzer auf, einen gültigen OpenAI-API-Schlüssel einzugeben. Der Schlüssel wird überprüft und gespeichert,
        wenn er gültig ist.

        Args:
            None

        Returns:
            Der gültige API-Schlüssel als String.
        """
        root = tk.Tk()
        root.withdraw()
        api_key = tk.simpledialog.askstring(title="API-Schlüssel", prompt="Bitte geben Sie Ihren OpenAI-API-Schlüssel ein:")

        while not self.check_api_key(api_key):
            api_key = tk.simpledialog.askstring(title="API-Schlüssel", prompt="Ungültiger API-Schlüssel. Bitte geben Sie einen gültigen OpenAI-API-Schlüssel ein:")

        os.environ["OPENAI_API_KEY"] = api_key

        return api_key

    def check_api_key(self, api_key):
        """
        Überprüft, ob der gegebene API-Schlüssel gültig ist.

        Args:
            api_key (str): Der API-Schlüssel, der überprüft werden soll.

        Returns:
            True, wenn der Schlüssel gültig ist, andernfalls False.
        """
        openai.api_key = api_key

        try:
            openai.Usage.retrieve()
            return True
        except Exception as e:
            self.logger.error(f"Fehler beim Überprüfen des API-Schlüssels: {e}")

        return False


# AI_Cdvst.py

class DALLEImageGenerator:
    ENDPOINT = "https://api.openai.com/v1/images/generations"

    @classmethod
    def generate_image(cls, prompt):
        import requests
        from requests.structures import CaseInsensitiveDict
        import json
        import base64
        from io import BytesIO
        from PIL import Image
        from Data_Cdvst import ConfigManager

        api_key = ConfigManager.load_config()["api_key"]

        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = f"Bearer {api_key}"

        data = """
        {
            """
        data += f'"model": "image-alpha-001",'
        data += f'"prompt": "{prompt}",'
        data += """
            "num_images":1,
            "size":"1024x1024",
            "response_format":"url"
        }
        """

        resp = requests.post(cls.ENDPOINT, headers=headers, data=data)

        if resp.status_code != 200:
            raise ValueError("Failed to generate image")

        response_data = json.loads(resp.text)
        image_url = response_data['data'][0]['url']

        # Download and display the image
        image_data = requests.get(image_url).content
        img = Image.open(BytesIO(image_data))
        img.show()

        return image_data


###-------------------###
###------ Tests ------###
###-------------------###
import unittest
import os
import openai
import tkinter as tk
from tkinter import messagebox
import logging
class TestOpenAICodeEditor(unittest.TestCase):
    def setUp(self):
        self.editor = OpenAICodeEditor()

    def test_get_api_key(self):
        api_key = self.editor.get_api_key()
        self.assertTrue(self.editor.check_api_key(api_key))

    def test_edit_code(self):
        input_text = 'print("Hello World!")'
        instruction_text = 'Replace "World" with "Universe"'
        result = self.editor.edit_code(input_text, instruction_text)
        expected_result = 'print("Hello Universe!")'
        self.assertEqual(result, expected_result)

    def test_edit_text(self):
        input_text = 'This is a test.'
        instruction_text = 'Add "It worked!" to the end of the sentence.'
        result = self.editor.edit_text(input_text, instruction_text)
        expected_result = 'This is a test. It worked!'
        self.assertEqual(result, expected_result)

    def test_edit_code_return_json(self):
        input_text = 'print("Hello World!")'
        instruction_text = 'Replace "World" with "Universe"'
        result = self.editor.edit_code(input_text, instruction_text, return_json=True)
        self.assertTrue(isinstance(result, openai.edits.Edit))

    def test_edit_text_return_json(self):
        input_text = 'This is a test.'
        instruction_text = 'Add "It worked!" to the end of the sentence.'
        result = self.editor.edit_text(input_text, instruction_text, return_json=True)
        self.assertTrue(isinstance(result, openai.edits.Edit))

###-------------------###
###------ Main -------###
###-------------------###
if __name__ == '__main__':
    unittest.main()
