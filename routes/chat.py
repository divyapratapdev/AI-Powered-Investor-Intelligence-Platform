import os
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from llm.azure_openai import get_openai_client
from vectorstore.azure_ai_search import AzureAISearchVectorStore

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    company: str | None = None
    year: int | None = None


@router.post("/chat")
def chat(request: ChatRequest):
    try:
        store = AzureAISearchVectorStore(
            endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            api_key=os.getenv("AZURE_SEARCH_API_KEY"),
            index_name=os.getenv("AZURE_SEARCH_INDEX_NAME")
        )

        filter_expr = None
        if request.company and request.year:
            filter_expr = f"company eq '{request.company}' and year eq '{request.year}'"

        results = list(
            store.client.search(
                search_text=request.question,
                top=5,
                filter=filter_expr
            )
        )

        context = "\n\n".join([r.get("content", "") for r in results])

        client = get_openai_client()
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
            messages=[
                {"role": "system", "content": "You are an expert financial analyst. Answer based on the provided context."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {request.question}"}
            ]
        )

        return JSONResponse(content={"answer": response.choices[0].message.content})

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
