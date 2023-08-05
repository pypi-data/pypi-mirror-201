import ast
import json
import nbformat
import re
import textwrap

class JupyterToLib:
  def ipynb_to_py(self, ipynb_path, py_path):
    with open(ipynb_path, 'r') as f:
      nb = json.load(f)
    pattern_func = re.compile(r'^def\s\w+\(.*\):', re.MULTILINE)
    pattern_import = re.compile(r'^from\s.+?\simport\s.+', re.MULTILINE)
    functions = []
    imports = []
    for cell in nb['cells']:
      if cell['cell_type'] == 'code' and cell['source']:
        source = ''.join(cell['source'])
        source = source.strip()
        if pattern_func.search(source):
          functions.append(source)
        elif pattern_import.search(source):
          imports.append(source)
    with open(py_path, 'w') as f:
      for imp in imports:
        f.write(imp + '\n')
      f.write('\n')
      for func in functions:
        f.write(func + '\n')
  
  def remove_comments_and_empty_lines(self, file_path):
    with open(file_path, 'r') as f:
      content = f.read()
    pattern_comment = r"(^|[^'\"#])#[^\n]*"# Expresión regular para encontrar comentarios
    pattern_empty = r'^\s*$' 
    content = re.sub(pattern_comment, '', content, flags=re.MULTILINE) 
    content = re.sub(pattern_empty, '', content, flags=re.MULTILINE) 
    pattern_keep = r'^(def|\t|\s|from|import)' 
    lines = content.split('\n')
    content = '\n'.join([line for line in lines if re.search(pattern_keep, line)])
    with open(file_path, 'w') as f:
      f.write(content)
  
  def sort_imports(self, file_path):
    with open(file_path, 'r') as f:
      content = f.read()
    pattern_from = r'^\s*from\s+\S+\s+import\s+.+'
    pattern_import = r'^\s*import\s+.+'
    imports_from = []
    imports_import = []
    rest = []
    for line in content.split('\n'):
      if re.match(pattern_from, line):
        imports_from.append(line)
      elif re.match(pattern_import, line):
        imports_import.append(line)
      else:
        rest.append(line)
    imports_from = sorted(list(set(imports_from)))
    imports_import = sorted(list(set(imports_import)))
    imports_from = '\n'.join(imports_from)
    imports_import = '\n'.join(imports_import)
    rest = '\n'.join(rest)
    content = f"{imports_from}\n{imports_import}\n\n{rest}"
    with open(file_path, 'w') as f:
      f.write(content)
  
  def obtener_nombres_funciones(self, funciones):
    nombres_funciones = {}
    for funcion in funciones:
      nombre = re.search(r'def\s+([a-zA-Z_][a-zA-Z_0-9]*)\s*\(', funcion)
      if nombre:
        nombres_funciones[nombre.group(1)] = funcion
    return nombres_funciones
  
  def add_self_to_functions(self, funciones_):
    for key, value in funciones_.items():
      if value.startswith("def"):
        lines = value.split("\n")
        first_line = lines[0]
        args = re.search(r"def (\w+)\((.*)\):", first_line)
        if args:
          func_name = args.group(1)
          new_args = "self, " + args.group(2)
          lines[0] = f"def {func_name}({new_args}):"
          for i in range(1, len(lines)):
            match = re.search(r"(\W)(\w+(?=\())", lines[i])
            if match and match.group(2) in funciones_.keys():
              lines[i] = re.sub(rf"(\W){match.group(2)}\(", rf"\1self.{match.group(2)}(", lines[i])
          funciones_[key] = "\n".join(lines)
    return funciones_
  
  def extract_libraries(self, string, filename='requirements.txt'):
    libraries = set()
    parsed = ast.parse(string)
    for node in parsed.body:
      if isinstance(node, ast.Import):
        for alias in node.names:
          libraries.add(alias.name)
      elif isinstance(node, ast.ImportFrom):
        libraries.add(node.module)
    with open(filename, 'w') as f:
      for library in libraries:
        f.write(library + '\n')
  
  def add_class_and_indent(self, string, class_name):
    new_string = f"class {class_name}:\n"
    lines = string.split("\n")
    for line in lines:
      new_string += "  " + line + "\n"
    return new_string
  
  def convert_indentation(self, function_str, ident=2):
    lines = function_str.split('\n')
    ident_len = ' '*ident
    primer_linea_def  = min([i for i, x in enumerate(lines) if 'def' in x])
    indentation = ''
    for line in lines[(primer_linea_def+1):]:
      if line.strip():
        indentation = line[:len(line)-len(line.lstrip())]
        break
    new_lines = []
    for line in lines:
      if line.startswith(indentation):
        line = line.replace(indentation,ident_len)
      new_lines.append(line)
    return '\n'.join(new_lines)
  
  def convert_file_indentation(self, file_path, requirements, ident):
    with open(file_path, 'r') as f:
      file_str = f.read()
    lines = file_str.split('\n')
    primer_linea_def  = min([i for i, x in enumerate(lines) if 'def' in x])
    importaciones_str = '\n'.join(lines[0:primer_linea_def])
    function_starts = [i for i in range(len(lines)) if re.match(r'def .*\):', lines[i])]
    function_ends = function_starts[1:] + [len(lines)]
    functions = [lines[function_starts[i]:function_ends[i]] for i in range(len(function_starts))]
    funciones = ['\n'.join(f) for f in functions]
    funs_dict = self.obtener_nombres_funciones(funciones)
    funs_dict = self.add_self_to_functions(funs_dict)
    functions = [x for x in funs_dict.values()]
    new_functions = []
    for i, function in enumerate(functions):
      new_function = self.convert_indentation(function, ident)
      new_functions.append(new_function)
    funciones_unidas_ = '\n\n'.join(new_functions)
    funciones_unidas = self.add_class_and_indent(funciones_unidas_,'mi_clase')

    new_file_str = importaciones_str + '\n' + funciones_unidas
    req_path = '/'.join(file_path.split('/')[:-1])+'/requirements.txt'
    if requirements:
      new_var = req_path
      self.extract_libraries(importaciones_str,new_var)
    with open(file_path, 'w') as f:
      f.write(new_file_str)
  
  def ProcessLib(self, nb_file, nb_file2, verbose = True, get_req=True, ident=4):
    if verbose:
      print('Generando archivo py')
    self.ipynb_to_py(nb_file,nb_file2)
    if verbose:
      print('Extrayendo funciones y librerías')
    self.remove_comments_and_empty_lines(nb_file2)
    if verbose:
      print('Ordenando contenido')
    self.sort_imports(nb_file2)
    if verbose:
      print('Homologando identación y generando requierimientos')
    self.convert_file_indentation(nb_file2,get_req, ident)
