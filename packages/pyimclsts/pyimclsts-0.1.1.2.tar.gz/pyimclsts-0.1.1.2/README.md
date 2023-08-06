## PyIMCtrans

This tool reads the IMC schema from a XML file, locally creates files containing the messages and connects (imports) the main global machinery.

See `/example` to check an example implementation of the Follow Reference maneuver.

### End-User
- Fancying a virtual env? (Not needed. Just in case you want to isolate it from your python setup)
```shell
$ sudo apt install python3.8-venv
$ python3 -m venv tutorial_env
$ source tutorial_env/bin/activate
```
- To use:
```shell
$ pip3 install pyimclsts
$ # or, if you are cloning the repo, from the folder pyproject.toml is located:
$ pip3 install .
```
- Choose a folder and have a version of the IMC schema. Otherwise, it will fetch the latest IMC version from the LSTS git repository. Extract messages locally, with:
```shell
$ python3 -m pyimclsts.extract
```
Check how to provide a black- or whitelist using:
```shell
$ python3 -m pyimclsts.extract --help
```
This will locally extract the IMC.xml as python classes. You will see a folder called `pyimc_generated` which contains base messages, bitfields and enumerations from the IMC.xml file. They can be locally loaded using, for example:
```python
import pyimc_generated as pg
```
In the top-level module, you will find some functions to allow you to connect to a vehicle and subscribe to messages, namely, a subscriber class.
```python
import pyimclsts.network as n

conn = n.tcp_interface('localhost', 6006)
sub = n.subscriber(conn)

# for example:
sub.subscribe_async(pg.messages.Announce, myfunction)
```
Check `/example` for further details.

### Change log:
#### Version 0.1.1.2
    - Parse command line arguments when pyimclsts.extract is called
        - Accept a black- or whitelist
        - Add minimal message list
    - [EXPERIMENTAL] Add the option to use asyncio or multiprocessing when using the subscriber
        - It's not clear-cut yet which approach is better, so both are provided until one proves to be superior

#### Version 0.1.1.1
    - Fix `Unknown message` being used for all messages
    - Fix string (IMC plaintext) decode/encode
    - Fix blocked termination when reading file

#### Version 0.1.1
    - Handle lost TCP connection/End of file:
        - Gracefully terminates, if EOF (or equivalent) is encountered.
    - Added a .subscribe_all() function.
    - Added MIT License
    - On extract, downloads IMC.xml definition from main git repository, when none is found.
    - Added an 'Unknown message', used when a message with valid sync number and valid crc but unknown id is received.
    - Update pyproject.toml
        - Corrected version
        - Added license
        - Added keywords

### Current TODO list:
    - Improve README
        - Add a description of the general functioning of the tool.
    - Implement a message whitelist
        - Although it works without problems, it is a little cumbersome to have +300 available messages.
    - Implement logging?
        - In the subscriber, message bus or the IO Interface?

    - Notes:
    - Users MUST be warned (documentation?) that the constructor does not type check, because the other operations (serialization) may fail if not correctly used. However, failure by type checking or failure by serialization is ultimately a failure during runtime, which begs the question: How to avoid a runtime error?
    - Currently using IntFlag to make bitfields. It works, but does not throw exceptions when using an invalid combination of flags.
        - Should it throw errors in this case?
    