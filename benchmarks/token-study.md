# Token and cost experiment / Experimento de tokens y coste

## Hypothesis
Transport overhead is not model token usage. Identical model-facing schemas and messages should not be assumed to yield different token counts merely because the invocation protocol changes.

## Factorial design
MCP/full, MCP/selected, UTCP/full, UTCP/selected. Use the same model deployment/version, tasks, tool schemas, selection algorithm, sampling settings and output normalization. Randomize execution order, separate cold and warm cache runs, and record failures.

## Offline baseline
Install requirements-tokens.txt. Run token_context.py with a JSON object containing mcp and utcp arrays of normalized OpenAI-style function definitions, and --selected get_stock. The script rejects unequal catalogs and estimates serialized schema tokens. This is not provider billing or a live agent benchmark.

## Live experiment (pending)
Capture provider-reported input, cached input and output tokens per model call; include selector calls, retries and failed tasks. Record task ID, protocol, strategy, model version, elapsed time, tool selection correctness and success. Calculate total model cost / successful tasks using timestamped pricing and separately report infrastructure cost. No live results have been collected.

## Decision
Compare protocols within each selection strategy and strategies within each protocol. Do not attribute selection savings to UTCP alone.
