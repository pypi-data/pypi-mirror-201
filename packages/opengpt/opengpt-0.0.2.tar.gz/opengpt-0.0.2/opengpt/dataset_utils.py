import pandas as pd
import math
import os
import json
import hashlib
from tqdm.auto import tqdm
from opengpt import parsers
from opengpt.openai_api import ask_openai
from tqdm.auto import tqdm
import logging

def split_csv_by_max_len(datasets, max_len, tokenizer, base_path):
    for dataset in tqdm(datasets, desc='Datasets', total=len(datasets)):
        csv_path = dataset['path']
        name = dataset['name']

        df = pd.read_csv(csv_path)
        cols = df.columns
        assert 'text' in cols, f'The CSV for dataset {name} has no "text" column.'

        new_data = [list(cols) + ['len', 'part']]
        for _, row in tqdm(df.iterrows(), desc=dataset['name'], total=len(df)):
            text = row['text']
            tokens = tokenizer.encode(text)

            for i in range(math.ceil(len(tokens) / max_len)):
                new_text = tokenizer.decode(tokens[i*max_len:(i+1)*max_len])
                new_data_row = [row[c] if c != 'text' else new_text for c in cols]
                new_data_row.append(len(tokens[i*max_len:(i+1)*max_len]))
                new_data_row.append(f'part_{i}')
                new_data.append(new_data_row)
        
        # Save
        new_df = pd.DataFrame(new_data[1:], columns=new_data[0])
        new_df.to_csv(os.path.join(base_path, name, 'data_split_by_length.csv'))
        logging.info(f'{dataset["name"]}: length before vs after: {len(df)} vs {len(new_df)}\n')

def create_dataset(config):
    prompt_db = json.load(open(config.path.prompt_db, 'rb'))
    data_columns = ['text', 'dataset', 'language', 'run', 'prompt_hash', 'prompt_text_hash', 'context']
    data = pd.DataFrame(None, columns=data_columns)
    data_path = os.path.join(config.base_path, f"generated_data_for_{config.name}.csv")
    if os.path.exists(data_path):
        data = pd.read_csv(data_path)
        logging.warning(f"Loading an existing openai generated dataset found at: {data_path} " + 
                        f"There are already {len(data)} rows in the that dataset, the generation will continue from where last left off. " + 
                        f"The script will also do all examples that were not done in the previous run.")

    cnt = 0
    for prompt_config in config.prompts:
        prompt = [prompt for prompt in prompt_db if prompt['hash'] == prompt_config['hash']][0] # There must be one
        parser = getattr(parsers, prompt['parser'])

        for run in range(prompt_config.get('runs', 1)):
            parameters = prompt_config['extra_parameters']

            for language in prompt_config.get('languages', ['English']):
                parameters['language'] = language
                prompt_text_template = prompt['text']

                logging.info(f"\nStarting prompt: {prompt_config['hash']}\nRun: {run}\nLanguage: {language}")
                for dataset_name in prompt_config['datasets']:
                    df = pd.read_csv(os.path.join(config.base_path, dataset_name, 'data_split_by_length.csv'))
                    for row_ind, row in tqdm(df.iterrows(), desc=dataset_name, total=len(df)):
                        parameters['context'] = row['text']
                        prompt_text = prompt_text_template.format(**parameters)
                        # The hash is of everything that is used to generate the output
                        h = hashlib.sha256(prompt_text.encode("utf-8"))
                        h.update(str(run).encode("utf-8"))
                        h = h.hexdigest()

                        # Only get the output if this was not done already
                        if h not in data.prompt_text_hash.values:
                            # Get output from OpenAI and parse using parser, the parser returns a list of strings.
                            #The parser will append references and everything else needed.
                            output = None
                            try:
                                openai_output = ask_openai(prompt_text, config)
                                output = parser(data=openai_output, prompt_config=prompt_config, config=config, row=row)
                            except Exception as e:
                                logging.exception(e)
                                logging.warning(f"Skipping example at position: {row_ind} for dataset: {dataset_name}")

                            # Parser will return None if there is a mistake in the ChatGPT output, we just skip those
                            if output is not None and len(output):
                                # Concat the current output to the data dataframe
                                new_data = pd.DataFrame([[text, dataset_name, language, run, prompt_config['hash'], h, parameters['context']] for text in output], columns=data_columns)
                                data = pd.concat([data, new_data], ignore_index=True)

                                cnt += 1
                                if cnt % config.data_generation_checkpoint_every == 0:
                                    logging.info("Checkpointing the generated dataset.")
                                    data.to_csv(data_path, index=False)
    # Final save
    data.to_csv(data_path, index=False)
    return data

def create_labels(examples, config, tokenizer):
    r''' This is used with a prepared HF dataset that is already tokenized. It will add labels
    so that only the AI generated parts (answers) will be trained on.
    '''
    
    user_token_id = tokenizer.vocab[config.special_tokens.user]
    ai_token_id = tokenizer.vocab[config.special_tokens.ai]
    # Everything written by an AI will be used for training, and everything by a user will be ignored

    examples['labels'] = []
    for i in range(len(examples['input_ids'])):
        labels = []
        ignore = True
        for tkn_id in examples['input_ids'][i]:
            if tkn_id == user_token_id:
                ignore = True
            elif tkn_id == ai_token_id:
                ignore = False
            
            if ignore:
                labels.append(config.train.ignore_index)
            else:
                labels.append(tkn_id)
        examples['labels'].append(labels)
    return examples

def pack_examples(examples, block_size, packing_type='partial'):
    r''' Used with a prepared HF dataset, will pack/group examples. Use with care, can mess up many things
    if the input is not formated properly (requires the <|eod|> token).
    
    partial_packing: will trim long examples
    '''
    # Concatenate all texts.
    if packing_type == 'partial':
        result = {k:[] for k in examples.keys()}
        _key = list(examples.keys())[0] # Take whichever key
        new_example = {k:[] for k in examples.keys()}

        for ind in range(len(examples[_key])):
            # Trim long sequences to block_size, this is required for partial packing
            example = {k:v[ind][0:block_size] for k,v in examples.items()}
            if len(new_example[_key]) + len(example[_key]) > block_size:
                result = {k:result[k] + [v] for k,v in new_example.items()}
                new_example = example 
            else:
                new_example = {k:new_example[k] + v for k,v in example.items()}
        #  Add the last example if there is something to add  
        if len(new_example[_key]) > 0:   
            result = {k:result[k] + [v] for k,v in new_example.items()}
    elif packing_type == 'full':
        # Full packing
        concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
        total_length = len(concatenated_examples[list(examples.keys())[0]])
        total_length = (total_length // block_size) * block_size
        # Split by chunks of max_len.
        result = {
            k: [t[i : i + block_size] for i in range(0, total_length, block_size)]
            for k, t in concatenated_examples.items()
        }
    else:
        # Do nothing
        result = examples
    return result