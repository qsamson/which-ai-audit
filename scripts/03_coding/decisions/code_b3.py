D = {
'FT016': dict(dec='E6', dec_q='see online supplementary material for pre-scripted dialog', note='Simulated, pre-scripted AI interaction (Wix stimulus); no real AI output.'),
'FT017': dict(type='T1', ov={'A1': ('R', 'we aim to estimate the prevalence and magnitude of representational bias in DALL·E 2 images'), 'A2': 'N', 'B1': ('P', 'we aim to estimate the prevalence and magnitude of representational bias in DALL·E 2 images'), 'B2': ('R', '@'), 'C2': 'NA', 'D1': 'NA', 'F1': ('P', '@')},
              X1='Answering', X6='yes', note='DALL·E 2 API audit, 153 occupations; no access date.'),
'FT018': dict(type='T1', ov={'A1': ('R', 'informed about using a GPT-4 chatbot, simulating a scenario of a local government’s hurricane prepared'), 'A2': 'N',
              'B1': ('R', 'leveraging GenAI capabilities of an internally trained model designated as “gpt-4-1106-preview.”'), 'B2': ('R', 'bot utilizes OpenAI’s Chat Completions API'), 'B4': 'N', 'B5': ('R', '@'),
              'C2': ('P', 'this chatbot was prompted to “adapt your language, tone, slang, acronyms, emojis, and other textual cues as appropriate based on the %race%,”'), 'D1': 'N', 'E2': 'N',
              'F1': ('R', 'The source code of our chatbot and its user instructions are available at: https://bitbucket.org/leecwwong/ai_chatbot/.')},
              X1='Customized assistant', X6='yes', note='Culturally tailored GPT-4 chatbots, 441 participants; code on Bitbucket.'),
'FT019': dict(type='T2', ov={'A1': ('R', 'The datasets analysed during the current study are available in the LMSYS-CHAT-1M repository'), 'A2': 'N', 'B2': 'N', 'C1': 'N', 'D1': 'N', 'E1': 'N', 'F1': ('R', '@'), 'G1': 'N'},
              X1='Answering', X6='yes', note='Refusals in LMSYS-Chat-1M logs (many LLMs; not separated).'),
'FT020': dict(dec='E2', dec_q='the current version of Bürokratt is mainly able to answer frequently asked questions', note='Public-sector FAQ chatbots, not generative AI.'),
'FT022': dict(dec='E2', dec_q='we focus on interactions initiated by Duplex in its publicly', note='Google Duplex (2018) calls; pre-LLM system.'),
'FT023': dict(type='T2', ov={'A1': ('R', 'The screenshots were introduced as “a case where AI is utilized in a new product launched by Google.”'), 'A2': 'N', 'B4': 'N', 'C1': 'N', 'D1': 'P', 'F1': 'N'},
              X1='Answering', X6='yes', note='Survey experiment with real Gemini image screenshots.'),
'FT025': dict(type='T1', ov={'A1': ('R', '@'), 'A2': 'N', 'C1': ('P', 'The concept of algorithmic bias was exemplified by prompting Midjourney to make pictures of government leaders'), 'C2': 'NA', 'D1': 'NA', 'F1': ('P', '@')},
              X1='Answering', X6='yes', note='Children workshops using Midjourney.'),
}
D['FT025']['ov']['A1'] = ('R', 'The concept of algorithmic bias was exemplified by prompting Midjourney to make pictures of government leaders')
