import asyncio
from typing import AsyncIterable
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain_openai import AzureChatOpenAI
from config import AZURE_CHATBOT_API_KEY, AZURE_CHATBOT_ENDPOINT, AZURE_CHATBOT_OPENAI_VERSION
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from app.prompts.chatbot_streaming import system_promt
from app.database.schemas.chat import Chat
from langchain_core.messages import messages_to_dict


class Chatbot:

    def __init__(self, chat: Chat):

        self.callback_handler = AsyncIteratorCallbackHandler()

        self.llm = AzureChatOpenAI(
            api_key=AZURE_CHATBOT_API_KEY,
            azure_endpoint=AZURE_CHATBOT_ENDPOINT,
            openai_api_version=AZURE_CHATBOT_OPENAI_VERSION,
            streaming=True,
            callbacks=[self.callback_handler]
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    system_promt,
                ),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ]
        )

        self.runnable = self.prompt | self.llm

        # self.store = chat.memory
        self.store = {}

        # self.chat_session_id = chat.id
        self.chat_session_id = "HAMZA"

        self.with_message_history = RunnableWithMessageHistory(
            self.runnable,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
            print(self.store)
        return self.store[session_id]

    async def chat_streaming(self, content: str) -> AsyncIterable[str]:

        task = asyncio.create_task(
            self.with_message_history.ainvoke(
                {"input": content},
                config={"configurable": {"session_id": self.chat_session_id}},
            )
        )

        try:
            async for token in self.callback_handler.aiter():
                print(token)
                yield f"data: {token}\n\n"
        except Exception as e:
            print(f"Exception occurred: {e}")
        finally:
            self.callback_handler.done.set()
        await task
