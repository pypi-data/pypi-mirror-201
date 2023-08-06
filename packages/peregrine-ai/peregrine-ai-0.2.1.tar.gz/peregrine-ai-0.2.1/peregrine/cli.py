from peregrine import ai_client, utils
import click
import typer
import fcntl, termios, sys
from halo import Halo
from peregrine import ai_client
from pathlib import Path

class APIKeyAddError(Exception):
    pass

class OpenAIException(Exception):
    pass

app = typer.Typer()

@app.command()
def how(input_action_qry: str, force_response= None):
    
    spinner = Halo(text='Loading', spinner='dots')
    
    if force_response:
        response = force_response
    else:
        try:
            spinner.start()
            response = ai_client.ai_suggest(input_action_qry)
        except Exception as e:
            spinner.stop()
            typer.echo(f"{utils.colors.FAIL} Encountered error when querying OpenAI API: {e}. \n Exiting...")
            raise typer.Exit()
        else:
            spinner.stop()
    
    action = typer.prompt(f"{utils.colors.OKGREEN}Suggestion:{utils.colors.ENDC} {utils.colors.BOLD}{response}{utils.colors.ENDC}\nUse this command? [y: copy / e: explain / a: alternatives / exit]: ", type=str)

    if action == "y":
        if response:
            # write generated prompt into terminal input buffer
            for c in response:
                fcntl.ioctl(sys.stdin, termios.TIOCSTI, c)

        raise typer.Exit()

    elif action == "e":

        what(response)        
        how("", force_response=response)

    elif action == "a":

        alt_resp = alternatives(response)
        alt_action = typer.prompt(f"{utils.colors.BOLD}Use alternative command: {alt_resp}? [y/N]: ", type=str)

        if alt_action == "y":
            response = alt_resp

        how("", force_response=response)
    
    else:
        typer.Exit()


@app.command()
def alternatives(command_str: str, number: int = 1):
    spinner = Halo(text='Loading', spinner='dots')
    
    alt_response = ""
    try:
        spinner.start()
        alt_response = ai_client.ai_alternatives(command_str, number)
    except Exception as e:
        spinner.stop()
        typer.echo(f"{utils.colors.FAIL} Encountered error when querying OpenAI API: {e}. \n Exiting...")
        raise typer.Exit()
    else:
        spinner.stop()
        typer.echo(f"{utils.colors.OKCYAN}Alternative: {utils.colors.ENDC} {alt_response}.")

    return alt_response


@app.command() 
def what(command_str: str, context = None):

    spinner = Halo(text='Loading', spinner='dots')

    try: 
        spinner.start()
        explain, stop_reason = ai_client.ai_explain(command_str, context)
    except Exception as e:
        spinner.stop()
        typer.echo(f"{utils.colors.FAIL} Encountered error when querying OpenAI API: {e}. \n Exiting...")
        raise typer.Exit()
    else:
        spinner.stop()
        typer.echo(f"{utils.colors.OKCYAN}{explain}{utils.colors.ENDC}")
    
        if stop_reason != "stop":
            typer.echo(f"{utils.colors.WARNING} Output stopped prematurely:{utils.colors.ENDC} {stop_reason}.")


@app.command()
def openai_key():

    in_key = typer.prompt("Input a valid OpenAI API key", type=str)
    
    try:
        utils.set_key(in_key)
    except Exception as e:
        typer.echo(f"{utils.colors.FAIL}Failed to add API Key.{utils.colors.ENDC} Error text: {e}.")
        typer.Abort()
    else:
        typer.echo(f"{utils.colors.OKGREEN}API key successfully added! Retry your query. {utils.colors.ENDC}")
        raise typer.Exit()


# @app.command()
# def select_model():
    
#     typer.echo(f"{utils.colors.BOLD}Current Model:{utils.get_model()} {utils.colors.ENDC}")

#     typer.echo("Select from: \n")
#     typer.echo(utils.models.MAPPING)
    
#     request = typer.prompt("Select a model [1-4]", type=int)

#     if not request in range(1, 5):
#         request = 1

#     print(request)
#     utils.set_model(request)
    
#     typer.echo(f"Model set to {utils.models.MAPPING[request]}.")
    

@app.callback()
def main():

    utils.make_env()

    key = utils.get_key()
    if not key:
        openai_key()

