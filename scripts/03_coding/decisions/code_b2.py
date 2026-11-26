D = {
'FT010': dict(dec='E6', dec_q='Respondents were not shown examples of such images.', note='Focus groups discussed AI images in general; no AI output seen.'),
'FT011': dict(type='T2', ov={'A1': ('R', 'we successfully extracted text containing conversa­ tional episodes between users and Replika'), 'A2': 'N', 'B2': 'N', 'C1': 'N', 'D1': 'N', 'E1': 'N', 'F1': 'N'},
              X1='Answering', X6='yes', note='Reddit screenshots of Replika chats (T2). BERT/sentenceBERT used as analysis tools.'),
'FT012': dict(type='T1', ov={'A1': ('R', 'with an AI chatbot powered by GPT-4'), 'A2': ('R', 'copying AI-generated messages, editing messages written by AI, or asking AI for guidance and then writing their own messages'), 'B1': ('P', 'with an AI chatbot powered by GPT-4'), 'C1': 'N', 'F1': ('P', '@')},
              X1='Answering', X6='yes', note='Participants wrote support messages with GPT-4 chatbot; temperature 0.01.'),
'FT013': dict(type='T1', ov={'A1': ('R', 'participants interacted with an AI chatbot based on OpenAI’s LLM GPT-4o-mini'), 'A2': 'N', 'B1': ('R', 'OpenAI’s LLM GPT-4o-mini (version 2024-07-18)'), 'B2': ('R', 'We manipulated the bots’ conversational behavior by changing the system prompt of the LLM in our underlying call to the OpenAIAPI.'), 'C2': ('R', '@'), 'F1': ('P', '@')},
              X1='Customized assistant', X6=('no', '@'), note='System-prompt manipulated GPT-4o-mini; exact prompts in S1. Version string counts as dated snapshot.'),
'FT014': dict(type='T1', ov={'A1': ('R', 'we first had ChatGPT-4o generate 15 relational maintenance activities'), 'A2': 'N', 'B1': ('P', 'we first had ChatGPT-4o generate 15 relational maintenance activities'), 'B4': 'N', 'F1': ('P', '@')},
              X1='Answering', X6=('no', 'the operationalization of GenAI is limited in ecologi­ cal validity'), note='Pre-generated ChatGPT-4o plans; preregistered.'),
'FT015': dict(type='T1', ov={'A1': ('R', 'they entered the testing page on which they had real interaction with Aida'), 'A2': 'N', 'B1': ('P', 'a newly developed health assistant powered by GPT 3.5, called Aida'), 'B4': 'N', 'B5': 'N', 'C1': ('P', 'On the left-hand side, we provided the assigned prompt and instructions.'), 'D1': 'P', 'F1': ('R', '@')},
              X1='Customized assistant', X6='yes', note='Custom GPT-3.5 assistant inserting misinformation; OSF prereg.'),
}
