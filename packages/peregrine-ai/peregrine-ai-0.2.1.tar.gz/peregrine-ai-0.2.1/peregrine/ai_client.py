import openai
from pathlib import Path
import os
import typer
from peregrine import utils

class KeyNotFoundError(Exception):
    pass

def check_env(func):
    def wrapper(*args, **kwargs):
        key = utils.get_key()    
        
        if key:
            retval = func(*args, **kwargs)
            return retval
        else:
            raise KeyNotFoundError("No OpenAI API key found. Create an OpenAI API Key, then run `ai --openai-key` to save your key.")
    return wrapper

@check_env
def ai_suggest(user_input: str) -> str:
    prompt = f"Translate the following action to a valid one-line bash command. Reply only with a one line bash command to fulfile the request, no other text. Assume any tools are installed: {user_input}"
    
    model = utils.get_model()

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": f"{prompt}"},
        ],
        temperature=0
    )

    # return the command suggested by GPT
    cmd = response.choices[0]["message"]["content"].strip().split("\n")[0]
    return cmd

@check_env
def ai_explain(command_str: str, context: str = None) -> str:

    prompt = f"Explain the following bash command and it's flags and arguments concisely to a knowledgeable audience: {command_str}"
    prompt_msg = {"role": "user", "content": f"{prompt}"}

    context_msgs = [prompt_msg]

    if context:
        context_lines = context.split("\n")
        context_msgs = [ {"role": "user", "content": context_msg} for context_msg in context_lines ].append(prompt_msg)    

    response = openai.ChatCompletion.create(
        model=utils.get_model(),
        messages=context_msgs
    )

    # return the command suggested by GPT
    return (response.choices[0]["message"]["content"], response.choices[0]["finish_reason"])

@check_env
def ai_explain(command_str: str, context: str = None) -> str:

    prompt = f"Explain the following bash command and it's flags and arguments concisely to a knowledgeable audience: {command_str}"
    prompt_msg = {"role": "user", "content": f"{prompt}"}

    context_msgs = [prompt_msg]

    if context:
        context_lines = context.split("\n")
        context_msgs = [ {"role": "user", "content": context_msg} for context_msg in context_lines ].append(prompt_msg)    

    response = openai.ChatCompletion.create(
        model=utils.get_model(),
        messages=context_msgs
    )

    # return the command suggested by GPT
    return (response.choices[0]["message"]["content"], response.choices[0]["finish_reason"])

@check_env
def ai_alternatives(cmd1: str, number: int = 1, prompt: str = None):

    if not prompt:
        prompt = f"Reply with a command that would also accomplish a similar action as this command: {cmd1} using a different tool. If no good alternatives exist, reply with the original command."

    response = openai.ChatCompletion.create(
        model=utils.get_model(),
        messages=[ {"role": "user", "content": prompt} ],
        temperature=0.5    
    )

    # return the command suggested by GPT
    return response.choices[0]["message"]["content"].strip().split("\n")[0]


    