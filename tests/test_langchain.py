from types import SimpleNamespace
from uuid import uuid4
from obs_ai.integrations.langchain import (
    ObsAiCallbackHandler,
    ObsAICallbackHandler,
    AiObsCallbackHandler,
    FeenionCallbackHandler,
    instrument_langchain,
)
from obs_ai import configure, tracer

def test_langchain_callback_flow():
    handler = instrument_langchain(trace_name="test_langchain_agent")
    chain_run_id = uuid4()
    llm_run_id = uuid4()
    tool_run_id = uuid4()

    # 1. Chain start
    handler.on_chain_start(
        serialized={"name": "RetrievalQAChatAgent"},
        inputs={"question": "What is Obs_AI?"},
        run_id=chain_run_id,
    )

    # 2. Tool start & end
    handler.on_tool_start(
        serialized={"name": "search_docs"},
        input_str="Obs_AI overview",
        run_id=tool_run_id,
        parent_run_id=chain_run_id,
    )
    handler.on_tool_end(output="Obs_AI is an AI debugger.", run_id=tool_run_id)

    # 3. LLM start & end
    handler.on_llm_start(
        serialized={"name": "ChatOpenAI"},
        prompts=["User: What is Obs_AI?"],
        run_id=llm_run_id,
        parent_run_id=chain_run_id,
        metadata={"model_name": "gpt-4o"},
    )
    mock_llm_result = SimpleNamespace(
        generations=[[SimpleNamespace(text="Obs_AI provides real-time tracing.")]],
        llm_output={"token_usage": {"prompt_tokens": 20, "completion_tokens": 15, "total_tokens": 35}},
    )
    handler.on_llm_end(response=mock_llm_result, run_id=llm_run_id)

    # 4. Chain end
    handler.on_chain_end(
        outputs={"answer": "Obs_AI provides real-time tracing."},
        run_id=chain_run_id,
    )

    # Verify spans completed cleanly
    assert len(handler._runs) == 0

def test_langchain_error_handling():
    handler = ObsAiCallbackHandler(trace_name="test_error_chain")
    run_id = uuid4()
    handler.on_chain_start(serialized={"name": "FailingAgent"}, inputs={}, run_id=run_id)
    handler.on_chain_error(RuntimeError("API Gateway Connection Error"), run_id=run_id)
    assert len(handler._runs) == 0

def test_obs_ai_and_backward_compat_callback_handlers():
    h_obs = ObsAiCallbackHandler(trace_name="test_obs")
    assert isinstance(h_obs, ObsAiCallbackHandler)
    
    h_aiobs = AiObsCallbackHandler(trace_name="test_ai_obs")
    assert isinstance(h_aiobs, ObsAiCallbackHandler)
    
    h_feenion = FeenionCallbackHandler(trace_name="test_feenion")
    assert isinstance(h_feenion, ObsAiCallbackHandler)
