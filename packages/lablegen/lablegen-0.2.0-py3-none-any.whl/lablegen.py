__version__ = "0.2.0"
__author__ = "Social Mean"



import pyperclip

def table_generator(dic, clip=False):
    col_count = len(dic)
    row_count = len(dic[list(dic.keys())[0]])
    
    latex_table_str = """\\begin{table}[H]
\\centering
\\begin{tabular}{""" + "c" * col_count + """}
\\hline\n"""
    
    for key in dic:
        latex_table_str += key + " &"
    latex_table_str = latex_table_str[0:-1]
    latex_table_str += """\\\\
\\hline\n"""
    for i in range(row_count):
        for key in dic:
            latex_table_str += str(dic[key][i]) + " &"
        latex_table_str = latex_table_str[0:-1]
        latex_table_str += "\\\\\n"
    
    
    latex_table_str += """\\hline
\\end{tabular}
\\caption{}
\\label{}
\\end{table}"""

    if clip:
        pyperclip.copy(latex_table_str)

    return latex_table_str