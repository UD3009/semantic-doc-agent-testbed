# Success metric
Per structural/trap commit (S1-S4, T), score module-doc accuracy for:
1. Stale   - doc from before the change, no update
2. ROME    - doc after a targeted edit
3. Retune  - doc after a full LoRA re-tune
Report accuracy (fixed rubric + embedding similarity), edit latency, and cost.
Rubric is frozen before any results are generated.
