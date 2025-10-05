from jinja2 import Environment, FileSystemLoader
from app import services_path
from app.services.data_utils import get_supporting_data
import pandas as pd

def load_no_data_template(names: list[str]):
    """Loads temporary template that doesn't integrate stats."""
    template_path = services_path / 'templates'
    env = Environment(loader=FileSystemLoader(template_path))

    template = env.get_template('temporary_prompt.jinja')
    return template.render(names=names)


def load_data_template(ids: list[int], names: list[str], data: pd.DataFrame):
    """Loads adversery template using 2024 quarterback stats. Returns the rendered
    Jinja template as a string."""
    template_path = services_path / 'templates'
    env = Environment(loader=FileSystemLoader(template_path))

    llm_data = get_supporting_data(ids, names, data)
    # a list of stat, table (markdown rendered)

    template = env.get_template('adversary_prompt.jinja')
    return template.render(names=names, data=llm_data)
    