from jinja2 import Environment, FileSystemLoader
from app import services_path

def load_no_data_template(names: list[str]):
    template_path = services_path / 'templates'
    env = Environment(loader=FileSystemLoader(template_path))

    template = env.get_template('temporary_prompt.jinja')
    return template.render(names=names)