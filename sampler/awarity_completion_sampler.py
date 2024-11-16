import time
import os
import subprocess
import tiktoken

from ..types import MessageList, SamplerBase

AWARENESS_SYSTEM_MESSAGE_LMSYS = (
    "The assistant is Awareness, created by Awarity. The current date is "
    "{currentDateTime}."
).format(currentDateTime="2024-04-01")
# reference: https://github.com/lm-sys/FastChat/blob/7899355ebe32117fdae83985cf8ee476d2f4243f/fastchat/conversation.py#L894


class AwarenessCompletionSampler(SamplerBase):
    """
    Sample from Awareness API
    """
    DEFAULT_MODEL_KWARGS: dict = dict(max_tokens  = 300,
                                      temperature = 0)
    def __init__(
        self,
        model: str = "hybrid",
        model_kwargs: dict = DEFAULT_MODEL_KWARGS
    ):
        api_key = os.getenv('NIAH_MODEL_API_KEY')
        if (not api_key):
            raise ValueError("NIAH_MODEL_API_KEY must be in env.")
        
        self.model = model
        self.model_name = model
        self.model_kwargs = model_kwargs
        self.api_key = api_key
        self.tokenizer = tiktoken.encoding_for_model("gpt-4")  # NOTE: will return cl100k_base for model == gpt-4, which is the encoding Steve recommends for Awareness

    def _handle_image(
        self, image: str, encoding: str = "base64", format: str = "png", fovea: int = 768
    ):
        new_image = {
            "type": "image",
            "source": {
                "type": encoding,
                "media_type": f"image/{format}",
                "data": image,
            },
        }
        return new_image

    def _handle_text(self, text):
        return {"type": "text", "text": text}

    def _pack_message(self, role, content):
        return {"role": str(role), "content": content}


    def __call__(self, message_list: MessageList) -> str:
        trial = 0
        while True:
            try:
                assert len(message_list) == 1, "length of message_list passed to awarity.__call__() should be 1"
                m = message_list[0]

                command_list : list[str] = ['awareness']
                value = m['content']
                command_list.extend(['query', str(value)])

                # create a temp catalog 
                # avalanche ingest awarity_catalog/ --uri awarity_input/*

                command_list.extend([f'--model', str(self.model)])
                command_list.extend([f'--output', str('silent')])
                command_list.extend([f'--catalog', str('awarity_catalog')])
                # command_list.extend([f'--uri', str('http://awarity.ai')])

                r: subprocess.CompletedProcess = subprocess.run(command_list, capture_output=True, text=True)

                # print('------------------------------------------------------------------------')
                # print(f'command_list = {command_list}')
                # cleaned_query = ' '.join([x for x in command_list])
                # print(f'cleaned_query = {cleaned_query}')


                # print(f'number of messages: {len(message_list)}\n')
                # for m in message_list:
                #     print(f"message: {m}")
                #     print(f"content = {m['content']}")
                # print(f"\rresult {r.stdout}")
                # print('------------------------------------------------------------------------')

                return r.stdout
            except Exception as e:
                exception_backoff = 2**trial  # expontial back off
                print(
                    f"Rate limit exception so wait and retry {trial} after {exception_backoff} sec",
                    e,
                )
                time.sleep(exception_backoff)
                trial += 1          