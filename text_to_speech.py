# -*- coding: utf-8 -*-
"""Text to Speech.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kR6gpb5m_eMufF1oYz715z61XqLv20XH
"""

pip install openai

from google.colab import files
uploaded = files.upload()

pip install pdfx

import pdfx

pdf=pdfx.PDFx('Article.pdf')
pdf_content=pdf.get_text()

pip install langchain

pip install tiktoken

from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter

model_name="gpt-3.5-turbo"

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(model_name=model_name)

text=text_splitter.split_text(pdf_content)
docs=[Document(page_content=t) for t in text]

pip install langchain-openai

from string import Template
from langchain_openai import ChatOpenAI
import os
from google.colab import userdata
OPENAI_API_KEY=userdata.get('openAI')
llm=ChatOpenAI(
    temperature=0,openai_api_key=OPENAI_API_KEY,model_name=model_name
)
from langchain.prompts import PromptTemplate
prompt_template=PromptTemplate(
    input_variables=['context'],
    template="summarize the following content:{content}"
)

prompt_template="""summarize the following content:{text}"""
prompt=PromptTemplate(template=prompt_template,input_variables=['text'])

from langchain.chains.combine_documents.stuff import StuffDocumentsChain

from langchain.chains import LLMChain

llm_chain = LLMChain(llm=llm, prompt=prompt)

chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

summary = chain.invoke(docs)
import textwrap
summary_text = summary.get('output_text','no summary available.')

print(textwrap.fill(summary_text,width=100))

!pip install gTTS

!pip install Ipython

from gtts import gTTS
from IPython.display import Audio

text = summary_text
tts = gTTS(text, lang='en')
tts.save("output.mp3")

Audio("output.mp3",autoplay=True)