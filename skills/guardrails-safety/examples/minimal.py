"""Chapter 18 — Block tool calls when session user_id does not match args."""

def validate_tool_params(tool, args, tool_context):
    if args.get("user_id_param") != tool_context.state.get("session_user_id"):
        return {"status": "error", "error_message": "Tool call blocked: User ID mismatch."}
    return None  # allow
