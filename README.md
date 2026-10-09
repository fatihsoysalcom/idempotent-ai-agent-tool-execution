# Idempotent AI Agent Tool Execution

This example demonstrates how AI agents can safely interact with external tools using idempotency. It simulates an external service that processes orders and an AI agent that retries failed calls. The idempotency key ensures that even with retries or accidental duplicate calls, the underlying side effect (order processing) occurs only once.

## Language

`python`

## How to Run

Save the code as `main.py`. Run from your terminal: `python main.py`

## Original Article

This example accompanies the Turkish article: [AI Ajanları İçin Daha Güvenli Araç Yürütme: Tekrarlamadan Önce İdempotens](https://fatihsoysal.com/blog/ai-ajanlari-icin-daha-guvenli-arac-yurutme-tekrarlamadan-once-idempotens/).

## License

MIT — see [LICENSE](LICENSE).
