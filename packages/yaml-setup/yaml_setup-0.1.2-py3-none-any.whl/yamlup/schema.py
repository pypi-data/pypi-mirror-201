from schema import Schema, And, Or, Optional, Literal, Regex, Use
from enum import Enum
from typing import List, Callable, Union, Any
import json
import yaml
import sys
from copy import deepcopy
from itertools import cycle, product

from textwrap import wrap
from pathlib import Path
from rich.console import Console

cout = Console()
cerr = Console(stderr=True)

isLiteral = lambda x: not isinstance(x, (list, dict))
isArray = lambda x: isinstance(x, list)
isDict = lambda x: isinstance(x,dict)

__all__ = [
    "SetupFile",
    "SetupBase",
    "cerr", "cout"
]

def dictFind(
        key:str, dictlike,
        visited:List[str] = None,
        depth: int = 0,
        condition : Callable[[str, dict],bool] = None,
        debug:bool = False,
        exclude: List[str] = None,
    ):
    visited = visited or []
    exclude = exclude or []

    result = {'found': False}
    if not condition:
        def _condition(k,v):
            if debug:
                fmtv = v.values() if isDict(v) else v
                cout.log(f"Query-Key (if any): {key} | Key: {k} | Value: {fmtv} | Condition? {k == key}")
            return k == key
    elif debug:
        def _condition(k,v):
            result = condition(k,v)
            if debug:
                fmtv = v.values() if isDict(v) else v
                cout.log(f"Query-Key (if any): {key} | Key: {k} | Value: {fmtv} | Condition? {result}")
            return result
    else:
        _condition = condition


    for k,v in dictlike.items():
        if not _condition(k,v):
            if isDict(v):
                visited += [k]
                result = dictFind(key, v, visited=visited, depth=depth+1, condition=_condition, exclude=exclude)
                if result['found']:
                    if not depth:
                        del result['found']
                    return result
        elif k not in exclude:
            return {
                    'visited':visited,
                    'key': k,
                    'content': v,
                    'depth': depth,
                    'found': True
                }
        
    
    if not result['found'] and not depth:
        return {'visited':visited, 'found':False}
    elif not result['found']:
        return {'visited':visited, 'found':False}
    else:
        raise ValueError
    
def dictFindAll(key, dictlike: dict, results = None, prefix=''):
    results = results or {}

    for dkey, dvalue in dictlike.items():
        if dkey == key:
            results[f"{prefix}{dkey}"] = dvalue
        
        if isDict(dvalue):
            prefix = dkey + '.'
            results |= dictFindAll(key, dvalue, results=results, prefix=prefix)
        elif isArray(dvalue):
            for v in dvalue:
                if isDict(v):
                    prefix = dkey + '.'
                    results |= dictFindAll(key, dictlike, results=results, prefix=prefix)

    return results

def findAll(key, dictlike):
    res = dictFindAll(key, dictlike)
    results = []
    for k, v in res.items():
        name = k.replace(f".{key}", "")
        results += [{
            "key": key,
            "location": name,
            "value": v
        }]
    return results



    
def allkeys(nested: dict, seen: list = None):
    seen = seen or []
    if isArray(nested):
        for v in nested:
            if isDict(v):
                seen += allkeys(v, seen=seen)

    elif isDict(nested):
        layers = []
        for k,v in nested.items():
            seen += [k]        
            if isDict(v):
                layers += [v]
        
        for v in layers:
            seen += allkeys(v, seen=seen)
    
    return list(set(seen))
        
def dfilter(condition, nested):
    filtered = {}
    for (key, value) in filter(lambda kv: condition(kv[0], kv[1]), nested.items()):
        if isDict(value):
            filtered[key] = dfilter(condition, value)
        else:
            filtered[key] = value
    return filtered

class SetupBase(Schema):
    _setup_loaded: bool = False
    _data: dict = {}
    def __call__(self, data: Union[str, Path, dict]):
        if not isDict(data):
            self.path = validatePath(data)
            data = reader(self.path)
            self._data = self.validate(data)
            self._setup_loaded = True
        else:
            self._data = self.validate(data)
            self.path = Path().cwd() / 'setup.yml'
        return self
        
    def get(self, *args, **kwargs):
        return self._data.get(*args, **kwargs)
    
    def find(self, key:str, debug:bool = False):
        return dictFind(key, self._data, debug=debug)
    
    def all(self, key:str):
        return findAll(key, self._data)

    def findByType(self, T : type):
        def condition(key, dictlike):
            return key in dictlike and isinstance(dictlike[key], T)
        
        return dictFindAll("", self._data, condition=condition)
    
    def save(self):
        writer(self._data, self.path)

    def __str__(self) -> str:
        return str(self._data)
    
    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()
    
    def items(self):
        return self._data.items()
    
    def tasks(self):
        return list(self._data.keys())

    def task_items_lazy(self, task:str):
        if task in self._data:
            tk = self._data[task]
            for item in tk['items']:
                yield {"name": item, **{k:v for k,v in tk['items'][item].items()}}
        else:
            yield {}

    def task_items(self, task:str, lazy=False):
        if lazy:
            return self.task_items_lazy(task)
        else:
            return list(self.task_items_lazy(task))
        
    def run_order(self,task):
        if task in self._data:
            tk = self._data[task]
            if 'run' in tk:
                return tk['run']['steps']
            else:
                cerr.print(f'❓Error | [green]Task: {task} was found[/green] | [yellow] But no `run` list declared.', style="bold red")
        else:
            cerr.print(f'❌ Could not find task: [yellow]{task}[/yellow]', style="bold red")
    
    def asArray(self, key):
        nestedArray = findAll(key, self._data)
        array = []

        for row in nestedArray:
            if isArray(row['value']):
                base = {k: v if not isArray(v) else v.pop() for k,v in row.items() if k != 'value'}
                for i,v in enumerate(row['value']):
                    if isArray(v):
                        for j, sv in enumerate(v):
                            arr = deepcopy(base)
                            arr['value'] = sv
                            arr['index'] = i+j
                            array += [arr]
                    else:
                        arr = deepcopy(base)
                        arr['value'] = v
                        arr['index'] = i
                        array += [arr]
            else:
               base = deepcopy(row) 
               base['index'] = None
               array += [base]
        return array
    
    def render(self, refs:List[str] = ["run"]):
        condition = lambda k,v : (k not in refs and not isArray(v)) or isDict(v)

        data = self._data
                
        
        content = '# High level description of the setup\n\n'

        header = '##'
        for key in data:
            content += header + f" Setup task group: {key}\n\n"
            header += "#"
            if 'description' in data[key]:
                content += data[key]['description'] + '\n\n'
            elif 'run' in data[key]:
                pass
            for item in data[key]['items']:
                content += header + f" Setup item: {item}\n\n"
                tp, pr, ar, ap = [data[key]['items'][item][k] for k in ['type', 'priority', 'admin', 'append-to-profile'] ]
                ap = True if ap else False
                content += '|Type|Priority|Admin Rights|Content to append to PATH|\n'
                content += '|:-:|:-:|:-:|:--|\n'
                content += f'|{tp}|{pr}|{ar}|{ap}|\n\n'

                if 'description' in data[key]['items'][item]:
                    content += header + '#' + ' Description:' + '\n\n'
                    content += data[key]['items'][item]['description'] + '\n\n'

                if 'commands' in data[key]['items'][item]:
                    content += '\n```powershell\n'
                    content += '\n'.join(data[key]['items'][item]['commands']) + '\n'
                    content += "```\n\n"

        return content

    
    def __rich__(self):
        colors = cycle(["red", "yellow", "pink", "pink2"])

        return json.dumps(applyColors(self._data), indent=4)

def applyColors(dictlike, colors=None):
    colors = colors or cycle(["red", "yellow", "pink", "pink2"])
    if isArray(dictlike):
        c = next(colors)
        return [f"[{c}]{v}[/{c}]" for v in dictlike]
    else:
        c = next(colors)
        return {
            f"[bold {c}]{k}[/bold {c}]": f"[dim {c}]{v}[/dim {c}]" if isLiteral(v) else applyColors(v, colors=colors)
            for k,v in dictlike.items()
        }

def flatten(nested: dict, sep:str = '.', prefix: str = ''):
    _sep = sep if prefix else ''
    processed = {}
    for key, value in nested.items():
        if isLiteral(value):
            processed[f"{prefix}{_sep}{key}"] = value
        elif isArray(value):
            for i, v in enumerate(value):
                if isLiteral(v):
                    processed[f"{prefix}{_sep}{key}{sep}{i}"] = v
                else:
                    processed |= flatten(v, sep=sep, prefix=f"{prefix}{_sep}{key}{sep}{i}")
            
        else:
            processed |= flatten(value, sep=sep, prefix=f"{prefix}{_sep}{key}")
    return processed

def validatePath(path: Path):
    if (
        Path(path).exists() and
        (
            set(Path(path).suffixes) &
            {'.json', '.yaml', '.yml'}
        )
    ):
        return Path(path)
    else:
        return False
    

def reader(path:Path):
    if path := validatePath(path):
        if path.suffix.endswith(".json"):
            return json.load(path.open())
        elif len(set(path.suffixes) & {'.yml', '.yaml'}):
            return yaml.safe_load(path.open())
        else:
            cerr.print(f"❌ Invalid extension: [yellow]{path}", style="bold red")
            sys.exit(1)
    else:
        cerr.print(f"❌ Invalid extension: [yellow]{path}", style="bold red")
        sys.exit(1)
    
def writer(data: dict, path:Path):
    if path := validatePath(path):
        if path.suffix.endswith(".json"):
            json.dump(data, path.open("w+"))
        elif len(set(path.suffixes) & {'.yml', '.yaml'}):
            yaml.safe_dump(data, path.open("w+"))
        elif path.suffix.endswith(".md"):
            raise NotImplementedError("A future serializer will handle this tasks")
    else:
        cerr.log(f"❓Path not valid, 👉 writing to {Path().cwd()/'README.md'} instead.")
        yaml.safe_dump(data, Path().cwd() / 'README.md')




class Priorities(Enum):
    Critical = "critical"
    Highest = "highest"
    High = "high"
    Important = "important"
    Required = "required"
    Medium = "medium"
    Low = "low"
    NiceToHave = "nice-to-have"
    Optional = "optional"
    Preferable = "preferable"
    Useful = "useful"
    CRITICAL = "0"
    HIGHEST = "1"
    HIGH = "2"
    IMPORTANT = "3"
    REQUIRED = "4"
    MEDIUM = "5"
    LOW = "6"
    NICETOHAVE = "7"
    OPTIONAL = "8"
    PREFERABLE = "9"
    USEFUL = "10"
    

    @staticmethod
    def all():
        return set(p.value for p in Priorities) | set(p.name for p in Priorities)

SetupFile = SetupBase({
    str : {
        Optional(
            "description",
            default="The setup creator has not given a description to this task"
        ) : str,
        "items": {
            str: {
                "priority": And(Use(str), lambda t: str(t).lower() in Priorities.all()),
                Optional(
                    "description",
                    default="The setup creator has not given a description to this package/software"
                ) : str,
                Optional(
                    "type",
                    default="Package",
                ): str,
                Optional(
                    "append-to-profile",
                    default="",
                ): str,
                Optional(
                    "admin",
                    default=False,
                ): bool,
                "commands":
                    And(Use(lambda o: [o] if not isinstance(o, list) else o), lambda cmds: all( isinstance(c, str) for c in cmds) )
            },
            
        },
        "run" : {
            Optional(
                    "description",
                    default="The setup creator has not given a description to this run configuration"
                ) : str,
            "steps": And(Use(list), lambda cmds: all( isinstance(c, str) for c in cmds) )
        }
    }
})