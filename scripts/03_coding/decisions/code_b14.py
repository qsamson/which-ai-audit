D = {
'FT126': dict(dec='E6', dec_q='participants in the two experi­ mental conditions were informed that the supervisor\'s e-mail was generated with the help of an AI tool', note='Vignette: AI involvement only framed.'),
'FT128': dict(type='T3', ov={'A1': ('R', 'The study first collected respondents’ basic demographic information, which included gender, educational background, frequency of chatbot use'), 'B1': 'N', 'D1': 'N'},
              X1='Answering', X6='yes', note='Survey of Gen Z chatbot users; no chatbot named.'),
'FT129': dict(type='T1', ov={'A1': ('R', 'individualized voice cloning that replicates users\' voices'), 'A2': 'N', 'B1': 'N', 'B2': 'N', 'C1': 'N', 'D1': 'N', 'E1': 'N', 'E2': 'N'},
              X1='Answering', X6='yes', R='disclosed: Claude (writing)', note='AI voice agents with cloned voices; cloning tool not identified in coding pass.'),
'FT132': dict(type='T1', ov={'A1': ('R', 'Participants engaged in face-to-face social interactions with an LLM-controlled agent in Virtual Reality.'), 'A2': 'N',
              'B1': ('P', 'The text input was then forwarded as a prompt to a text generation model (“SauerkrautLM-HerO”'), 'B2': ('R', '@'), 'B4': 'N', 'C1': ('R', '@'), 'E1': 'N', 'F1': ('P', '@')},
              X1='Customized assistant', X6='no', note='Open-weights SauerkrautLM via Hugging Face; persona prompts and temperatures in Table 1.'),
'FT134': dict(type='T2', ov={'A1': ('R', 'enhance human discrimination between real and StyleGAN2 faces'), 'A2': 'N', 'B1': ('P', 'StyleGAN2-generated images of White human faces are especially problematic'), 'C1': 'NA', 'E1': 'N', 'F1': ('P', '@')},
              X1='Answering', X6='no', note='StyleGAN2 faces detection training.'),
'FT136': dict(type='T3', ov={'A1': ('R', '@'), 'B1': 'N'},
              X1='Answering', X6='yes', R='none', note='GAI literacy scale (borderline T3).'),
}
D['FT136']['ov']['A1'] = ('R', 'After receiving approval from the ethics review board of the authors’ university, we developed a standard scale to measure GAI literacy in DMC.')
