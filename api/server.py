import os
import typing as t
from typing import Any, Dict, List

import sentry_sdk
from sentry_sdk.integrations.starlette import StarletteIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.langchain import LangchainIntegration

from dotenv import dotenv_values
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

# from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel


# from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableLambda

from langfuse.decorators import langfuse_context, observe


JSONDict = Dict[str, Any]

config = {
    **dotenv_values(".env.production"),  # load sensitive variables
    **dotenv_values(
        ".env.local"
    ),  # load local/dev sensitive variables, do not deploy `.env.local`
    **os.environ,  # override loaded values
}

# override os.environ with the config values
# (some langchain modules read it from os.environ by default)
for key, value in config.items():
    os.environ[key] = value or ""

if "SENTRY_DSN" in os.environ:
    sentry_sdk.init(
        dsn=os.environ["SENTRY_DSN"],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
        send_default_pii=True,  # send personally-identifiable information like LLM responses to sentry
        integrations=[
            StarletteIntegration(
                transaction_style="url",
                failed_request_status_codes=[403, range(500, 599)],
            ),
            FastApiIntegration(
                transaction_style="url",
                failed_request_status_codes=[403, range(500, 599)],
            ),
            # LangchainIntegration(
            #     include_prompts=True,
            # ),
        ],
    )


class UnauthorizedMessage(BaseModel):
    detail: str = "Bearer token missing or unknown"


app = FastAPI(debug=config.get("FASTAPI_DEBUG", False) == "True")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
async def redirect_root_to_docs() -> RedirectResponse:
    return RedirectResponse("/docs")


# @observe()
def generate_draft_analysis(text: str, considerations: str) -> Any:

    model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo-0125")
    if model.startswith('"') and model.endswith('"'):
        model = model[1:-1]

    temperature = float(os.environ.get("OPENAI_TEMPERATURE", 0.7))

    print("Model and temp: ", model, temperature)

    # langfuse_context.update_current_trace(
    #     # name="custom-trace0",
    # )
    # langfuse_handler = langfuse_context.get_current_langchain_handler()

    llm = ChatOpenAI(model=model, temperature=temperature)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", considerations),
            (
                "human",
                "{text}",
            ),
        ]
    )

    chain = {"text": RunnablePassthrough()} | prompt | llm

    # with sentry_sdk.start_transaction(
    #     op="ai-inference", name="generate_draft_analysis"
    # ):
    #     result = chain.invoke(
    #         text,
    #         config={"callbacks": [langfuse_handler]},
    #     )

    result = chain.invoke(
        text,
        # config={"callbacks": [langfuse_handler]},
    )

    return {"id": result.id, "content": result.content}


class DraftAnalysisRequest(BaseModel):
    considerations: str
    text: str


@app.post(
    "/draft-analysis",
    response_model=JSONDict,
    responses={status.HTTP_401_UNAUTHORIZED: dict(model=UnauthorizedMessage)},
)
async def draft_analysis(
    request: DraftAnalysisRequest,
) -> JSONDict:
    text = request.text
    considerations = request.considerations

    result = generate_draft_analysis(text, considerations)

    return {
        "id": result["id"],
        "query": text,
        "considerations": considerations,
        "draft-analysis": result["content"],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8889)
