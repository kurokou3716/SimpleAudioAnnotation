import typer
import pandas as pd
import yaml
from random import choice

app = typer.Typer()

@app.command()
def gen_blank_result(
    dataset = typer.Argument(

    ), 
    config_file = typer.Argument(

    ),
    outfile = typer.Argument(

    ),
    file_list = typer.Option(
        None
    ),
    random : bool = typer.Option(
        False, '--random'
    )
):
    """
    """
    rows = pd.read_csv(
        dataset, delimiter='|'
    ).to_dict('records')
    configs = yaml.safe_load(open(config_file))

    temps = []
    for row in rows:
        temp = {
            'filename' : str(row['filename'])
        }
        for k in configs['labels']:
            label = configs['labels'][k]
            temp_field = label['fieldname']
            if label['type'] == 'radio':
                valueList = label['values']
                if random:
                    temp[temp_field] = choice(valueList)
                else:
                    temp[temp_field] = valueList[0]
            elif label['type'] == 'text_area':
                temp[temp_field] = label['values']
        temps.append(temp)

    df = pd.DataFrame(temps)
    df.to_csv(outfile, index=False, sep='|')

if __name__ == '__main__':
    app()