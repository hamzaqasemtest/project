from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import messages_from_dict
from app.prompts.chatbot import chat_prompt


class Chatbot:

    def __init__(self, llm):
        self.llm = llm

        self.conversation = ConversationChain(
            prompt=PromptTemplate(
                input_variables=["history", "input"], template=chat_prompt
            ),
            llm=self.llm,
            memory=ConversationBufferMemory(),
            verbose=False,
        )

    async def chat(self, message: str):
        response = self.conversation.predict(input=message)
        return response

    def set_memory(self, database_entry):
        langchain_format = self.convert_entry_to_langchain(database_entry)
        retrieved_messages = messages_from_dict(langchain_format)
        retrieved_chat_history = ChatMessageHistory(messages=retrieved_messages)
        retrieved_memory = ConversationBufferMemory(chat_memory=retrieved_chat_history)
        self.conversation.memory = retrieved_memory

    def convert_entry_to_langchain(self, database_entry):
        print("Database Entry")
        print(database_entry)
        langchain_data = []
        for i in range(0, len(database_entry.session), 2):
            human_entry = {
                "type": "human",
                "data": {
                    "content": database_entry.session[i].text,
                    "additional_kwargs": {},
                    "response_metadata": {},
                    "type": "human",
                    "name": None,
                    "id": None,
                    "example": False
                }
            }

            ai_entry = {
                "type": "ai",
                "data": {
                    "content": database_entry.session[i].text,
                    "additional_kwargs": {},
                    "response_metadata": {},
                    "type": "ai",
                    "name": None,
                    "id": None,
                    "example": False,
                    "tool_calls": [],
                    "invalid_tool_calls": []
                }
            }
            langchain_data.append(human_entry)
            langchain_data.append(ai_entry)
        return langchain_data


