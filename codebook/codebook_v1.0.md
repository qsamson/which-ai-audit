# Codebook v1.0

This is the codebook used for first-pass coding and for the double-coded subsample. Changes made in v1.1 and v1.2 are listed in `codebook_changes_v1.1_v1.2.md`.

| Item | Rule |
|---|---|
| ft_decision | include, or exclusion code E1 E2 E3 E4 E6 |
| study_type | T1 researcher-controlled AI use; T2 secondary AI outputs; T3 participant-reported use |
| Item values | R = reported, P = partly, N = not reported, NA = not applicable |
| NA by type | T2: B3 B4 B5 C2 E2 are NA. T3: only A1 B1 D1 G1 apply. |
| A1 | Purpose/task of the AI in the study |
| A2 | Human-in-the-loop: whether humans reviewed, edited or relayed AI output |
| B1 | R = model + version AND date/snapshot of use; P = name or version only; N = AI not identified |
| B2 | Access mode: API, web interface, app, local |
| B3 | Parameters (temperature, top-p, max tokens, seed) or explicit "default settings" |
| B4 | Fine-tuning, customization or RAG, including explicit "not fine-tuned" |
| B5 | Memory / conversation history handling |
| C1 | Prompts: R = full prompts; P = examples or paraphrase |
| C2 | System instructions, custom instructions, personas |
| D1 | Personal data entering the AI: R = handling described; P = only general ethics/consent; NA = no personal data reached the AI |
| E1 | Human validation of AI outputs (not coding of interviews) |
| E2 | Post-processing of AI outputs |
| F1 | Code/data/materials: R = public link; P = on request or supplement |
| G1 | R = funding AND conflict-of-interest statements; P = one of them |
| X1 | Regime: Answering, Grounded/RAG, Customized assistant, Tool-using agent, Autonomous/multi-agent, Unclear |
| X2-X5 | Only for tool-using or autonomous regimes: X2 tools/data, X3 actions, X4 autonomy (operator, collaborator, consultant, approver, observer), X5 oversight |
| X6 | yes = conclusions about AI/chatbots generally AND limitations ignore model/regime specificity |
| R | Authors' own use of LLM tools for writing/analysis: none, or disclosed + model |
| Rule | Code independently, without looking at the AI-assisted coding sheet. Give a short verbatim quote for every R or P. |
