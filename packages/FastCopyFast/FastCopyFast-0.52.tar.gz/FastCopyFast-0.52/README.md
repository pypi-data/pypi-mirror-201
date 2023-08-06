Three functions to copy/move files faster with Python:

Based on this answer: https://stackoverflow.com/a/28129677/15096247

```python
pip install FastCopyFast
```

```python
copyfile(src: str, dst: str, copystat: bool = True) -> bool

movefile(src: str, dst: str, copystat: bool = True) -> bool

copytree(  
src: str, dst: str, ignore: Union[list, type(None)] = None, symlinks: bool = False  
)
```

```python
from FastCopyFast import copyfile,movefile,copytree

copyfile(r"F:\2020-12-02 15-35-25.mp4", r'c:\videoxxxxxxxxxxxx.mp4')
Out[3]: True

copyfile(r"F:\2020-12-02 15-35-25.mp4", r'c:\videoxxxxxxxxxxxx.mp4', copystat=False)
Out[4]: True

copyfile(r"F:\2020-12-02 15-35-25.mp4", r'c:\videoxxxxxxxxxxx2x.mp4', copystat=False)
Out[5]: True

movefile(r"C:\videoxxxxxxxxxxxx.mp4",r'c:\videoxxxxxxxxxxxxaaaaaa.mp4' , copystat=False)
Out[7]: True

movefile(r"c:\videoxxxxxxxxxxxxaaaaaa.mp4",r'c:\videoxxaavvvvbbbxxxxxxxxxxaaaaaa.mp4' , copystat=True)
Out[8]: True

copytree(r"F:\GUTENBERGNEU2", 'c:\\testcopytree', ignore=None,symlinks=False)
```
