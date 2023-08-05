# import os

# import pytest
# from langchain import LLMChain
# from langchain import PromptTemplate
# from langchain.agents import initialize_agent
# from langchain.agents import load_tools
# from langchain.document_loaders import GitbookLoader
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.llms import OpenAI
# from langchain.llms.fake import FakeListLLM

# lib_path = os.path.dirname(os.path.abspath(__file__))
# sdk_path = os.path.dirname(lib_path)
# project_path = os.path.dirname(sdk_path)
# config_path = os.path.join(
#     os.path.dirname(os.path.dirname(os.path.dirname(project_path))),
#     "local-conf",
# )

# with open(f'{config_path}/open-api.key.txt', 'r') as f:
#     api_key = f.read()
# os.environ["OPENAI_API_KEY"] = api_key.strip()

# template = """
# I want you to act as a naming consultant for new companies.

# Here are some examples of good company names:

# - search engine, Google
# - social media, Facebook
# - video sharing, YouTube

# The name should be short, catchy and easy to remember.

# What is a good name for a company that makes {product}?
# """

# def test_prompt_template():
#     prompt = PromptTemplate(
#         input_variables=["product"],
#         template=template,
#     )
#     print(prompt.format(product="AI platform for AIGC"))

# def test_llm():
#     llm = OpenAI(model_name="text-ada-001", n=2, best_of=2)
#     print(llm("Tell me a joke about dog"))
#     assert llm("Tell me a joke about dog") != None

# def test_openai_llm():
#     template = """Question: {question}

#     Answer: Let's think step by step."""

#     prompt = PromptTemplate(template=template, input_variables=["question"])
#     llm = OpenAI()
#     llm_chain = LLMChain(prompt=prompt, llm=llm)
#     question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"
#     print(llm_chain.run(question))

# def test_fake_llm_agent():
#     tools = load_tools(["python_repl"])
#     responses = [
#         "Action: Python REPL\nAction Input: print(2 + 2)", "Final Answer: 4"
#     ]
#     llm = FakeListLLM(responses=responses)

#     agent = initialize_agent(
#         tools,
#         llm,
#         agent="zero-shot-react-description",
#         verbose=True,
#     )

#     print(agent.run("whats 2 + 2"))
#     llm.save(os.path.join(config_path, "llm.yaml"))

# def test_gitbook_loader():
#     loader = GitbookLoader("https://docs.gitbook.com")
#     page_data = loader.load()
#     print(page_data[:10])

# pytest.mark.skip(reason="TODO: fix test next PR")

# def test_embeddings():
#     embeddings = OpenAIEmbeddings()
#     text = "This is a test document."
#     query_result = embeddings.embed_query(text)
#     assert len(query_result) == 1536
#     doc_result = embeddings.embed_documents([text])
#     assert len(doc_result) == 1
#     embeddings = HuggingFaceEmbeddings()
#     query_result = embeddings.embed_query(text)
#     assert len(query_result) == 768
#     doc_result = embeddings.embed_documents([text])
#     assert len(doc_result) == 1

# def test_summarize():
#     from langchain import OpenAI
#     from langchain.chains import AnalyzeDocumentChain
#     from langchain.chains.summarize import load_summarize_chain
#     with open(os.path.join(lib_path, "state_of_the_union.txt")) as f:
#         state_of_the_union = f.read()
#     llm = OpenAI(temperature=0)
#     summary_chain = load_summarize_chain(llm, chain_type="map_reduce")
#     summarize_document_chain = AnalyzeDocumentChain(
#         combine_docs_chain=summary_chain)
#     print(summarize_document_chain.run(state_of_the_union))
