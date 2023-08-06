# chainstream

Chainstream provides the class `ChainStream`, a subclass of `io.RawIOBase`,
to chain I/O streams together into a single stream. See below for example
usage, and the module help for more information.

Chainstream is distributed under the CC-BY-SA version 4.0; see
https://creativecommons.org/licenses/by-sa/4.0/

## Example

```
from chainstream import ChainStream

def generate_open_file_streams():
    for file in filenames:
        yield open(file, 'rb')
f = io.BufferedReader(ChainStream(generate_open_file_streams()))
f.read()
```
