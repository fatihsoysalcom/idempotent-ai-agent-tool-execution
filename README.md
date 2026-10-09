# idempotent-ai-agent-tool-execution
This example demonstrates how AI agents can safely interact with external tools using idempotency. It simulates an external service that processes orders and an AI agent that retries failed calls. The idempotency key ensures that even with retries or accidental duplicate calls, the underlying side effect (order processing) occurs only once.
