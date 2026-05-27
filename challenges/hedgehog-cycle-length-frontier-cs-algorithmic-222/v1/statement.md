# Hedgehog Cycle Length

This is an interactive `zip_project` challenge. Your run command is started once and communicates with a trusted evaluator over stdin/stdout. The evaluator owns the hidden Frontier-CS state and enforces the original interactor protocol, query validation, and scoring for `algorithmic/problems/222`.

Follow the original Frontier-CS interactive protocol shown by the prompts sent by the evaluator. A session may contain one or more original Frontier-CS cases; after a case terminates, the evaluator may immediately start the next case in the same stdin/stdout session. Exit after stdin closes.

Public validation is a small synthetic protocol smoke. Official scoring uses private Frontier-CS-derived cases and reports the average source interactor ratio as `score` from 0 to 100. Protocol errors, malformed commands, query-limit failures, and wrong final answers receive zero for the affected case and stop the session.
