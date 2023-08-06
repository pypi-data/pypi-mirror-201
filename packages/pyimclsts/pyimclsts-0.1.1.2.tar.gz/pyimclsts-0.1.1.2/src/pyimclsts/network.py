'''
    Contains classes that define the role this pyimc instance will perform and
    are intended to be used directly by the user or their abstraction layer

'''
import typing as _typing
import functools as _functools
import inspect as _inspect

import multiprocessing as _multiprocessing
import asyncio as _asyncio
import time as _time

import importlib.util as _import
import sys as _sys
import os as _os

import pyimclsts.core as core

module_name = 'pyimc_generated' # and folder name
location = _os.getcwd() + '/' + module_name + '/__init__.py'

spec = _import.spec_from_file_location(module_name, location)

_pg = _import.module_from_spec(spec)
_sys.modules[module_name] = _pg
spec.loader.exec_module(_pg)

def unpack(message : bytes, *, is_big_endian : bool, is_field_message : bool = False, fast_mode : bool = False) -> _pg._base_templates.IMC_message:
    '''Expects a serializable (= exactly long (header + fields + CRC)) string of bits, but may fail (returns None)
    if the string is invalid. 
    
    Fast mode skips all type checking performed by the descriptor by directly invoking the constructor.
    '''
    unpack_functions = core.unpack_functions_big if is_big_endian else core.unpack_functions_little
    cursor = 0
    
    if not is_field_message:
        # deserialize header
        (m, size) = unpack_functions['header'](message[cursor:])
        deserialized_header = _pg._base_templates.header_data(*m)
        cursor += size
        # Magic number 2 = CRC size in bytes
        contents = message[:-2]
        crc = unpack_functions['uint16_t'](message[-2:])[0]
        crc_valid = crc == core.CRC16IMB(contents)
    else:
        crc_valid = None
    
    # check CRC-16.
    if crc_valid or is_field_message:
        if is_field_message:
            msgid = unpack_functions['uint16_t'](message[cursor:cursor+2])[0]
            cursor += 2
        else:
            msgid = deserialized_header.mgid
            if msgid not in _pg.messages._message_ids:
                unknown_msg = _pg.messages.Unknown(msgid, contents = message[cursor:-2], endianess = is_big_endian)
                unknown_msg._header = deserialized_header
                return unknown_msg
        
        if fast_mode:
            # get corresponding class
            message_class = getattr(_pg.messages, _pg.messages._message_ids.get(msgid, None))

            fields = [(f, getattr(getattr(type(message_class()), f), '_field_def')['type']) for f in message_class()._Attributes.fields]
            arguments = dict()
            for field, t in fields:
                if t == 'message':
                    if unpack_functions['uint16_t'](message[cursor:cursor+2])[0] == 65535:
                        cursor += 2
                    else:
                        (m, size) = unpack(message[cursor:], is_big_endian=is_big_endian, is_field_message=True, fast_mode=fast_mode)
                        arguments[field] = m
                        cursor += size
                elif t == 'message-list':
                    (n, _) = unpack_functions['uint16_t'](message[cursor:])
                    cursor += 2
                    arguments[field] = []
                    for _ in range(n):
                        (m, size) = unpack(message[cursor:], is_big_endian=is_big_endian, is_field_message=True, fast_mode=fast_mode)
                        arguments[field].append(m)
                        cursor += size
                else:
                    (m, size) = unpack_functions[t](message[cursor:])
                    arguments[field] = m
                    cursor += size
            # instantiate class through constructor
            message_class = message_class(**arguments)
            
        else:
            # instantiate empty class
            message_class = getattr(_pg.messages, _pg.messages._message_ids.get(msgid, None))()

            # deserialize fields
            # make a (field, type) tuple list, get information in the descriptor
            fields = [(f, getattr(getattr(type(message_class), f), '_field_def')['type']) for f in message_class._Attributes.fields]
            for field, t in fields:
                if t == 'message':
                    if unpack_functions['uint16_t'](message[cursor:cursor+2])[0] == 65535:
                        cursor += 2
                    else:
                        (m, size) = unpack(message[cursor:], is_big_endian=is_big_endian, is_field_message=True, fast_mode=fast_mode)
                        cursor += size
                        setattr(message_class, field, m)
                elif t == 'message-list':
                    (n, _) = unpack_functions['uint16_t'](message[cursor:])
                    cursor += 2
                    message_list = []
                    for _ in range(n):
                        (m, size) = unpack(message[cursor:], is_big_endian=is_big_endian, is_field_message=True, fast_mode=fast_mode)
                        message_list.append(m)
                        cursor += size
                    setattr(message_class, field, message_list)
                else:
                    (m, size) = unpack_functions[t](message[cursor:])
                    cursor += size
                    setattr(message_class, field, m)
        
        if not is_field_message:
            message_class._header = deserialized_header
            return message_class
        else:
            return (message_class, cursor)
    return None

async def _async_wrapper(func, *args):
    return func(*args)

class base_IO_interface:
    '''
        An 'abstract'* class that describes the basic implementation of an I/O interface.

        * Not really abstract as in Java, but consider it so. 
        I will not use abc and its decorators.
    '''
    __slots__ = ['_input', '_output', '_o', '_i']

    def __init__(self, _input : any = None, _output : any = None) -> None:
        self._input = _input
        self._output = _output

    async def open(self) -> None:
        raise NotImplementedError
    
    async def read(self, n_bytes : int) -> bytes:
        raise NotImplementedError
        
    async def write(self, byte_string : bytes) -> None:
        raise NotImplementedError
    
    async def close(self) -> None:
        raise NotImplementedError

class file_interface(base_IO_interface):
    '''
        A minimal implemenation of a file interface. Receives an input
        file name and (optionally) an output file name, to which it appends.
    '''
    __slots__ = ['_input', '_output', '_o', '_i']

    def __init__(self, _input : any = None, _output : any = None) -> None:
        self._input = _input
        self._output = _output

    async def open(self) -> None:
        self._o = open(self._output, 'ab') if self._output is not None else None
        self._i = open(self._input, 'rb')
    
    async def read(self, n_bytes : int) -> bytes:
        r = self._i.read(n_bytes)
        if r == b'':
            raise EOFError('End of File reached')
        return r
        
    async def write(self, byte_string : bytes) -> None:
        if self._o is not None:
            self._o.write(byte_string)
    
    async def close(self) -> None:
        if self._o is not None:
            self._o.close()
        self._i.close()

class tcp_interface(base_IO_interface):
    '''
        A minimal implementation of a TPC interface. It wraps a
        connection established with the asyncio module.
    '''
    __slots__ = ['_ip', '_port', '_reader', '_writer']

    def __init__(self, ip : str, port : int) -> None:
        self._ip = ip
        self._port = port

    async def open(self) -> None:
        self._reader, self._writer = await _asyncio.open_connection(self._ip, self._port)
    
    async def read(self, n_bytes : int) -> bytes:
        r = await self._reader.read(n_bytes)
        if r == b'':
            raise EOFError('Connection returned empty byte string')
        return r
        
    async def write(self, byte_string : bytes) -> None:
        self._writer.write(byte_string)
        await self._writer.drain()
    
    async def close(self) -> None:
        self._writer.close()
        await self._writer.wait_closed()

class message_bus():
    '''
        Send and receives messages as bytes, but exposes them as IMC messages

        Receives a base_IO_interface, which must implement open(), read(), write() and close()
        asynchronous methods.

        Starts another process that continuously reads/writes to the base_IO_interface.
    '''

    __slots__ = ['_io_interface', '_timeout', '_child_end', '_parent_end', '_child_process', '_keep_running', '_big_endian']
    
    def __init__(self, IO_interface : base_IO_interface, timeout = 60, big_endian=False):
        super().__init__()

        self._io_interface = IO_interface
        self._timeout = timeout

        # mode to send messages
        self._big_endian = big_endian

    def _external_listener_loop(self, child_end, timeout : int, keep_running : _multiprocessing.Value):
        '''All code bellow is executed in a separate process.'''

        async def consume_output(io_interface : base_IO_interface):
            '''Continuously read the pipe end to send messages'''
            
            while keep_running.value:
                try:
                    has_message = child_end.poll()
                    while has_message:
                        message = child_end.recv_bytes()
                        await io_interface.write(message)
                        has_message = child_end.poll()
                finally:
                    pass
                # Yield an exit point to the event loop
                await _asyncio.sleep(0)
            
            print("Writer stream has been closed.")

        async def consume_input(io_interface : base_IO_interface):
            '''Continuously read the socket to deserialize messages'''

            buffer = bytearray()
            while keep_running.value:
                try:
                    # magic number: 6 = sync number + (msgid + msgsize) size in bytes
                    if len(buffer) < 6:
                        buffer += await io_interface.read(6 - len(buffer))

                    if int.from_bytes(buffer[:2], byteorder='little') == _pg._base_templates._sync_number:
                        # get msg size
                        size = int.from_bytes(buffer[4:6], byteorder='little')
                        # magic number: 22 = 20(header size) + 2(CRC) sizes in bytes.
                        read_size = max(size + 22 - len(buffer), 0)
                        buffer += await io_interface.read(read_size)

                        # Validate message, but do not unpack yet
                        unparsed_msg = bytes(buffer[:(size + 22)])
                        if core.CRC16IMB(unparsed_msg[:-2]) == int.from_bytes(unparsed_msg[-2:], byteorder='little'):
                            child_end.send_bytes(unparsed_msg)
                            # eliminate message from buffer
                            del buffer[:size + 22]
                        else:
                            # deserialization failed:
                            # sync number is not followed by a sound/valid message. Remove it from buffer
                            # to look for next message
                            del buffer[:2]
                    elif int.from_bytes(buffer[:2], byteorder='big') == _pg._base_templates._sync_number:
                        size = int.from_bytes(buffer[4:6], byteorder='big')
                        read_size = max(size + 22 - len(buffer), 0)
                        buffer += await io_interface.read(read_size)

                        unparsed_msg = bytes(buffer[:(size + 22)])
                        if core.CRC16IMB(unparsed_msg[:-2]) == int.from_bytes(unparsed_msg[-2:], byteorder='big'):
                            child_end.send_bytes(unparsed_msg)
                            del buffer[:size + 22]
                        else:
                            del buffer[:2]
                    else:
                        # buffer does not start with a sync number. Remove it to search
                        # for a valid sync number.
                        del buffer[:2]
                except EOFError as e:
                    print("EOF reached by the stream reader. Waiting for stream writer to finish...")
                    
                    # Unblock the main thread and send an empty byte string. 
                    # (-> signal EOF, so that it won't write anymore)
                    child_end.send_bytes(b'')

                    # Yield to the event loop to let stream writer finish 
                    await _asyncio.sleep(1.5)
                    
                    # Prevent further reads/writes in this process
                    with keep_running.get_lock():
                        keep_running.value = False
                finally:
                    pass
                
                # Yield an exit point to the event loop
                await _asyncio.sleep(0)
            print("Reader stream has been closed.")
        async def main_loop():
            await self._io_interface.open()
            try:
                await _asyncio.gather(consume_input(self._io_interface), consume_output(self._io_interface))
            finally:
                child_end.close()
                print('IO interface has been closed.')
                await self._io_interface.close()

        try:
            _asyncio.run(main_loop())
        except EOFError as e:
            print('No more bytes to read.')
        finally:
            with self._keep_running.get_lock():
                self._keep_running.value = False
            print('Message Bus has been closed.')

    def open(self):
        
        # Using a pipe to establish communication between processes
        self._parent_end, self._child_end = _multiprocessing.Pipe(duplex=True)

        self._keep_running = _multiprocessing.Value('i', True)

        # Start process
        self._child_process = _multiprocessing.Process(target=self._external_listener_loop, 
                                                        args=(self._child_end, self._timeout, self._keep_running))
        self._child_process.start()

        # It is very likely that the main process will run faster than the child process, which
        # may cause some undesirable behaviour, such as, the main process' context manager closes 
        # the connection before the child process' procedures can even start.
        # The naive solution: block the main thread for 0.5 second
        _time.sleep(0.5)
    
    def close(self, max_wait : float = 1) -> None:        
        with self._keep_running.get_lock():
            self._keep_running.value = False
        
        self._child_process.join()
        self._child_process.close()

    def send(self, message : _pg._base_templates.base_message, *, src : int = None, src_ent : int = None, 
                        dst : int = None, dst_ent : int = None) -> None:
        '''Wrapper around a queue (actually a pipe end).'''
        
        self._parent_end.send_bytes(message.pack(is_big_endian=self._big_endian, src = src, src_ent = src_ent, 
                        dst = dst, dst_ent = dst_ent))

    def recv(self) -> _pg._base_templates.base_message:
        '''Wrapper around a queue (actually a pipe end). Blocks until a message is available.
        The _external_listener_loop is supposed to send complete messages (as per multiprocessing 
        documentation).'''       
        msg = self._parent_end.recv_bytes()
        
        if msg == b'':
            raise EOFError('Message Bus has been closed.')
        else:
            if int.from_bytes(msg[:2], byteorder='big') == 0xFE54:
                msg = unpack(msg, is_big_endian=True, fast_mode=True)
            else:
                msg = unpack(msg, is_big_endian=False, fast_mode=True)
            return msg
            
    def poll(self, timeout : int = 0) -> bool:
        '''Extra function to check whether there are any available messages.
        Check _multiprocessing module pipes.
        '''
        return self._parent_end.poll(timeout=timeout)

    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()
        if exc_type == EOFError:
            print('Child process has been closed due to end of file.')
            return True
        print('Child process has been closed.')
        return None

class message_bus_st():
    '''
        Send and receives messages as bytes, but exposes them as IMC messages

        Receives a base_IO_interface, which must implement open(), read(), write() and close()
        asynchronous methods.

        DOES NOT start another process. Runs in the main process.
    '''

    __slots__ = ['_io_interface', '_timeout', '_writer_queue', '_reader_queue', '_keep_running', '_big_endian', '_task']
    
    def __init__(self, IO_interface : base_IO_interface, timeout = 60, big_endian=False):
        super().__init__()

        self._io_interface = IO_interface
        self._timeout = timeout

        # mode to send messages
        self._big_endian = big_endian

    async def open(self):
        self._keep_running = True

        self._writer_queue = _asyncio.Queue()
        self._reader_queue = _asyncio.Queue()

        async def consume_output(io_interface : base_IO_interface):
            '''Continuously read the pipe end to send messages'''
            
            while self._keep_running:
                try:
                    # flush queue or wait.
                    while not self._writer_queue.empty():
                        message = await self._writer_queue.get()
                        await io_interface.write(message)
                    else:
                        await _asyncio.sleep(0.5)
                finally:
                    pass
            
            print("Writer stream has been closed.")

        async def consume_input(io_interface : base_IO_interface):
            '''Continuously read the socket to deserialize messages'''
            
            buffer = bytearray()
            while self._keep_running:
                try:
                    # magic number: 6 = sync number + (msgid + msgsize) size in bytes
                    if len(buffer) < 6:
                        buffer += await io_interface.read(6 - len(buffer))

                    if int.from_bytes(buffer[:2], byteorder='little') == _pg._base_templates._sync_number:
                        # get msg size
                        size = int.from_bytes(buffer[4:6], byteorder='little')
                        # magic number: 22 = 20(header size) + 2(CRC) sizes in bytes.
                        read_size = max(size + 22 - len(buffer), 0)
                        buffer += await io_interface.read(read_size)

                        # Validate message, but do not unpack yet
                        unparsed_msg = bytes(buffer[:(size + 22)])
                        if core.CRC16IMB(unparsed_msg[:-2]) == int.from_bytes(unparsed_msg[-2:], byteorder='little'):
                            await self._reader_queue.put(unparsed_msg)
                            # eliminate message from buffer
                            del buffer[:size + 22]
                        else:
                            # deserialization failed:
                            # sync number is not followed by a sound/valid message. Remove it from buffer
                            # to look for next message
                            del buffer[:2]
                    elif int.from_bytes(buffer[:2], byteorder='big') == _pg._base_templates._sync_number:
                        size = int.from_bytes(buffer[4:6], byteorder='big')
                        read_size = max(size + 22 - len(buffer), 0)
                        buffer += await io_interface.read(read_size)

                        unparsed_msg = bytes(buffer[:(size + 22)])
                        if core.CRC16IMB(unparsed_msg[:-2]) == int.from_bytes(unparsed_msg[-2:], byteorder='big'):
                            await self._reader_queue.put(unparsed_msg)
                            del buffer[:size + 22]
                        else:
                            del buffer[:2]
                    else:
                        # buffer does not start with a sync number. Remove it to search
                        # for a valid sync number.
                        del buffer[:2]
                except EOFError as e:
                    print("EOF reached by the stream reader. Waiting for stream writer to finish...")
                    
                    # Unblock the main thread and send an empty byte string. 
                    # (-> signal EOF, so that it won't write anymore)
                    await self._reader_queue.put(b'')

                    # Yield to the event loop to let stream writer finish 
                    await _asyncio.sleep(1.5)
                    
                    # Prevent further reads/writes in this process
                    self._keep_running = False
                finally:
                    pass
                await _asyncio.sleep(0)
            print("Reader stream has been closed.")
        async def main_loop():
            await self._io_interface.open()
            try:
                await _asyncio.gather(consume_input(self._io_interface), consume_output(self._io_interface))
            finally:
                print('IO interface has been closed.')
                await self._io_interface.close()

        self._task = _asyncio.create_task(main_loop())
    
    def close(self, max_wait : float = 1) -> None:
        self._keep_running = False
        self._task.cancel()
        print('Message Bus has been closed.')

    def send(self, message : _pg._base_templates.base_message, *, src : int = None, src_ent : int = None, 
                        dst : int = None, dst_ent : int = None) -> None:
        '''Wrapper around a queue (actually a pipe end).'''
        
        # this looks dangerous (But it is an infinite queue)
        self._writer_queue.put_nowait(message.pack(is_big_endian=self._big_endian, src = src, src_ent = src_ent, 
                        dst = dst, dst_ent = dst_ent))

    async def recv(self) -> _pg._base_templates.base_message:
        '''Wrapper around a queue (actually a pipe end). Blocks until a message is available.
        The _external_listener_loop is supposed to send complete messages (as per multiprocessing 
        documentation).'''

        msg = await self._reader_queue.get()
        
        if msg == b'':
            raise EOFError('No more bytes to read.')
        else:
            if int.from_bytes(msg[:2], byteorder='big') == 0xFE54:
                msg = unpack(msg, is_big_endian=True, fast_mode=True)
            else:
                msg = unpack(msg, is_big_endian=False, fast_mode=True)
            return msg
            
    def poll(self, timeout : int = 0) -> bool:
        '''Extra function to check whether there are any available messages.
        '''
        return not self._reader_queue.empty()

    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()
        if exc_type == EOFError:
            print('Message bus event loop has been closed due to end of file.')
            return True
        print('Message bus event loop has been closed.')
        return None

class subscriber:

    __slots__ = ['msg_manager', '_subscriptions', '_subscripted_all', '_periodic', '_call_once', '_use_mp']

    def __init__(self, IO_interface : base_IO_interface, *,big_endian=False, use_mp = False) -> None:
        self._use_mp = use_mp
        if self._use_mp:
            self.msg_manager = message_bus(IO_interface, big_endian)
        else:
            self.msg_manager = message_bus_st(IO_interface, big_endian)
        self._subscriptions = dict()
        self._subscripted_all = []
        self._periodic = []
        self._call_once = []
    
    def _event_loop(self):

        async def periodic_wrapper_coro(_period : float, f : _typing.Callable, send_callback : _typing.Callable[[_pg._base_templates.IMC_message], None]):
            loop = _asyncio.get_running_loop()
            while True:
                last_exec = loop.time()
                await f(send_callback)
                now = loop.time()
                await _asyncio.sleep(max(last_exec - now + _period, 0))
                
        async def periodic_wrapper(_period : float, f : _typing.Callable, send_callback : _typing.Callable[[_pg._base_templates.IMC_message], None]):
            loop = _asyncio.get_running_loop()
            f(send_callback)
            while True:
                await _asyncio.sleep(_period)
                loop.call_later(_period, f, send_callback)

        async def main_loop():
            msg_mgr = self.msg_manager
            try:
                if self._use_mp:
                    msg_mgr.open()
                else:
                    await msg_mgr.open()
                loop = _asyncio.get_running_loop()

                for f, delay in self._call_once:
                    if delay is not None:
                        loop.call_later(delay, f, msg_mgr.send)
                    else:
                        f(msg_mgr.send)
                
                tasks = []
                for f, period in self._periodic:
                    if _inspect.iscoroutinefunction(f):
                        tasks.append(loop.create_task(periodic_wrapper_coro(period, f, msg_mgr.send)))
                    elif callable(f):
                        tasks.append(loop.create_task(periodic_wrapper(period, f, msg_mgr.send)))
                    else:
                        print(f'Warning: Given function {f} is neither _typing.Callable nor a coroutine.')

                while True:
                    msg = msg_mgr.recv() if self._use_mp else await msg_mgr.recv()
                    if msg._header.mgid in self._subscriptions:
                        for f in self._subscriptions[msg._header.mgid]:
                            await f(msg, msg_mgr.send)
                    
                    [f(msg, msg_mgr.send) for f in self._subscripted_all]
                    # Offer an exit point
                    await _asyncio.sleep(0)
            except EOFError:
                print('Stream has ended.')
            finally:
                msg_mgr.close()
        _asyncio.run(main_loop())

    def subscribe_async(self, msg_id : _typing.Union[int, _pg._base_templates.IMC_message], callback : _typing.Callable[[_pg._base_templates.IMC_message], None]):
        '''Appends the callback to the list of subscripted functions.
        
        The main loop calls the function and pass the message and a callback to send messages.
        The return value is discarded and the function must have exactly two parameters (the message and the callback)
        and must not have additional parameters, to avoid unintended behavior*.
        
        *Due to python's pass-by-assignment, the argument values are evaluated when a function is called.
        This means that even if we pass, say "x", to the .subscribe_async method and then try to
        pass "x" to the callback, we can only pass x's value at the moment .subscribe_async was called.
        This means that if we subscribe, for example, f(x) and somewhere a function g "updates" x, and then call
        f(x) again, f will be called with x's first value.
        This could be bypassed using mutable data structures, but let's not delve into that.

        Tip: If the original function really needs arguments, wrap it with _functools.partial.
        Tip2: Use a class instance to keep shared values across different calls. See followRef.py.
        '''
        key = None
        if isinstance(msg_id, _pg._base_templates.IMC_message):
            key = msg_id._Attributes.id
        elif isinstance(msg_id, int):
            key = msg_id
        elif _inspect.isclass(msg_id):
            if issubclass(msg_id, _pg._base_templates.IMC_message):
                key = msg_id()._Attributes.id
        else:
            print(f'Warning: Given message id {msg_id} is not a valid message.')
            
        if key is not None:
            c = None
            if _inspect.iscoroutinefunction(callback):
                c = callback
            elif callable(callback):
                c = _functools.partial(_async_wrapper, callback)
            else:
                print(f'Warning: Given function {callback} is neither callable nor a coroutine.')
            
            if c is not None:
                if self._subscriptions.get(key, None):
                    self._subscriptions[key].append(c)
                else:
                    self._subscriptions[key] = [c]

    def subscribe_all(self, callback : _typing.Callable[[_pg._base_templates.IMC_message], None]):
        '''Append to the list of callbacks that will be called to every *received* message
        
        The main loop calls the function and pass the message and a callback to send messages.
        The return value is discarded and the function must have exactly two parameters (the message and the callback)
        and must not have additional parameters, to avoid unintended behavior*.
        '''
        self._subscripted_all.append(callback)

    def periodic_async(self, callback : _typing.Callable[[_pg._base_templates.IMC_message], None], period = float):
        '''Add callback to a list to be called every period seconds. Function must take
        a send callback as parameter. This callback can be used to send messages.'''
        self._periodic.append((callback, period))

    def subscribe_mp(self, msg_id : _typing.Union[int, _pg._base_templates.IMC_message], callback : _typing.Callable[[_pg._base_templates.IMC_message], None]):
        '''Calls a function and pass the message and a callback to send messages to it.
        Runs the given callback in a different process and should be used only with heavy load
        functions.
        '''
        raise NotImplemented

    def call_once(self, callback : _typing.Callable[[_typing.Callable[[_pg._base_templates.IMC_message], None]], None], delay : float = None):
        '''Calls the given callbacks as soon as the main loop starts or according to their delay in seconds.
        Callback parameters must be exactly one callback (that can be used to send messages).'''
        self._call_once.append((callback, delay))

    def run(self):
        self._event_loop()

if __name__ == '__main__':

    io_interface = tcp_interface('localhost', 6006)
    f_interface = file_interface('Data.lsf', 'output_test.lsf')
    
    s = subscriber(io_interface, big_endian=False)
    s.subscribe_all(lambda x, y : print(x))
    #s.subscribe_async(_pg.messages.EstimatedState, lambda x, y : print('oi'))

    s.call_once(lambda _: print("hi"))
    s.call_once(lambda _: print("hi2"), 1)

    #s.periodic_async(lambda _ : print('oi'), 1)
    #s.periodic_async(x, 2)
    s.run()