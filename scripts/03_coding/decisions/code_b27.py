D = {
'FT253': dict(type='T1', ov={'A1': ('R', 'For the following year, we built on this important observation and designed an interactive art installation'), 'A2': 'N',
              'B1': ('P', 'Within T2I-Adapter, images were generated with Stable Diffusion version 1.5 [54] with 50 diffusion steps and CFG 8.0.'), 'B3': ('R', 'Within T2I-Adapter, images were generated with Stable Diffusion version 1.5 [54] with 50 diffusion steps and CFG 8.0.'),
              'B4': 'N', 'C2': 'NA', 'E1': 'N'},
              X1='Answering', X6='no', note='Body-prompting art installation; SD 1.5 settings and code on GitHub.'),
'FT254': dict(type='T3', ov={'A1': ('R', '@'), 'B1': ('P', '@')},
              X1='Answering', X6='no', note='Interviews with AI red teamers.'),
'FT255': dict(type='T1', ov={'A1': ('R', 'By making conversational features optional (via manual chat initiation), we could distinguish between participants who utilized the AI'), 'A2': 'N',
              'B1': ('P', 'While GPT-4-turbo produced the highest quality outputs, GPT-4o-mini delivered comparable consistency at substantially lower cost'), 'B2': ('P', '@'), 'B4': 'N',
              'B5': ('R', 'While personas were visible, participants were not aware of the memory capacities'), 'E1': 'N', 'E2': 'N', 'F1': ('P', '@')},
              X1='Customized assistant', X6='no', note='GPT-4o-mini NPCs with memory and system prompts.'),
'FT256': dict(type='T1', ov={'A1': ('R', 'Design, Implementation and Evaluation of an LLM-powered Meeting Recap System'), 'A2': 'N', 'B1': 'N', 'B2': 'N', 'B4': 'N', 'B5': ('P', '@'), 'E1': 'N', 'F1': ('P', '@')},
              X1='Answering', X6='yes', note='LLM meeting recap system; model not identified in coding pass.'),
'FT257': dict(type='T1', ov={'A1': ('R', '@'), 'A2': 'N', 'B1': ('P', 'We utilized version 1.3.2 of the local version of Stable Diffusion, along with the v5-PrtRE version of the Anything Model.'),
              'B2': ('R', 'We utilized version 1.3.2 of the local version of Stable Diffusion'), 'B4': 'N', 'B5': 'N', 'C2': 'NA', 'D1': 'N'},
              X1='Answering', X6='no', note='Older adults recreating memories with local SD.'),
'FT258': dict(type='T1', ov={'A1': ('R', 'we used the final version of the texts redacted by GPT and asked the AI system to reconstruct a text in the same genre and tone'), 'A2': 'N',
              'B1': ('P', 'we used the final version of the texts redacted by GPT'), 'B2': 'N', 'B4': 'N', 'B5': 'N', 'C1': ('P', '@'), 'C2': 'N', 'D1': 'N', 'E1': 'N', 'E2': 'N', 'F1': ('P', '@')},
              X1='Answering', X6='yes', note='Mostly conceptual; includes analysis of ChatGPT outputs (kept under real-output rule). Flag for second coder.'),
'FT259': dict(type='T1', ov={'A1': ('R', 'For the A/B testing experiment, we targeted 100 participants'), 'A2': 'N', 'B1': 'N', 'B2': 'N', 'B4': 'N', 'C1': 'N', 'E1': 'N', 'G1': 'P'},
              X1='Answering', X6='yes', note='Expert inputs on LLM completions; survey + A/B test; LLM not named in methods.'),
'FT260': dict(type='T3', ov={'A1': ('R', 'Delving into the collective understanding and emerging GenAI use practices'), 'B1': 'N', 'D1': 'N'},
              X1='Answering', X6='yes', R='disclosed: ChatGPT (analysis)', R_q='In this stage, the researchers also employed ChatGPT to refine the labels and table keywords.', note='Interviews on GenAI in higher education.'),
}
D['FT254']['ov']['A1'] = ('R', 'For instance, P7, facing the challenge of injecting large volumes of misinformation to stress-test generative models, used ChatGPT to')
D['FT254']['ov']['B1'] = ('P', 'For instance, P7, facing the challenge of injecting large volumes of misinformation to stress-test generative models, used ChatGPT to')
D['FT257']['ov']['A1'] = ('R', 'Each workshop was held virtually using an online meeting tool')
