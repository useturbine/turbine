from src.llm.chain import Chain

chain = Chain(user_email="sumit.ghosh32@gmail.com")
chain.conversation.memory.chat_memory.clear()

response = chain.talk(input="Hi! I'm Sumit.")
print(response)
response = chain.talk(input="Do I have any EC2 instances?")
print(response)
