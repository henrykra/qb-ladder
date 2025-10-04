import abc
import time
import os
from google import genai

class LLMClient(abc.ABC):

    @abc.abstractmethod
    def chat(promt: str) -> str:
        ...

    @abc.abstractmethod
    def chat_streaming(prompt: str):
        ...


class TestClient(LLMClient):
    name = 'test'

    response = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, \
sed do eiusmod tempor incididunt ut labore et dolore magna \
aliqua. Ut enim ad minim veniam, quis nostrud exercitation \
ullamco laboris nisi ut aliquip ex ea commodo consequat. \
Duis aute irure dolor in reprehenderit in voluptate velit esse \
cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat \
cupidatat non proident, sunt in culpa qui officia deserunt \
mollit anim id est laborum."""

    def __init__(self):
        return super().__init__()


    def chat_streaming(self, prompt: str=None):

        yield prompt

        for word in self.response.split(' '):
            time.sleep(.05)
            yield word + ' '


    def chat(self, prompt: str=None):
        return self.response
    

class GeminiClient(LLMClient):
    name = 'gemini-2.5-flash-lite'

    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        print(api_key)
        self.client = genai.Client(api_key=api_key)


    def chat(self, prompt: str=None):
        resp = self.client.models.generate_content(
            model=self.name,
            contents=prompt,
        )
        return resp.text

    
    def chat_streaming(self, prompt: str=None):
        for chunk in self.client.models.generate_content_stream(
            model=self.name,
            contents=prompt,
        ):
            for letter in chunk.text:
                time.sleep(.01)
                yield letter
            # for word in chunk.text.strip().split(' '):
            #     time.sleep(.05)
            #     yield word + ' '
            