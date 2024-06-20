# Setup

## Install deps

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run in a different terminal the LocalAi LLM (localhost:8080)

Note: this will download a 6GB model in `/models` also the docker image for LocalAi is pretty big too.

```bash
make localai
```

## Run the server with and without Sentry

Without `SENTRY_DSN` (commented out in `.env.local`) start the server

```bash
source .venv/bin/activate
python ./api/server.py
```

Then in another console run:

```bash
curl -X 'POST' \
  'http://localhost:8889/draft-analysis' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "considerations": "You are an assistant.",
  "text": "Hello."
}'
```

The answer might take 3-5m depending on your local machine CPU:

```bash
{
  "id": "run-3de97013-9cb2-49d9-abe6-00a846f338d4-0",
  "query": "Hello.",
  "considerations": "You are an assistant.",
  "draft-analysis": "How can I help you today?...."
}

```

Enable `SENTRY_DSN` (in `.env.local`) and run the server again:

```bash
source .venv/bin/activate
python ./api/server.py
```

Then in another console run:

```bash
curl -X 'POST' \
  'http://localhost:8889/draft-analysis' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "considerations": "You are an assistant.",
  "text": "Hello."
}'
```

The answer might take 3-5m depending on your local machine CPU:

```bash
Internal Server Error
```

In server terminal:

```bash
Model and temp:  hermes-2-pro-mistral 0.7
INFO:     127.0.0.1:57209 - "POST /draft-analysis HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File ".venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 408, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 84, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".venv/lib/python3.12/site-packages/fastapi/applications.py", line 1054, in __call__
    await super().__call__(scope, receive, send)
  File ".venv/lib/python3.12/site-packages/sentry_sdk/integrations/starlette.py", line 362, in _sentry_patched_asgi_app
    return await middleware(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".venv/lib/python3.12/site-packages/sentry_sdk/integrations/asgi.py", line 144, in _run_asgi3
    return await self._run_app(scope, receive, send, asgi_version=3)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".venv/lib/python3.12/site-packages/sentry_sdk/integrations/asgi.py", line 235, in _run_app
    raise exc from None
  File ".venv/lib/python3.12/site-packages/sentry_sdk/integrations/asgi.py", line 230, in _run_app
    return await self.app(
           ^^^^^^^^^^^^^^^
  File ".venv/lib/python3.12/site-packages/starlette/applications.py", line 123, in __call__
    await self.middleware_stack(scope, receive, send)
  File ".venv/lib/python3.12/site-packages/sentry_sdk/integrations/starlette.py", line 158, in _create_span_call
    return await old_call(app, scope, new_receive, new_send, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in __call__
    raise exc
  File ".venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File ".venv/lib/python3.12/site-packages/sentry_sdk/integrations/starlette.py", line 158, in _create_span_call
    return await old_call(app, scope, new_receive, new_send, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".venv/lib/python3.12/site-packages/starlette/middleware/cors.py", line 85, in __call__
    await self.app(scope, receive, send)
  File ".venv/lib/python3.12/site-packages/sentry_sdk/integrations/starlette.py", line 257, in _sentry_exceptionmiddleware_call
    await old_call(self, scope, receive, send)
  File ".venv/lib/python3.12/site-packages/sentry_sdk/integrations/starlette.py", line 158, in _create_span_call
    return await old_call(app, scope, new_receive, new_send, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File ".venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
    raise exc
  File ".venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    await app(scope, receive, sender)
  File ".venv/lib/python3.12/site-packages/starlette/routing.py", line 756, in __call__
    await self.middleware_stack(scope, receive, send)
  File ".venv/lib/python3.12/site-packages/starlette/routing.py", line 776, in app
    await route.handle(scope, receive, send)
  File ".venv/lib/python3.12/site-packages/starlette/routing.py", line 297, in handle
    await self.app(scope, receive, send)
  File ".venv/lib/python3.12/site-packages/starlette/routing.py", line 77, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File ".venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
    raise exc
  File ".venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    await app(scope, receive, sender)
  File ".venv/lib/python3.12/site-packages/starlette/routing.py", line 72, in app
    response = await func(request)
               ^^^^^^^^^^^^^^^^^^^
  File ".venv/lib/python3.12/site-packages/sentry_sdk/integrations/fastapi.py", line 137, in _sentry_app
    return await old_app(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".venv/lib/python3.12/site-packages/fastapi/routing.py", line 278, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".venv/lib/python3.12/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "./api/server.py", line 152, in draft_analysis
    result = generate_draft_analysis(text, considerations)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "./api/server.py", line 128, in generate_draft_analysis
    result = chain.invoke(
             ^^^^^^^^^^^^^
  File ".venv/lib/python3.12/site-packages/langchain_core/runnables/base.py", line 2504, in invoke
    input = step.invoke(input, config)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".venv/lib/python3.12/site-packages/langchain_core/language_models/chat_models.py", line 170, in invoke
    self.generate_prompt(
  File ".venv/lib/python3.12/site-packages/langchain_core/language_models/chat_models.py", line 599, in generate_prompt
    return self.generate(prompt_messages, stop=stop, callbacks=callbacks, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".venv/lib/python3.12/site-packages/langchain_core/language_models/chat_models.py", line 456, in generate
    raise e
  File ".venv/lib/python3.12/site-packages/langchain_core/language_models/chat_models.py", line 446, in generate
    self._generate_with_cache(
  File ".venv/lib/python3.12/site-packages/langchain_core/language_models/chat_models.py", line 671, in _generate_with_cache
    result = self._generate(
             ^^^^^^^^^^^^^^^
  File ".venv/lib/python3.12/site-packages/langchain_openai/chat_models/base.py", line 538, in _generate
    return self._create_chat_result(response)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".venv/lib/python3.12/site-packages/langchain_openai/chat_models/base.py", line 556, in _create_chat_result
    response = response.model_dump()
               ^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'model_dump'
```
