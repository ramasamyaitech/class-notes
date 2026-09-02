# from langchain_core.prompts import ChatPromptTemplate

# from models import OllamaModel
# from services.retrieval_service import RetrievalService


# class RAGService:

#     def __init__(self):

#         self.model = OllamaModel()

#         self.llm = self.model.get_llm()

#         self.retriever = RetrievalService()

#         self.prompt = ChatPromptTemplate.from_template(
#             """
# You are a helpful AI assistant.

# Answer the user's question using ONLY the provided context.

# If the answer is not available in the context,
# say:

# "I don't have enough information in the provided documents."

# Do not make up information.

# Context:
# {context}

# Question:
# {question}

# Answer:
# """
#         )

#     def ask(self, question: str):

#         documents = self.retriever.retrieve(question)

#         context = "\n\n".join(
#             document.page_content
#             for document in documents
#         )

#         prompt = self.prompt.format(
#             context=context,
#             question=question
#         )

#         response = self.llm.invoke(prompt)

#         sources = [
#             {
#                 "page": doc.metadata.get("page"),
#                 "source": doc.metadata.get("source")
#             }
#             for doc in documents
#         ]

#         return {
#             "answer": response.content,
#             "sources": sources
#         }


# =============================================



from langchain_core.prompts import ChatPromptTemplate

from services.retrieval_service import RetrievalService
from services.llm_service import LLMService


class RAGService:

    def __init__(self):

        self.retriever = RetrievalService()
        self.llm_service = LLMService()

        self.prompt = ChatPromptTemplate.from_template(
            """
You are an enterprise RAG assistant.

Answer the question using ONLY the context below.

Do not make up information.

If the answer is not available in the context,
say:

"I don't have enough information in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""
        )

    def ask(self, question: str):

        results = self.retriever.retrieve(question)

        if not results:
            return {
                "answer": (
                    "I don't have enough information "
                    "in the provided documents."
                ),
                "sources": []
            }

        documents = []
        sources = []

        # Handle both:
        # 1. Document
        # 2. (Document, score)

        for item in results:

            if isinstance(item, tuple) and len(item) == 2:

                document, score = item

            else:

                document = item
                score = None

            documents.append(document)

            sources.append({
                "source": document.metadata.get("source"),
                "page": document.metadata.get("page"),
                "score": float(score) if score is not None else None
            })

        # Build context
        context = "\n\n".join(
            document.page_content
            for document in documents
        )

        # Create prompt
        prompt = self.prompt.format(
            context=context,
            question=question
        )

        # Generate answer
        answer = self.llm_service.generate(prompt)

        return {
            "answer": answer,
            "sources": sources
        }