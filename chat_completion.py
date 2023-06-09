import asyncio
import openai_async
import openai
from pprint import pprint
from promt_templates import system_chat_template
from configs import OPENAI_KEY

openai.api_key = OPENAI_KEY

messages = [
    {"role": "system", "content": system_chat_template}]


def chatbot(input):
    if input:
        if input == 'exit':
            exit()
        messages.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        # chat = await openai_async.chat_complete(OPENAI_KEY,
        #                                         timeout=0.05,
        #                                         payload={
        #                                              "model": "gpt-3.5-turbo",
        #                                              "messages": messages
        #                                          })
        # reply = chat.json()["choices"][0]["message"]
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply


if __name__ == "__main__":
    while True:
        query = input("Query: ")
        response = chatbot(query)
        pprint(response)
