import os
import IPython
def install(x):
    d = IPython.paths.get_ipython_dir()
    d = d+'/profile_default/startup'
    os.chdir(d )
    Load_package  = '# Importing basic Functions\nimport os\nimport warnings\nwarnings.filterwarnings(\'ignore\')\nimport matplotlib.pyplot as plt\nimport pandas as pd\nfrom oauth2client.service_account import ServiceAccountCredentials\nimport pandas_gbq\nimport time\nimport requests\nimport json\nimport math\nimport datetime\nimport re\n\ndef find_all(x,y) :\n    return [i.start() for i in re.finditer(x,y)]\ndef par_to_str(par_to_str_VAR_56431):\n    if type(eval(par_to_str_VAR_56431) )== str :\n        return  "\'" + eval(par_to_str_VAR_56431) + "\'"\n    elif type(eval(par_to_str_VAR_56431) )== list :\n        return  "(" + str(eval(par_to_str_VAR_56431))[1:-1] + ")"\n    else :\n        return eval(par_to_str_VAR_56431)\ndef par_replace(y):\n    y = re.sub(\'\\n\',\' \\n\',y)\n    for i in find_all(\'@\',y):\n        i = find_all(\'@\',y)[0]\n        y = y[0:i] + str(par_to_str(y[i+1 :i+re.search(\' \',y[i:]).start() ])) + y[i+re.search(\' \',y[i:]).start() : ]\n    return(y)\n'
    with open('01_Load_package.ipy','w') as file:
        file.write(Load_package)
    Magic = '#Magic Creation\nfrom IPython.core.magic import register_cell_magic\nfrom IPython.core.magic_arguments import (argument, magic_arguments,parse_argstring)\n@magic_arguments()\n@argument(\'-save_to\', \'--option\', help=\'Save as data \')\n@argument(\'-job\', \'--job\', help=\'if the query needs to be run as a job or not\')\n@argument(\'-para\', \'--para\', help=\'if the query needs to be run as a job or not\')\n@register_cell_magic\ndef BQSQL(line, cell):\n    args = parse_argstring(BQSQL, line)\n    if cell.strip()[-1] != \';\':\n        x = cell + \';\'\n    else :\n        x = cell\n    if args.job == \'Y\' :\n        x = x + "SELECT \'JOB RUN SUCCESS\' ;"\n    if args.para == \'Y\':\n        x = par_replace(x)\n    if args.option == None :\n        if args.job == \'Y\':\n            return pd.read_gbq(x, project_id = \'GBQ_DIR\', dialect = \'standard\' ).iloc[0,0]\n        else :\n            return pd.read_gbq(x, project_id = \'GBQ_DIR\', dialect = \'standard\' )\n    else :\n        globals()[args.option] = pd.read_gbq(x, project_id = \'GBQ_DIR\', dialect = \'standard\' )\n        print("Data has been successfully writen to " + args.option )\n'
    Magic = Magic.replace('GBQ_DIR',x)
    with open('02_Load_Magic.ipy','w') as file:
        file.write(Magic)
