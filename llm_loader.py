
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain_community.llms import Replicate
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain_community.llms import Replicate

from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler, BaseCallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler
from langchain_community.llms import Replicate
from langchain_community import llms
class StreamingStdOutCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        super().__init__()

    def __call__(self, text):
        print(text, end='')
def load_llm():
    llm = Replicate(
    streaming=True,
    model="meta/meta-llama-3-8b-instruct",
    replicate_api_token="r8_ZCeBv5kVfDcoj2wCnbJ2tFLHIZb2FY20XJJT8",
    callbacks=[StreamingStdOutCallbackHandler()]
    )
    return llm
    