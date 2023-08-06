import click
import os
import time


from .chapters import chapters_list
from .problem import Problem
from .choice_option import ChoiceOption

path_parent = os.environ["TEX_PARENT_PATH"] 

eqn_number_without_database = f'{int(time.strftime("%H%M%S%d%m%Y")):14}'

option=r"""
\def\option{
\begin{tasks}(2)
\task $\dfrac{b^2\tau}{4}$
\task $\dfrac{b^2\tau}{2}$
\task $b^2\tau$
\task $\dfrac{b^2\tau}{\sqrt{2}}$
\end{tasks}
}"""

diagram=r"""
\begin{center}
\begin{tikzpicture}
\pic at (0, 0) {frame=5cm};
\end{tikzpicture}
\end{center}
"""


assemble=r"""
\vspace*{\fill}
\begin{tikzpicture}
	\node[qnumber] (n) at (0, 0)[scale=2] {$\pn.$};
	\node[question] (q) [right=2mm of n.east] {\question};
	\tzline[divider]<-0.125, 0> (q.north west)(q.south west);
	\node[format] (f) at  (q.south east){[\exam \quad \year]};
\end{tikzpicture}	
\vspace*{\fill}
"""

qrcode=r"""
\vspace*{\fill}
\begin{center}
	\fbox{\qrcode[height=2cm]{\gdrive}}
\end{center}
\vspace*{\fill}
"""

size_square = f'\\vgeometry\n\n'
size_h_rectangle = f'\\vgeometry[8][4.5]\n\n'
size_v_rectangle = f'\\geometry[4.5][8]\n\n'

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(
        context_settings = CONTEXT_SETTINGS,
        help="Creates problem format tex file"
        )
@click.option(
        '-c',
        '--chapter',
        prompt='Chapters',
        type=click.Choice(
            chapters_list,
            case_sensitive=False),
        cls=ChoiceOption,
        help="Chapter name",
        )
@click.option(
        '-f',
        '--format_problem',
        prompt='Format',
        default=1,
        type=click.Choice(['JEE', 'IIT-JEE', 'NEET', 'BOOK', 'MINE']),
        cls=ChoiceOption,
        help='Format of the problem'
        )
@click.option(
        '-s',
        '--size',
        prompt='Size',
        default=1,
        type=click.Choice(['square', 'h-rectangle', 'v-rectangle']),
        cls=ChoiceOption,
        show_default=True,
        help="Size of the canvas"
        )
@click.option(
        '-n',
        '--problem_number',
        type=click.INT
        )
@click.option(
        '-a',
        '--append_to_database',
        is_flag=True,
        default=True,
        prompt=True,
        help="flag (-a turns-on) appends the equation to database"
        )
def main(chapter, format_problem, size, problem_number, append_to_database):
    problem = Problem(format_problem.lower(), chapter, path_parent)
    if append_to_database:
        try:
            problem_number = problem.get_data(1)[0][0] + 1
        except:
            problem_number = 1
        problem.insert_data()
    else:
        problem_number = eqn_number_without_database

    path_problem= os.path.join(
            problem.path_problem_format(),
            f'problem-{problem_number:02}'
            )


    os.makedirs(path_problem, exist_ok=True)
    os.makedirs(f'{path_problem}/downloads', exist_ok=True) 
    main_tex = os.path.join(path_problem, 'main.tex')
    with open(main_tex, 'w') as file:
        file.write(f'\\documentclass{{article}}\n')
        file.write(f'\\usepackage{{v-problem}}\n')
        if size == 'square':
            file.write(size_square)
        elif size == 'h-rectangle':
            file.write(size_h_rectangle)
        elif size == 'v-rectangle':
            file.write(size_v_rectangle)

        file.write(f'\\begin{{document}}\n')
        file.write(f'\\vtitle[{chapter.upper()}]\n\n')
        file.write(f'\\def\\pn{{{problem_number:02}}}\n')
		
        if format_problem == 'BOOK':
            file.write(f'\\def\\book{{{format_problem}}}\n')
            file.write(f'\\def\\page{{{2022}}}\n')
        else:	
            file.write(f'\\def\\exam{{{format_problem}}}\n')
            file.write(f'\\def\\year{{{2022}}}\n')
        file.write(f'\\def\\gdrive{{Link}}\n\n')
        file.write(f'\\def\\question{{\nProblem\n}}\n')
        
        if format_problem == 'BOOK':
            assemble_book = assemble.replace('exam', 'book').replace('year', 'page')
            file.write(f'{assemble_book}')
        else:
            file.write(f'{option}\n')
            file.write(f'{assemble}')
        
        file.write(f'{diagram}\n')
        file.write(f'{qrcode}\n')
        file.write(f'\\end{{document}}\n')


    os.system(f'bat {main_tex}')
    click.pause()
    os.system(f'open -a texmaker {main_tex}')
    print('\n\topening texmaker ...\n')
    time.sleep(1)
    click.launch("https://drive.google.com/drive/u/5/folders/1-ICIUilvPsc8nkFskk4WWpvKB4vQ3QIV")



