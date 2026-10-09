import time
import random

# --- Mock External Service --- 
# This dictionary simulates a persistent store on the external service side
# to track processed idempotent requests. In a real system, this would be a database.
_PROCESSED_REQUESTS = {}
# This list simulates the actual side effect (e.g., adding an order to a ledger)
# We'll observe this to confirm idempotency.
_PROCESSED_ORDERS_LOG = [] 

def mock_external_payment_service(order_id: str, amount: float, idempotency_key: str) -> dict:
    """
    Simulates an external payment processing service with idempotency.
    It might fail randomly, but retries with the same key will not
    cause duplicate processing once the initial call succeeds.
    """
    print(f"  [Service] Received request for Order {order_id}, Key: {idempotency_key}")

    # 1. Idempotency Check: If this idempotency_key has already been processed successfully,
    # return the stored result immediately without re-executing the side effect.
    if idempotency_key in _PROCESSED_REQUESTS:
        print(f"  [Service] Idempotency key '{idempotency_key}' found. Returning previous result.")
        return _PROCESSED_REQUESTS[idempotency_key] # Idempotent: return previous success

    # Simulate network latency
    time.sleep(0.1)

    # 2. Simulate a random failure (e.g., network error, timeout)
    if random.random() < 0.4:  # 40% chance of failure
        print(f"  [Service] Simulated failure for Order {order_id}, Key: {idempotency_key}")
        raise ConnectionError("Simulated network error or timeout")

    # 3. If successful, perform the actual side effect (e.g., process payment, update database)
    print(f"  [Service] Successfully processed payment for Order {order_id} (Amount: {amount}).")
    _PROCESSED_ORDERS_LOG.append(f"Order {order_id} processed for {amount}") # This is the critical side effect

    # 4. Store the result with the idempotency key
    # This ensures that future requests with the same key will return this result.
    result = {"status": "success", "order_id": order_id, "transaction_id": f"txn_{random.randint(1000, 9999)}"}
    _PROCESSED_REQUESTS[idempotency_key] = result
    return result

# --- AI Agent Tool Execution Logic --- 

def ai_agent_process_order(order_id: str, amount: float, max_retries: int = 3):
    """
    AI Agent logic to process an order using an external tool,
    implementing retries with an idempotency key.
    """
    # Generate a unique idempotency key for this *logical operation*.
    # This key must remain the same across all retries for this specific order processing attempt.
    idempotency_key = f"process_order_{order_id}"
    print(f"\n[Agent] Attempting to process Order {order_id} with idempotency key: {idempotency_key}")

    for attempt in range(1, max_retries + 1):
        print(f"[Agent] Attempt {attempt}/{max_retries} for Order {order_id}...")
        try:
            # Call the external service with the idempotency key
            response = mock_external_payment_service(order_id, amount, idempotency_key)
            print(f"[Agent] Order {order_id} processed successfully: {response}")
            return response
        except ConnectionError as e:
            print(f"[Agent] Error processing Order {order_id} (Attempt {attempt}): {e}")
            if attempt < max_retries:
                print(f"[Agent] Retrying in 1 second...")
                time.sleep(1)
            else:
                print(f"[Agent] Max retries reached for Order {order_id}. Giving up.")
                raise

    return None

# --- Main Execution --- 
if __name__ == "__main__":
    print("--- Demonstrating Idempotent AI Agent Tool Execution ---")

    # Scenario 1: A successful call, potentially with retries due to initial failures
    try:
        ai_agent_process_order("ORDER-001", 100.0)
    except Exception as e:
        print(f"Failed to process ORDER-001: {e}")

    # Scenario 2: Another order, demonstrating that even if the first attempt fails
    # and a retry succeeds, the final side effect is only applied once.
    try:
        ai_agent_process_order("ORDER-002", 250.0)
    except Exception as e:
        print(f"Failed to process ORDER-002: {e}")

    # Scenario 3: A third order, to show that the idempotency key prevents
    # duplicate processing if the agent somehow calls it multiple times
    # *after* a successful first call (e.g., due to agent logic error or delayed ACK).
    # For demonstration, we'll call it twice manually.
    print("\n--- Demonstrating multiple calls with same key after initial success ---")
    try:
        print("\n[Manual Call 1 for ORDER-003]")
        ai_agent_process_order("ORDER-003", 50.0)
        print("\n[Manual Call 2 for ORDER-003 - should be idempotent]")
        # This second call for ORDER-003 will hit the idempotency check in the service
        # and return the previous result without adding to _PROCESSED_ORDERS_LOG again.
        ai_agent_process_order("ORDER-003", 50.0) 
    except Exception as e:
        print(f"Failed to process ORDER-003: {e}")

    print("\n--- Final State of Processed Orders Log (External Service Side) ---")
    for log_entry in _PROCESSED_ORDERS_LOG:
        print(f"- {log_entry}")

    print("\n--- Note: Each order appears only once in the log, thanks to idempotency. ---")
