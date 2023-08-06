import typer
import json
import yaml
import datetime
import dateutil.parser

app = typer.Typer()

def timestamp_constructor(loader, node):
    return dateutil.parser.parse(node.value)

yaml.add_constructor(u'tag:yaml.org,2002:timestamp', timestamp_constructor)

@app.command()
def yaml2json(yamlfile: typer.FileText, output: typer.FileTextWrite = typer.Option(None), pretty: bool = True):
    if output:
        if pretty:
            json.dump(
                yaml.safe_load(yamlfile.read()),
                output,
                # sort_keys=True,
                indent=2,
                separators=(',', ': '),
                cls=JsonTimeEncoder
            )
        else:
            json.dump(
                yaml.safe_load(yamlfile.read()),
                output,
                cls=JsonTimeEncoder
            )
    else:
        if pretty:
            print(pretty_output(yamlfile.read()))
        else:
            print(compressed_output(yamlfile.read()))


# -----------------------------------------------------------------------------

class JsonTimeEncoder(json.JSONEncoder):
    """
    Converts datetime objects into strings for JSON.
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            if int(obj.strftime('%f')) == 0:
                return obj.strftime('%Y-%m-%dT%H:%M:%S%z')
            else:
                return obj.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

# -----------------------------------------------------------------------------

def pretty_output(read):
    return json.dumps(
        yaml.safe_load(read),
        # sort_keys=True,
        indent=4,
        separators=(',', ': '),
        cls=JsonTimeEncoder
    )

def compressed_output(read):
    return json.dumps(
        yaml.safe_load(read),
        cls=JsonTimeEncoder
    )

# -----------------------------------------------------------------------------


