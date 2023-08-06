import click
import os
from .functions_tex import extract_tex_env


tikz_render=r"""
\vspace*{\fill}
\begin{center}
\input{tikz.tex}
\end{center}
\vspace*{\fill}
\pagebreak
"""

tikz_code=r"""
\vspace*{\fill}
\inputminted[tabsize=4, breaklines]{tex}{tikz.tex}
\vspace*{\fill}
"""


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
    
    try:
        extract_tex_env(inputfile, outputfile, environment)
        try:
            global files
            files = [f for f in os.listdir(f'{path_tikz}/tikz') if os.path.isfile(f)]
        except:
            click.echo("Faild to list files.")
    except:
        click.echo("Failed to extract_tex_env")

    with open(path_main, 'w') as file:
        file.write(f'\\documentclass{{article}}\n')
        file.write(f'\\usepackage{{v-equation}}\n')
        file.write(f'\\usepackage{{minted}}\n')
        file.write(f'\\usemintedstyle{{staroffice}}\n')
        file.write(f'\\vgeometry\n')

        file.write(f'\\begin{{document}}\n')

        print(files)
        if len(files) == 1:
            file.write(f'{tikz_render.replace("tikz.tex", files[0])}\n')
            file.write(f'{tikz_code.replace("tikz.tex", files[0])}\n')
        else:
            for f in files[1:-1]:
                file.write(f'{tikz_render.replace("tikz.tex", f)}\n')
                file.write(f'{tikz_code.replace("tikz.tex", f)}\n')
                if f != files[-1]:
                    file.write(f'\\pagebreak\n')

        file.write(f'\\end{{document}}')













