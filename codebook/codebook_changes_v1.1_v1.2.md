# Codebook v1.1 – changes made in the final coding pass (for the OSF deviations log)

Date: 25 Nov 2026. Coder: Claude (AI-assisted), first-author review pending.
Trigger: Claude–GPT comparison on the 51-paper reliability sample showed that Claude systematically under-coded G1 and B1. The re-check covered all 220 included papers, not only the sample.

1. **B1 (model identity)**
   - R requires a version for every model whose outputs are analysed, plus a date or dated snapshot of this study's use. The date can be a dated API snapshot (e.g., gpt-4o-2024-08-06) or a stated data-collection window during which participants used the model live.
   - A version the authors infer ("the most likely models", "were the current versions") stays P.
   - A participant-survey date counts only if the version is also named.
2. **G1 (funding/COI)**
   - The detection regex now accepts PDF ligatures (ﬂ, ﬁ), the headings "Funding information", "Author Disclosure Statement" and "Declaration of conflicting interests", and funding stated only in the Acknowledgements.
   - It excludes the CRediT term "Funding acquisition" and body-text uses of "funding".
3. **T3 applicability**
   - Per codebook v1.0 ("for T3 only A1 B1 D1 G1 apply"), X1–X6 are now NA for T3 papers. v1.0 coding had applied them.
   - H3 and H4 denominators are now T1+T2 (n = 159).
4. **X6 (over-generalisation), operational rule**
   - yes = the abstract or conclusion states a finding about AI/GenAI/LLMs/chatbots as a class, AND no sentence anywhere notes that results may depend on the specific model, version, tool or configuration, or that models change over time.
   - no = the conclusion is about the authors' own named system or case, OR findings are differentiated by model, OR a model/version caveat is present.
   - Every yes now carries a verbatim quote.
5. **E1**
   - Eight T1 papers were upgraded to R where human validation or rating of AI outputs is described.
   - E1, A2, E2 and D1 were not fully re-derived. They are left to adjudication.

All quotes were verified as verbatim substrings of the full text (0 errors). Every change and its reason is listed in `recheck_log_v11.csv` and in the "Final-pass changes" sheet.

## v1.2 – X6 rule agreed with the first author (25 Nov 2026)
Each eligible paper (T1+T2, n = 159) gets three judgments:
- **General AI claim**: the conclusion makes a claim about AI or chatbots generally.
- **Model/version caveat**: the authors explicitly say the finding may depend on the model or version used. Naming the model in Methods does not count.
- **X6 (H4 outcome)**: yes = general AI claim AND the limitations give no qualification about the model OR the setup (prompts, stimuli, configuration, interface, dose, snapshot in time).

A setup caveat (e.g., FT037's portrait prompt) makes X6 = no, but it does not count as a model/version caveat.

This replaces v1.1's narrower rule, under which only model/version caveats counted. On the 51-paper subset, the first author's independent pass and Claude's recode agree on all 34 papers both coded: 2 yes (FT039, FT271). FT168 was adjudicated to no by the first author.
