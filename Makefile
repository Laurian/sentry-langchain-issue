include localai.env
-include .env.local
export

# Define the URLs of the files to be downloaded
HERMES2PRO_MISTRAL7B_URL := https://huggingface.co/NousResearch/Hermes-2-Pro-Mistral-7B-GGUF/resolve/main/Hermes-2-Pro-Mistral-7B.Q6_K.gguf

# Define the target paths where the files will be saved
HERMES2PRO_MISTRAL7B := models/Hermes-2-Pro-Mistral-7B.Q6_K.gguf

# Default target
all: $(HERMES2PRO_MISTRAL7B)

# Target for creating the models/ directory
models/:
	@mkdir -p models

# Target for downloading the HERMES2PRO_MISTRAL7B file
$(HERMES2PRO_MISTRAL7B): models/
	@echo "Checking and downloading model2 if missing..."
	@if [ ! -f $(HERMES2PRO_MISTRAL7B) ]; then \
		wget -O $(HERMES2PRO_MISTRAL7B) $(HERMES2PRO_MISTRAL7B_URL); \
	else \
		echo "HERMES2PRO_MISTRAL7B already exists."; \
	fi

venv:
	@if [ ! -d .venv ]; then \
		python3.12 -m venv .venv; \
	fi
	bash -c "source .venv/bin/activate && pip install --upgrade pip"

localai: $(HERMES2PRO_MISTRAL7B)
	@echo "Local AI models are ready."
	docker run \
		--env-file $(shell pwd)/localai.env \
		-p 8080:8080 \
		-v $(shell pwd)/models:/models \
		-v $(shell pwd)/images:/images \
		-v $(shell pwd)/huggingface:/huggingface \
		-ti \
		--rm quay.io/go-skynet/local-ai:v2.9.0 \
		--debug

printenv:
	printenv

# Phony targets to avoid conflicts with files of the same name
.PHONY: all models/ venv localai printenv
