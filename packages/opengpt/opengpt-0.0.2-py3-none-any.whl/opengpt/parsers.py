import pandas as pd
from io import StringIO
import re
import logging

def csv_parser(data, prompt_config, config, row):
    r''' Try to load the output into a dataframe, if it fails we skip.
    '''
    qa_pairs = None
    df = pd.read_csv(StringIO(data), sep=';;;;', engine='python')

    # Strip everything
    df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    ref_col = prompt_config.get('reference_column_to_append', None)
    if ref_col and ref_col in row and row[ref_col]:
        # Means we want to append a reference at the end of each Answer
        to_append = f"\nReferences:\n- {row[ref_col]}"
        df['Answer'] = df['Answer'] + to_append
    df['Question'] += f' {config.special_tokens.eos}' # Every Q/A pair is independent
    df['Answer'] += f' {config.special_tokens.eos} {config.special_tokens.eod}'
    qa_pairs = [f'{config.special_tokens.user} {q.strip()} {config.special_tokens.ai} {a.strip()}' for q,a in df[['Question', 'Answer']].values]
    return qa_pairs 


def medical_conversation_parser(data, prompt_config, row, config):
    conversation = None

    # Merge the extractions into one conversation
    data = re.split(r'\s*(Patient:|AI-Assistant:)\s*', data)[1:]
    if len(data) > 0:
        conversation = ""
        to_append = None

        ref_col = prompt_config.get('reference_column_to_append', None)
        if ref_col and ref_col in row and row[ref_col]:
            # Means we want to append a reference at the end of each Answer
            to_append = f"\nReferences:\n- {row[ref_col]}"

        actor = None
        for message in data:
            message = message.strip()
            if message in ['Patient:', 'AI-Assistant:']:
                actor = message
            elif actor is not None: 
                if actor == 'Patient:':
                    conversation += f'{config.special_tokens.user} {message} {config.special_tokens.eos} '
                elif actor == 'AI-Assistant:':
                    conversation += f'{config.special_tokens.ai} {message}'
                    if to_append is not None and to_append:
                        conversation += to_append
                    conversation += f" {config.special_tokens.eos} "
        if conversation:
            # Make into an array, as parsers have to return arrays
            conversation = conversation.strip() + f" {config.special_tokens.eod}"
            conversation = [conversation.strip()]
    return conversation 