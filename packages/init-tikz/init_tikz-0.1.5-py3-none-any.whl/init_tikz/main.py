import click
import os
from .functions_tex import extract_tex_env


@click.command(
        help="Extracts tex environments from tex files"
        )
@click.option(
        '-i',
        '--inputfile',
        type=click.Path(),
        default="./main.tex",
        show_default=True,
        help="Input file path"
        )
@click.option(
        '-o',
        '--outputfile',
        type = click.Path(),
        default = "./tikz/tikz.tex",
        show_default=True,
        help = "Output file path"
        )
@click.option(
        '-e',
        '--environment',
        type=click.Choice(['tikzpicture', 'align*']),
        default="tikzpicture",
        show_default=True,
        help="Environment to be extracted"
        )
def main(inputfile, outputfile, environment):
    path_tikz = os.path.dirname(os.path.abspath(inputfile))
    os.makedirs(f'{path_tikz}/tikz', exist_ok=True)
    path_main = os.path.join(f'{path_tikz}/tikz', 'main.tex')
    extract_tex_env(inputfile, outputfile, environment)

    with open(path_main, 'w') as file:
        file.write(f'\\documentclass{{article}}\n')
        file.write(f'\\usepackage{{v-equation}}\n')
        file.write(f'\\usepackage{{minted}}\n')
        file.write(f'\\usemintedstyle{{staroffice}}\n')
        file.write(f'\\vgeometry\n')

        file.write(f'\\begin{{document}}\n')
        file.write(f'\\vspace*{{\\fill}}\n')
        file.write(f'\\begin{{center}}\n')
        file.write(f'\\input{{tikz-1.tex}}\n')
        file.write(f'\\end{{center}}\n')
        file.write(f'\\vspace*{{\\fill}}\n')

        file.write(f'\\pagebreak\n')

        
        file.write(f'\\vspace*{{\\fill}}\n')
        file.write(f'\\inputminted[tabsize=4, breaklines, linenos=true, fontsize=\\small]{{tex}}{{tikz-1.tex}}\n')
        file.write(f'\\vspace*{{\\fill}}\n')

        file.write(f'\\end{{document}}')













