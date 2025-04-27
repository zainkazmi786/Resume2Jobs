from groq import Groq
import os

client = Groq(
    api_key="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",
)

chat_completion = client.chat.completions.create(

    messages=[
        {
            "role": "user",
            "content": "hello how are you",
        }
    ],

    model="qwen-2.5-32b",
    
    stream=False,
)

print(chat_completion.choices[0].message.content)