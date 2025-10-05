import abc
import time
import os
from google import genai

class LLMClient(abc.ABC):
    """Abstract base class for an LLM client."""
    @abc.abstractmethod
    def chat(promt: str) -> str:
        """Method for querying an llm. 
        Returns llm response once it has been completely processed.
        
        Arguments
        ---------
        prompt: str
            String prompt pased to LLM
        
        Returns
        -------
        str
            LLM response.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def chat_streaming(prompt: str):
        """Method for querying an llm streaming the response back.
        
        Arguments
        ---------
        prompt: str
            String prompt pased to LLM
        
        Returns
        -------
        str
            LLM response generator of strings.
        """
        raise NotImplementedError


class TestClient(LLMClient):
    """Client for testing text streaming."""
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
        """Streams back the prompt as passed to the client and a sample response."""
        yield prompt

        for word in self.response.split(' '):
            time.sleep(.05)
            yield word + ' '


    def chat(self, prompt: str=None):
        return self.response
    

class GeminiClient(LLMClient):
    name = 'gemini-2.5-flash-lite'

    def __init__(self):
        """Creates gemini client using the enviroment variable containg the api key."""
        api_key = os.getenv('GEMINI_API_KEY')
        self.client = genai.Client(api_key=api_key)


    def chat(self, prompt: str=None):
        """Return entire response from gemini client. """
        resp = self.client.models.generate_content(
            model=self.name,
            contents=prompt,
        )
        return resp.text

    
    def chat_streaming(self, prompt: str=None):
        """Generator streaming back LLM response word by word."""
        for chunk in self.client.models.generate_content_stream(
            model=self.name,
            contents=prompt,
        ):
            for letter in chunk.text:
                time.sleep(.01)
                yield letter
            