

This is an analsis about some source code which creates lists and a possible alternative syntax. 
You can find [here](https://discuss.python.org/t/conditional-elements-arguments/26567/1) more information.

The source files for this analysis where taken from `sys.base_prefix`.

111 pattern can be transformed to the new syntax.

for reference: there are 2053 list comprehensions in the code.

The following transformations are sorted by the number of conditions.




## python3.11/http/cookiejar.py:1837
current syntax:
``` python
h = [(cookie.name, cookie.value),
     ("path", cookie.path),
     ("domain", cookie.domain)]
if cookie.port is not None: h.append(("port", cookie.port))
if cookie.path_specified: h.append(("path_spec", None))
if cookie.port_specified: h.append(("port_spec", None))
if cookie.domain_initial_dot: h.append(("domain_dot", None))
if cookie.secure: h.append(("secure", None))
if cookie.expires: h.append(("expires",
                           time2isoz(float(cookie.expires))))
if cookie.discard: h.append(("discard", None))
if cookie.comment: h.append(("comment", cookie.comment))
if cookie.comment_url: h.append(("commenturl", cookie.comment_url))
```

new syntax:
``` python
h=[
    (cookie.name, cookie.value),
    ('path', cookie.path),
    ('domain', cookie.domain),
    ('port', cookie.port) if cookie.port is not None,
    ('path_spec', None) if cookie.path_specified,
    ('port_spec', None) if cookie.port_specified,
    ('domain_dot', None) if cookie.domain_initial_dot,
    ('secure', None) if cookie.secure,
    ('expires', time2isoz(float(cookie.expires))) if cookie.expires,
    ('discard', None) if cookie.discard,
    ('comment', cookie.comment) if cookie.comment,
    ('commenturl', cookie.comment_url) if cookie.comment_url,
]
```


## python3.11/tkinter/__init__.py:3875
current syntax:
``` python
args = [self._w, 'search']
if forwards: args.append('-forwards')
if backwards: args.append('-backwards')
if exact: args.append('-exact')
if regexp: args.append('-regexp')
if nocase: args.append('-nocase')
if elide: args.append('-elide')
if count: args.append('-count'); args.append(count)
if pattern and pattern[0] == '-': args.append('--')
args.append(pattern)
args.append(index)
if stopindex: args.append(stopindex)
```

new syntax:
``` python
args=[
    self._w,
    'search',
    '-forwards' if forwards,
    '-backwards' if backwards,
    '-exact' if exact,
    '-regexp' if regexp,
    '-nocase' if nocase,
    '-elide' if elide,
    *['-count', count] if count,
    '--' if pattern and pattern[0] == '-',
    pattern,
    index,
    stopindex if stopindex,
]
```


## python3.11/asyncio/streams.py:422
current syntax:
``` python
info = ['StreamReader']
if self._buffer:
    info.append(f'{len(self._buffer)} bytes')
if self._eof:
    info.append('eof')
if self._limit != _DEFAULT_LIMIT:
    info.append(f'limit={self._limit}')
if self._waiter:
    info.append(f'waiter={self._waiter!r}')
if self._exception:
    info.append(f'exception={self._exception!r}')
if self._transport:
    info.append(f'transport={self._transport!r}')
if self._paused:
    info.append('paused')
```

new syntax:
``` python
info=[
    'StreamReader',
    f'{len(self._buffer)} bytes' if self._buffer,
    'eof' if self._eof,
    f'limit={self._limit}' if self._limit != _DEFAULT_LIMIT,
    f'waiter={self._waiter!r}' if self._waiter,
    f'exception={self._exception!r}' if self._exception,
    f'transport={self._transport!r}' if self._transport,
    'paused' if self._paused,
]
```


## python3.11/site-packages/pip/_vendor/pygments/formatters/rtf.py:125
current syntax:
``` python
buf = []
if style['bgcolor']:
    buf.append('\\cb%d' % color_mapping[style['bgcolor']])
if style['color']:
    buf.append('\\cf%d' % color_mapping[style['color']])
if style['bold']:
    buf.append('\\b')
if style['italic']:
    buf.append('\\i')
if style['underline']:
    buf.append('\\ul')
if style['border']:
    buf.append('\\chbrdr\\chcfpat%d' %
               color_mapping[style['border']])
```

new syntax:
``` python
buf=[
    '\\cb%d' % color_mapping[style['bgcolor']] if style['bgcolor'],
    '\\cf%d' % color_mapping[style['color']] if style['color'],
    '\\b' if style['bold'],
    '\\i' if style['italic'],
    '\\ul' if style['underline'],
    '\\chbrdr\\chcfpat%d' % color_mapping[style['border']] if style['border'],
]
```


## python3.11/site-packages/pkg_resources/_vendor/packaging/utils.py:52
current syntax:
``` python
parts = []

# Epoch
if parsed.epoch != 0:
    parts.append(f"{parsed.epoch}!")

# Release segment
# NB: This strips trailing '.0's to normalize
parts.append(re.sub(r"(\.0)+$", "", ".".join(str(x) for x in parsed.release)))

# Pre-release
if parsed.pre is not None:
    parts.append("".join(str(x) for x in parsed.pre))

# Post-release
if parsed.post is not None:
    parts.append(f".post{parsed.post}")

# Development release
if parsed.dev is not None:
    parts.append(f".dev{parsed.dev}")

# Local version segment
if parsed.local is not None:
    parts.append(f"+{parsed.local}")
```

new syntax:
``` python
parts=[
    f'{parsed.epoch}!' if parsed.epoch != 0,
    re.sub('(\\.0)+$', '', '.'.join((str(x) for x in parsed.release))),
    ''.join((str(x) for x in parsed.pre)) if parsed.pre is not None,
    f'.post{parsed.post}' if parsed.post is not None,
    f'.dev{parsed.dev}' if parsed.dev is not None,
    f'+{parsed.local}' if parsed.local is not None,
]
```


## python3.11/site-packages/pkg_resources/_vendor/packaging/version.py:294
current syntax:
``` python
parts = []

# Epoch
if self.epoch != 0:
    parts.append(f"{self.epoch}!")

# Release segment
parts.append(".".join(str(x) for x in self.release))

# Pre-release
if self.pre is not None:
    parts.append("".join(str(x) for x in self.pre))

# Post-release
if self.post is not None:
    parts.append(f".post{self.post}")

# Development release
if self.dev is not None:
    parts.append(f".dev{self.dev}")

# Local version segment
if self.local is not None:
    parts.append(f"+{self.local}")
```

new syntax:
``` python
parts=[
    f'{self.epoch}!' if self.epoch != 0,
    '.'.join((str(x) for x in self.release)),
    ''.join((str(x) for x in self.pre)) if self.pre is not None,
    f'.post{self.post}' if self.post is not None,
    f'.dev{self.dev}' if self.dev is not None,
    f'+{self.local}' if self.local is not None,
]
```


## python3.11/site-packages/setuptools/_vendor/packaging/utils.py:52
current syntax:
``` python
parts = []

# Epoch
if parsed.epoch != 0:
    parts.append(f"{parsed.epoch}!")

# Release segment
# NB: This strips trailing '.0's to normalize
parts.append(re.sub(r"(\.0)+$", "", ".".join(str(x) for x in parsed.release)))

# Pre-release
if parsed.pre is not None:
    parts.append("".join(str(x) for x in parsed.pre))

# Post-release
if parsed.post is not None:
    parts.append(f".post{parsed.post}")

# Development release
if parsed.dev is not None:
    parts.append(f".dev{parsed.dev}")

# Local version segment
if parsed.local is not None:
    parts.append(f"+{parsed.local}")
```

new syntax:
``` python
parts=[
    f'{parsed.epoch}!' if parsed.epoch != 0,
    re.sub('(\\.0)+$', '', '.'.join((str(x) for x in parsed.release))),
    ''.join((str(x) for x in parsed.pre)) if parsed.pre is not None,
    f'.post{parsed.post}' if parsed.post is not None,
    f'.dev{parsed.dev}' if parsed.dev is not None,
    f'+{parsed.local}' if parsed.local is not None,
]
```


## python3.11/site-packages/setuptools/_vendor/packaging/version.py:294
current syntax:
``` python
parts = []

# Epoch
if self.epoch != 0:
    parts.append(f"{self.epoch}!")

# Release segment
parts.append(".".join(str(x) for x in self.release))

# Pre-release
if self.pre is not None:
    parts.append("".join(str(x) for x in self.pre))

# Post-release
if self.post is not None:
    parts.append(f".post{self.post}")

# Development release
if self.dev is not None:
    parts.append(f".dev{self.dev}")

# Local version segment
if self.local is not None:
    parts.append(f"+{self.local}")
```

new syntax:
``` python
parts=[
    f'{self.epoch}!' if self.epoch != 0,
    '.'.join((str(x) for x in self.release)),
    ''.join((str(x) for x in self.pre)) if self.pre is not None,
    f'.post{self.post}' if self.post is not None,
    f'.dev{self.dev}' if self.dev is not None,
    f'+{self.local}' if self.local is not None,
]
```


## python3.11/site-packages/pip/_vendor/distlib/wheel.py:1012
current syntax:
``` python
matches = [arch]
if arch in ('i386', 'ppc'):
    matches.append('fat')
if arch in ('i386', 'ppc', 'x86_64'):
    matches.append('fat3')
if arch in ('ppc64', 'x86_64'):
    matches.append('fat64')
if arch in ('i386', 'x86_64'):
    matches.append('intel')
if arch in ('i386', 'x86_64', 'intel', 'ppc', 'ppc64'):
    matches.append('universal')
```

new syntax:
``` python
matches=[
    arch,
    'fat' if arch in ('i386', 'ppc'),
    'fat3' if arch in ('i386', 'ppc', 'x86_64'),
    'fat64' if arch in ('ppc64', 'x86_64'),
    'intel' if arch in ('i386', 'x86_64'),
    'universal' if arch in ('i386', 'x86_64', 'intel', 'ppc', 'ppc64'),
]
```


## python3.11/site-packages/pip/_vendor/packaging/utils.py:52
current syntax:
``` python
parts = []

# Epoch
if parsed.epoch != 0:
    parts.append(f"{parsed.epoch}!")

# Release segment
# NB: This strips trailing '.0's to normalize
parts.append(re.sub(r"(\.0)+$", "", ".".join(str(x) for x in parsed.release)))

# Pre-release
if parsed.pre is not None:
    parts.append("".join(str(x) for x in parsed.pre))

# Post-release
if parsed.post is not None:
    parts.append(f".post{parsed.post}")

# Development release
if parsed.dev is not None:
    parts.append(f".dev{parsed.dev}")

# Local version segment
if parsed.local is not None:
    parts.append(f"+{parsed.local}")
```

new syntax:
``` python
parts=[
    f'{parsed.epoch}!' if parsed.epoch != 0,
    re.sub('(\\.0)+$', '', '.'.join((str(x) for x in parsed.release))),
    ''.join((str(x) for x in parsed.pre)) if parsed.pre is not None,
    f'.post{parsed.post}' if parsed.post is not None,
    f'.dev{parsed.dev}' if parsed.dev is not None,
    f'+{parsed.local}' if parsed.local is not None,
]
```


## python3.11/site-packages/pip/_vendor/packaging/version.py:294
current syntax:
``` python
parts = []

# Epoch
if self.epoch != 0:
    parts.append(f"{self.epoch}!")

# Release segment
parts.append(".".join(str(x) for x in self.release))

# Pre-release
if self.pre is not None:
    parts.append("".join(str(x) for x in self.pre))

# Post-release
if self.post is not None:
    parts.append(f".post{self.post}")

# Development release
if self.dev is not None:
    parts.append(f".dev{self.dev}")

# Local version segment
if self.local is not None:
    parts.append(f"+{self.local}")
```

new syntax:
``` python
parts=[
    f'{self.epoch}!' if self.epoch != 0,
    '.'.join((str(x) for x in self.release)),
    ''.join((str(x) for x in self.pre)) if self.pre is not None,
    f'.post{self.post}' if self.post is not None,
    f'.dev{self.dev}' if self.dev is not None,
    f'+{self.local}' if self.local is not None,
]
```


## python3.11/datetime.py:694
current syntax:
``` python
args = []
if self._days:
    args.append("days=%d" % self._days)
if self._seconds:
    args.append("seconds=%d" % self._seconds)
if self._microseconds:
    args.append("microseconds=%d" % self._microseconds)
if not args:
    args.append('0')
```

new syntax:
``` python
args=[
    'days=%d' % self._days if self._days,
    'seconds=%d' % self._seconds if self._seconds,
    'microseconds=%d' % self._microseconds if self._microseconds,
    '0' if not args,
]
```


## python3.11/subprocess.py:1042
current syntax:
``` python
to_close = []
if stdin == PIPE:
    to_close.append(p2cread)
if stdout == PIPE:
    to_close.append(c2pwrite)
if stderr == PIPE:
    to_close.append(errwrite)
if hasattr(self, '_devnull'):
    to_close.append(self._devnull)
```

new syntax:
``` python
to_close=[
    p2cread if stdin == PIPE,
    c2pwrite if stdout == PIPE,
    errwrite if stderr == PIPE,
    self._devnull if hasattr(self, '_devnull'),
]
```


## python3.11/asyncio/base_events.py:837
current syntax:
``` python
msg = [f"{host}:{port!r}"]
if family:
    msg.append(f'family={family!r}')
if type:
    msg.append(f'type={type!r}')
if proto:
    msg.append(f'proto={proto!r}')
if flags:
    msg.append(f'flags={flags!r}')
```

new syntax:
``` python
msg=[
    f'{host}:{port!r}',
    f'family={family!r}' if family,
    f'type={type!r}' if type,
    f'proto={proto!r}' if proto,
    f'flags={flags!r}' if flags,
]
```


## python3.11/ensurepip/__init__.py:192
current syntax:
``` python
args = ["install", "--no-cache-dir", "--no-index", "--find-links", tmpdir]
if root:
    args += ["--root", root]
if upgrade:
    args += ["--upgrade"]
if user:
    args += ["--user"]
if verbosity:
    args += ["-" + "v" * verbosity]
```

new syntax:
``` python
args=[
    'install',
    '--no-cache-dir',
    '--no-index',
    '--find-links',
    tmpdir,
    *['--root', root] if root,
    '--upgrade' if upgrade,
    '--user' if user,
    '-' + 'v' * verbosity if verbosity,
]
```


## python3.11/site-packages/setuptools/command/setopt.py:98
current syntax:
``` python
filenames = []
if self.global_config:
    filenames.append(config_file('global'))
if self.user_config:
    filenames.append(config_file('user'))
if self.filename is not None:
    filenames.append(self.filename)
if not filenames:
    filenames.append(config_file('local'))
```

new syntax:
``` python
filenames=[
    config_file('global') if self.global_config,
    config_file('user') if self.user_config,
    self.filename if self.filename is not None,
    config_file('local') if not filenames,
]
```


## python3.11/site-packages/pip/_internal/commands/list.py:329
current syntax:
``` python
row = [proj.raw_name, str(proj.version)]

if running_outdated:
    row.append(str(proj.latest_version))
    row.append(proj.latest_filetype)

if has_editables:
    row.append(proj.editable_project_location or "")

if options.verbose >= 1:
    row.append(proj.location or "")
if options.verbose >= 1:
    row.append(proj.installer)
```

new syntax:
``` python
row=[
    proj.raw_name,
    str(proj.version),
    *[str(proj.latest_version), proj.latest_filetype] if running_outdated,
    proj.editable_project_location or '' if has_editables,
    proj.location or '' if options.verbose >= 1,
    proj.installer if options.verbose >= 1,
]
```


## python3.11/test/support/socket_helper.py:174
current syntax:
``` python
errors = [errno.ECONNREFUSED]
if hasattr(errno, 'ENETUNREACH'):
    # On Solaris, ENETUNREACH is returned sometimes instead of ECONNREFUSED
    errors.append(errno.ENETUNREACH)
if hasattr(errno, 'EADDRNOTAVAIL'):
    # bpo-31910: socket.create_connection() fails randomly
    # with EADDRNOTAVAIL on Travis CI
    errors.append(errno.EADDRNOTAVAIL)
if hasattr(errno, 'EHOSTUNREACH'):
    # bpo-37583: The destination host cannot be reached
    errors.append(errno.EHOSTUNREACH)
if not IPV6_ENABLED:
    errors.append(errno.EAFNOSUPPORT)
```

new syntax:
``` python
errors=[
    errno.ECONNREFUSED,
    errno.ENETUNREACH if hasattr(errno, 'ENETUNREACH'),
    errno.EADDRNOTAVAIL if hasattr(errno, 'EADDRNOTAVAIL'),
    errno.EHOSTUNREACH if hasattr(errno, 'EHOSTUNREACH'),
    errno.EAFNOSUPPORT if not IPV6_ENABLED,
]
```


## python3.11/asyncio/subprocess.py:31
current syntax:
``` python
info = [self.__class__.__name__]
if self.stdin is not None:
    info.append(f'stdin={self.stdin!r}')
if self.stdout is not None:
    info.append(f'stdout={self.stdout!r}')
if self.stderr is not None:
    info.append(f'stderr={self.stderr!r}')
```

new syntax:
``` python
info=[
    self.__class__.__name__,
    f'stdin={self.stdin!r}' if self.stdin is not None,
    f'stdout={self.stdout!r}' if self.stdout is not None,
    f'stderr={self.stderr!r}' if self.stderr is not None,
]
```


## python3.11/site-packages/pip/_vendor/pygments/formatters/terminal256.py:88
current syntax:
``` python
attrs = []
if self.fg is not None:
    attrs.append("39")
if self.bg is not None:
    attrs.append("49")
if self.bold or self.underline or self.italic:
    attrs.append("00")
```

new syntax:
``` python
attrs=[
    '39' if self.fg is not None,
    '49' if self.bg is not None,
    '00' if self.bold or self.underline or self.italic,
]
```


## python3.11/optparse.py:1068
current syntax:
``` python
result = []
if self.description:
    result.append(self.format_description(formatter))
if self.option_list:
    result.append(self.format_option_help(formatter))
```

new syntax:
``` python
result=[
    self.format_description(formatter) if self.description,
    self.format_option_help(formatter) if self.option_list,
]
```


## python3.11/optparse.py:1630
current syntax:
``` python
result = []
if self.usage:
    result.append(self.get_usage() + "\n")
if self.description:
    result.append(self.format_description(formatter) + "\n")
result.append(self.format_option_help(formatter))
result.append(self.format_epilog(formatter))
```

new syntax:
``` python
result=[
    self.get_usage() + '\n' if self.usage,
    self.format_description(formatter) + '\n' if self.description,
    self.format_option_help(formatter),
    self.format_epilog(formatter),
]
```


## python3.11/site.py:651
current syntax:
``` python
buffer = []
if '--user-base' in args:
    buffer.append(USER_BASE)
if '--user-site' in args:
    buffer.append(USER_SITE)
```

new syntax:
``` python
buffer=[
    USER_BASE if '--user-base' in args,
    USER_SITE if '--user-site' in args,
]
```


## python3.11/subprocess.py:488
current syntax:
``` python
args = ['args={!r}'.format(self.args),
        'returncode={!r}'.format(self.returncode)]
if self.stdout is not None:
    args.append('stdout={!r}'.format(self.stdout))
if self.stderr is not None:
    args.append('stderr={!r}'.format(self.stderr))
```

new syntax:
``` python
args=[
    'args={!r}'.format(self.args),
    'returncode={!r}'.format(self.returncode),
    'stdout={!r}'.format(self.stdout) if self.stdout is not None,
    'stderr={!r}'.format(self.stderr) if self.stderr is not None,
]
```


## python3.11/warnings.py:458
current syntax:
``` python
args = []
if self._record:
    args.append("record=True")
if self._module is not sys.modules['warnings']:
    args.append("module=%r" % self._module)
```

new syntax:
``` python
args=[
    'record=True' if self._record,
    'module=%r' % self._module if self._module is not sys.modules['warnings'],
]
```


## python3.11/asyncio/base_subprocess.py:56
current syntax:
``` python
info = [self.__class__.__name__]
if self._closed:
    info.append('closed')
if self._pid is not None:
    info.append(f'pid={self._pid}')
```

new syntax:
``` python
info=[
    self.__class__.__name__,
    'closed' if self._closed,
    f'pid={self._pid}' if self._pid is not None,
]
```


## python3.11/asyncio/events.py:47
current syntax:
``` python
info = [self.__class__.__name__]
if self._cancelled:
    info.append('cancelled')
if self._callback is not None:
    info.append(format_helpers._format_callback_source(
        self._callback, self._args))
```

new syntax:
``` python
info=[
    self.__class__.__name__,
    'cancelled' if self._cancelled,
    format_helpers._format_callback_source(self._callback, self._args) if self._callback is not None,
]
```


## python3.11/asyncio/taskgroups.py:27
current syntax:
``` python
info = ['']
if self._tasks:
    info.append(f'tasks={len(self._tasks)}')
if self._errors:
    info.append(f'errors={len(self._errors)}')
```

new syntax:
``` python
info=[
    '',
    f'tasks={len(self._tasks)}' if self._tasks,
    f'errors={len(self._errors)}' if self._errors,
]
```


## python3.11/importlib/_bootstrap.py:371
current syntax:
``` python
args = ['name={!r}'.format(self.name),
        'loader={!r}'.format(self.loader)]
if self.origin is not None:
    args.append('origin={!r}'.format(self.origin))
if self.submodule_search_locations is not None:
    args.append('submodule_search_locations={}'
                .format(self.submodule_search_locations))
```

new syntax:
``` python
args=[
    'name={!r}'.format(self.name),
    'loader={!r}'.format(self.loader),
    'origin={!r}'.format(self.origin) if self.origin is not None,
    'submodule_search_locations={}'.format(self.submodule_search_locations) if self.submodule_search_locations is not None,
]
```


## python3.11/site-packages/setuptools/msvc.py:1430
current syntax:
``` python
tools = []
if include32:
    tools += [join(si.FrameworkDir32, ver)
              for ver in si.FrameworkVersion32]
if include64:
    tools += [join(si.FrameworkDir64, ver)
              for ver in si.FrameworkVersion64]
```

new syntax:
``` python
tools=[
    *[join(si.FrameworkDir32, ver) for ver in si.FrameworkVersion32] if include32,
    *[join(si.FrameworkDir64, ver) for ver in si.FrameworkVersion64] if include64,
]
```


## python3.11/site-packages/pip/_internal/cli/parser.py:41
current syntax:
``` python
opts = []

if option._short_opts:
    opts.append(option._short_opts[0])
if option._long_opts:
    opts.append(option._long_opts[0])
```

new syntax:
``` python
opts=[
    option._short_opts[0] if option._short_opts,
    option._long_opts[0] if option._long_opts,
]
```


## python3.11/site-packages/pip/_vendor/distlib/index.py:450
current syntax:
``` python
handlers = []
if self.password_handler:
    handlers.append(self.password_handler)
if self.ssl_verifier:
    handlers.append(self.ssl_verifier)
```

new syntax:
``` python
handlers=[
    self.password_handler if self.password_handler,
    self.ssl_verifier if self.ssl_verifier,
]
```


## python3.11/site-packages/pip/_vendor/pygments/formatters/html.py:792
current syntax:
``` python
style = []
if (self.noclasses and not self.nobackground and
        self.style.background_color is not None):
    style.append('background: %s' % (self.style.background_color,))
if self.cssstyles:
    style.append(self.cssstyles)
```

new syntax:
``` python
style=[
    'background: %s' % (self.style.background_color,) if self.noclasses and (not self.nobackground) and (self.style.background_color is not None),
    self.cssstyles if self.cssstyles,
]
```


## python3.11/site-packages/pip/_vendor/pygments/formatters/html.py:806
current syntax:
``` python
style = []
if self.prestyles:
    style.append(self.prestyles)
if self.noclasses:
    style.append(self._pre_style)
```

new syntax:
``` python
style=[
    self.prestyles if self.prestyles,
    self._pre_style if self.noclasses,
]
```


## python3.11/xml/dom/minidom.py:1818
current syntax:
``` python
declarations = []

if encoding:
    declarations.append(f'encoding="{encoding}"')
if standalone is not None:
    declarations.append(f'standalone="{"yes" if standalone else "no"}"')
```

new syntax:
``` python
declarations=[
    f'encoding="{encoding}"' if encoding,
    f'''standalone="{('yes' if standalone else 'no')}"''' if standalone is not None,
]
```


## python3.11/test/test_codecs.py:1788
current syntax:
``` python
all_unicode_encodings = [
    "ascii",
    "big5",
    "big5hkscs",
    "charmap",
    "cp037",
    "cp1006",
    "cp1026",
    "cp1125",
    "cp1140",
    "cp1250",
    "cp1251",
    "cp1252",
    "cp1253",
    "cp1254",
    "cp1255",
    "cp1256",
    "cp1257",
    "cp1258",
    "cp424",
    "cp437",
    "cp500",
    "cp720",
    "cp737",
    "cp775",
    "cp850",
    "cp852",
    "cp855",
    "cp856",
    "cp857",
    "cp858",
    "cp860",
    "cp861",
    "cp862",
    "cp863",
    "cp864",
    "cp865",
    "cp866",
    "cp869",
    "cp874",
    "cp875",
    "cp932",
    "cp949",
    "cp950",
    "euc_jis_2004",
    "euc_jisx0213",
    "euc_jp",
    "euc_kr",
    "gb18030",
    "gb2312",
    "gbk",
    "hp_roman8",
    "hz",
    "idna",
    "iso2022_jp",
    "iso2022_jp_1",
    "iso2022_jp_2",
    "iso2022_jp_2004",
    "iso2022_jp_3",
    "iso2022_jp_ext",
    "iso2022_kr",
    "iso8859_1",
    "iso8859_10",
    "iso8859_11",
    "iso8859_13",
    "iso8859_14",
    "iso8859_15",
    "iso8859_16",
    "iso8859_2",
    "iso8859_3",
    "iso8859_4",
    "iso8859_5",
    "iso8859_6",
    "iso8859_7",
    "iso8859_8",
    "iso8859_9",
    "johab",
    "koi8_r",
    "koi8_t",
    "koi8_u",
    "kz1048",
    "latin_1",
    "mac_cyrillic",
    "mac_greek",
    "mac_iceland",
    "mac_latin2",
    "mac_roman",
    "mac_turkish",
    "palmos",
    "ptcp154",
    "punycode",
    "raw_unicode_escape",
    "shift_jis",
    "shift_jis_2004",
    "shift_jisx0213",
    "tis_620",
    "unicode_escape",
    "utf_16",
    "utf_16_be",
    "utf_16_le",
    "utf_7",
    "utf_8",
]

if hasattr(codecs, "mbcs_encode"):
    all_unicode_encodings.append("mbcs")
if hasattr(codecs, "oem_encode"):
    all_unicode_encodings.append("oem")
```

new syntax:
``` python
all_unicode_encodings=[
    'ascii',
    'big5',
    'big5hkscs',
    'charmap',
    'cp037',
    'cp1006',
    'cp1026',
    'cp1125',
    'cp1140',
    'cp1250',
    'cp1251',
    'cp1252',
    'cp1253',
    'cp1254',
    'cp1255',
    'cp1256',
    'cp1257',
    'cp1258',
    'cp424',
    'cp437',
    'cp500',
    'cp720',
    'cp737',
    'cp775',
    'cp850',
    'cp852',
    'cp855',
    'cp856',
    'cp857',
    'cp858',
    'cp860',
    'cp861',
    'cp862',
    'cp863',
    'cp864',
    'cp865',
    'cp866',
    'cp869',
    'cp874',
    'cp875',
    'cp932',
    'cp949',
    'cp950',
    'euc_jis_2004',
    'euc_jisx0213',
    'euc_jp',
    'euc_kr',
    'gb18030',
    'gb2312',
    'gbk',
    'hp_roman8',
    'hz',
    'idna',
    'iso2022_jp',
    'iso2022_jp_1',
    'iso2022_jp_2',
    'iso2022_jp_2004',
    'iso2022_jp_3',
    'iso2022_jp_ext',
    'iso2022_kr',
    'iso8859_1',
    'iso8859_10',
    'iso8859_11',
    'iso8859_13',
    'iso8859_14',
    'iso8859_15',
    'iso8859_16',
    'iso8859_2',
    'iso8859_3',
    'iso8859_4',
    'iso8859_5',
    'iso8859_6',
    'iso8859_7',
    'iso8859_8',
    'iso8859_9',
    'johab',
    'koi8_r',
    'koi8_t',
    'koi8_u',
    'kz1048',
    'latin_1',
    'mac_cyrillic',
    'mac_greek',
    'mac_iceland',
    'mac_latin2',
    'mac_roman',
    'mac_turkish',
    'palmos',
    'ptcp154',
    'punycode',
    'raw_unicode_escape',
    'shift_jis',
    'shift_jis_2004',
    'shift_jisx0213',
    'tis_620',
    'unicode_escape',
    'utf_16',
    'utf_16_be',
    'utf_16_le',
    'utf_7',
    'utf_8',
    'mbcs' if hasattr(codecs, 'mbcs_encode'),
    'oem' if hasattr(codecs, 'oem_encode'),
]
```


## python3.11/test/test_compileall.py:985
current syntax:
``` python
lines = []
if docstring:
    lines.append("'module docstring'")
lines.append('x = 1')
if assertion:
    lines.append("assert x == 1")
```

new syntax:
``` python
lines=[
    "'module docstring'" if docstring,
    'x = 1',
    'assert x == 1' if assertion,
]
```


## python3.11/test/test_faulthandler.py:105
current syntax:
``` python
regex = [f'^{fatal_error}']
if py_fatal_error:
    regex.append("Python runtime state: initialized")
regex.append('')
regex.append(fr'{header} \(most recent call first\):')
if garbage_collecting:
    regex.append('  Garbage-collecting')
regex.append(fr'  File "<string>", line {lineno} in {function}')
```

new syntax:
``` python
regex=[
    f'^{fatal_error}',
    'Python runtime state: initialized' if py_fatal_error,
    '',
    f'{header} \\(most recent call first\\):',
    '  Garbage-collecting' if garbage_collecting,
    f'  File "<string>", line {lineno} in {function}',
]
```


## python3.11/test/test_utf8_mode.py:170
current syntax:
``` python
args = []
if encoding:
    args.append(f'encoding={encoding!r}')
if errors:
    args.append(f'errors={errors!r}')
```

new syntax:
``` python
args=[
    f'encoding={encoding!r}' if encoding,
    f'errors={errors!r}' if errors,
]
```


## python3.11/test/libregrtest/setup.py:35
current syntax:
``` python
signals = []
if hasattr(signal, 'SIGALRM'):
    signals.append(signal.SIGALRM)
if hasattr(signal, 'SIGUSR1'):
    signals.append(signal.SIGUSR1)
```

new syntax:
``` python
signals=[
    signal.SIGALRM if hasattr(signal, 'SIGALRM'),
    signal.SIGUSR1 if hasattr(signal, 'SIGUSR1'),
]
```


## python3.11/test/libregrtest/utils.py:14
current syntax:
``` python
parts = []
if hours:
    parts.append('%s hour' % hours)
if minutes:
    parts.append('%s min' % minutes)
```

new syntax:
``` python
parts=[
    '%s hour' % hours if hours,
    '%s min' % minutes if minutes,
]
```


## python3.11/configparser.py:202
current syntax:
``` python
message = ["While reading from ", repr(source)]
if lineno is not None:
    message.append(" [line {0:2d}]".format(lineno))
message.append(": section ")
```

new syntax:
``` python
message=[
    'While reading from ',
    repr(source),
    ' [line {0:2d}]'.format(lineno) if lineno is not None,
    ': section ',
]
```


## python3.11/configparser.py:228
current syntax:
``` python
message = ["While reading from ", repr(source)]
if lineno is not None:
    message.append(" [line {0:2d}]".format(lineno))
message.append(": option ")
```

new syntax:
``` python
message=[
    'While reading from ',
    repr(source),
    ' [line {0:2d}]'.format(lineno) if lineno is not None,
    ': option ',
]
```


## python3.11/dataclasses.py:573
current syntax:
``` python
_init_params = [_init_param(f) for f in std_fields]
if kw_only_fields:
    # Add the keyword-only args.  Because the * can only be added if
    # there's at least one keyword-only arg, there needs to be a test here
    # (instead of just concatenting the lists together).
    _init_params += ['*']
    _init_params += [_init_param(f) for f in kw_only_fields]
```

new syntax:
``` python
_init_params=[
    *[_init_param(f) for f in std_fields],
    *['*', *[_init_param(f) for f in kw_only_fields]] if kw_only_fields,
]
```


## python3.11/reprlib.py:72
current syntax:
``` python
pieces = [repr1(elem, newlevel) for elem in islice(x, maxiter)]
if n > maxiter:
    pieces.append(self.fillvalue)
```

new syntax:
``` python
pieces=[
    *[repr1(elem, newlevel) for elem in islice(x, maxiter)],
    self.fillvalue if n > maxiter,
]
```


## python3.11/site.py:365
current syntax:
``` python
libdirs = [sys.platlibdir]
if sys.platlibdir != "lib":
    libdirs.append("lib")
```

new syntax:
``` python
libdirs=[
    sys.platlibdir,
    'lib' if sys.platlibdir != 'lib',
]
```


## python3.11/typing.py:1256
current syntax:
``` python
res = []
if self.__origin__ not in bases:
    res.append(self.__origin__)
```

new syntax:
``` python
res=[
    self.__origin__ if self.__origin__ not in bases,
]
```


## python3.11/zipfile.py:414
current syntax:
``` python
result = ['<%s filename=%r' % (self.__class__.__name__, self.filename)]
if self.compress_type != ZIP_STORED:
    result.append(' compress_type=%s' %
                  compressor_names.get(self.compress_type,
                                       self.compress_type))
```

new syntax:
``` python
result=[
    '<%s filename=%r' % (self.__class__.__name__, self.filename),
    ' compress_type=%s' % compressor_names.get(self.compress_type, self.compress_type) if self.compress_type != ZIP_STORED,
]
```


## python3.11/asyncio/base_events.py:130
current syntax:
``` python
afs = [socket.AF_INET]
if _HAS_IPv6:
    afs.append(socket.AF_INET6)
```

new syntax:
``` python
afs=[
    socket.AF_INET,
    socket.AF_INET6 if _HAS_IPv6,
]
```


## python3.11/asyncio/base_events.py:1619
current syntax:
``` python
info = [msg]
if stdin is not None:
    info.append(f'stdin={_format_pipe(stdin)}')
```

new syntax:
``` python
info=[
    msg,
    f'stdin={_format_pipe(stdin)}' if stdin is not None,
]
```


## python3.11/asyncio/streams.py:322
current syntax:
``` python
info = [self.__class__.__name__, f'transport={self._transport!r}']
if self._reader is not None:
    info.append(f'reader={self._reader!r}')
```

new syntax:
``` python
info=[
    self.__class__.__name__,
    f'transport={self._transport!r}',
    f'reader={self._reader!r}' if self._reader is not None,
]
```


## python3.11/asyncio/windows_events.py:433
current syntax:
``` python
info = ['overlapped#=%s' % len(self._cache),
        'result#=%s' % len(self._results)]
if self._iocp is None:
    info.append('closed')
```

new syntax:
``` python
info=[
    'overlapped#=%s' % len(self._cache),
    'result#=%s' % len(self._results),
    'closed' if self._iocp is None,
]
```


## python3.11/distutils/command/config.py:294
current syntax:
``` python
body = []
if decl:
    body.append("int %s ();" % func)
body.append("int main () {")
```

new syntax:
``` python
body=[
    'int %s ();' % func if decl,
    'int main () {',
]
```


## python3.11/distutils/tests/test_bdist_dumb.py:88
current syntax:
``` python
wanted = ['foo-0.1-py%s.%s.egg-info' % sys.version_info[:2], 'foo.py']
if not sys.dont_write_bytecode:
    wanted.append('foo.%s.pyc' % sys.implementation.cache_tag)
```

new syntax:
``` python
wanted=[
    'foo-0.1-py%s.%s.egg-info' % sys.version_info[:2],
    'foo.py',
    'foo.%s.pyc' % sys.implementation.cache_tag if not sys.dont_write_bytecode,
]
```


## python3.11/ensurepip/__init__.py:228
current syntax:
``` python
args = ["uninstall", "-y", "--disable-pip-version-check"]
if verbosity:
    args += ["-" + "v" * verbosity]
```

new syntax:
``` python
args=[
    'uninstall',
    '-y',
    '--disable-pip-version-check',
    '-' + 'v' * verbosity if verbosity,
]
```


## python3.11/http/server.py:1162
current syntax:
``` python
args = [script]
if '=' not in decoded_query:
    args.append(decoded_query)
```

new syntax:
``` python
args=[
    script,
    decoded_query if '=' not in decoded_query,
]
```


## python3.11/idlelib/searchbase.py:145
current syntax:
``` python
options = [(engine.revar, "Regular expression"),
           (engine.casevar, "Match case"),
           (engine.wordvar, "Whole word")]
if self.needwrapbutton:
    options.append((engine.wrapvar, "Wrap around"))
```

new syntax:
``` python
options=[
    (engine.revar, 'Regular expression'),
    (engine.casevar, 'Match case'),
    (engine.wordvar, 'Whole word'),
    (engine.wrapvar, 'Wrap around') if self.needwrapbutton,
]
```


## python3.11/importlib/_bootstrap_external.py:427
current syntax:
``` python
SOURCE_SUFFIXES = ['.py']
if _MS_WINDOWS:
    SOURCE_SUFFIXES.append('.pyw')
```

new syntax:
``` python
SOURCE_SUFFIXES=[
    '.py',
    '.pyw' if _MS_WINDOWS,
]
```


## python3.11/importlib/metadata/_adapters.py:49
current syntax:
``` python
headers = [(key, redent(value)) for key, value in vars(self)['_headers']]
if self._payload:
    headers.append(('Description', self.get_payload()))
```

new syntax:
``` python
headers=[
    *[(key, redent(value)) for key, value in vars(self)['_headers']],
    ('Description', self.get_payload()) if self._payload,
]
```


## python3.11/lib2to3/refactor.py:604
current syntax:
``` python
block = [indent + self.PS1 + new.pop(0)]
if new:
    block += [indent + self.PS2 + line for line in new]
```

new syntax:
``` python
block=[
    indent + self.PS1 + new.pop(0),
    *[indent + self.PS2 + line for line in new] if new,
]
```


## python3.11/multiprocessing/process.py:276
current syntax:
``` python
info = [type(self).__name__, 'name=%r' % self._name]
if self._popen is not None:
    info.append('pid=%s' % self._popen.pid)
info.append('parent=%s' % self._parent_pid)
info.append(status)
```

new syntax:
``` python
info=[
    type(self).__name__,
    'name=%r' % self._name,
    'pid=%s' % self._popen.pid if self._popen is not None,
    'parent=%s' % self._parent_pid,
    status,
]
```


## python3.11/site-packages/pkg_resources/_vendor/packaging/version.py:357
current syntax:
``` python
parts = []

# Epoch
if self.epoch != 0:
    parts.append(f"{self.epoch}!")

# Release segment
parts.append(".".join(str(x) for x in self.release))
```

new syntax:
``` python
parts=[
    f'{self.epoch}!' if self.epoch != 0,
    '.'.join((str(x) for x in self.release)),
]
```


## python3.11/site-packages/pkg_resources/_vendor/pyparsing/exceptions.py:63
current syntax:
``` python
ret = []
if isinstance(exc, ParseBaseException):
    ret.append(exc.line)
    ret.append(" " * (exc.column - 1) + "^")
ret.append("{}: {}".format(type(exc).__name__, exc))
```

new syntax:
``` python
ret=[
    *[exc.line, ' ' * (exc.column - 1) + '^'] if isinstance(exc, ParseBaseException),
    '{}: {}'.format(type(exc).__name__, exc),
]
```


## python3.11/site-packages/setuptools/installer.py:65
current syntax:
``` python
cmd = [
    sys.executable, '-m', 'pip',
    '--disable-pip-version-check',
    'wheel', '--no-deps',
    '-w', tmpdir,
]
if quiet:
    cmd.append('--quiet')
```

new syntax:
``` python
cmd=[
    sys.executable,
    '-m',
    'pip',
    '--disable-pip-version-check',
    'wheel',
    '--no-deps',
    '-w',
    tmpdir,
    '--quiet' if quiet,
]
```


## python3.11/site-packages/setuptools/msvc.py:1197
current syntax:
``` python
paths = ['Lib%s' % arch_subdir, r'ATLMFC\Lib%s' % arch_subdir]

if self.vs_ver >= 14.0:
    paths += [r'Lib\store%s' % arch_subdir]
```

new syntax:
``` python
paths=[
    'Lib%s' % arch_subdir,
    'ATLMFC\\Lib%s' % arch_subdir,
    'Lib\\store%s' % arch_subdir if self.vs_ver >= 14.0,
]
```


## python3.11/site-packages/setuptools/msvc.py:1502
current syntax:
``` python
build = [join(base_path, path)]

if self.vs_ver >= 15.0:
    # Add Roslyn C# & Visual Basic Compiler
    build += [join(base_path, path, 'Roslyn')]
```

new syntax:
``` python
build=[
    join(base_path, path),
    join(base_path, path, 'Roslyn') if self.vs_ver >= 15.0,
]
```


## python3.11/site-packages/setuptools/_distutils/command/config.py:316
current syntax:
``` python
body = []
if decl:
    body.append("int %s ();" % func)
body.append("int main () {")
```

new syntax:
``` python
body=[
    'int %s ();' % func if decl,
    'int main () {',
]
```


## python3.11/site-packages/setuptools/_vendor/importlib_metadata/_adapters.py:49
current syntax:
``` python
headers = [(key, redent(value)) for key, value in vars(self)['_headers']]
if self._payload:
    headers.append(('Description', self.get_payload()))
```

new syntax:
``` python
headers=[
    *[(key, redent(value)) for key, value in vars(self)['_headers']],
    ('Description', self.get_payload()) if self._payload,
]
```


## python3.11/site-packages/setuptools/_vendor/packaging/version.py:357
current syntax:
``` python
parts = []

# Epoch
if self.epoch != 0:
    parts.append(f"{self.epoch}!")

# Release segment
parts.append(".".join(str(x) for x in self.release))
```

new syntax:
``` python
parts=[
    f'{self.epoch}!' if self.epoch != 0,
    '.'.join((str(x) for x in self.release)),
]
```


## python3.11/site-packages/setuptools/_vendor/pyparsing/exceptions.py:63
current syntax:
``` python
ret = []
if isinstance(exc, ParseBaseException):
    ret.append(exc.line)
    ret.append(" " * (exc.column - 1) + "^")
ret.append("{}: {}".format(type(exc).__name__, exc))
```

new syntax:
``` python
ret=[
    *[exc.line, ' ' * (exc.column - 1) + '^'] if isinstance(exc, ParseBaseException),
    '{}: {}'.format(type(exc).__name__, exc),
]
```


## python3.11/site-packages/setuptools/command/easy_install.py:1387
current syntax:
``` python
prefixes = [sys.prefix]
if sys.exec_prefix != sys.prefix:
    prefixes.append(sys.exec_prefix)
```

new syntax:
``` python
prefixes=[
    sys.prefix,
    sys.exec_prefix if sys.exec_prefix != sys.prefix,
]
```


## python3.11/site-packages/setuptools/command/test.py:42
current syntax:
``` python
tests = []
tests.append(TestLoader.loadTestsFromModule(self, module))

if hasattr(module, "additional_tests"):
    tests.append(module.additional_tests())
```

new syntax:
``` python
tests=[
    TestLoader.loadTestsFromModule(self, module),
    module.additional_tests() if hasattr(module, 'additional_tests'),
]
```


## python3.11/site-packages/pip/_internal/cli/main_parser.py:124
current syntax:
``` python
msg = [f'unknown command "{cmd_name}"']
if guess:
    msg.append(f'maybe you meant "{guess}"')
```

new syntax:
``` python
msg=[
    f'unknown command "{cmd_name}"',
    f'maybe you meant "{guess}"' if guess,
]
```


## python3.11/site-packages/pip/_internal/commands/help.py:32
current syntax:
``` python
msg = [f'unknown command "{cmd_name}"']
if guess:
    msg.append(f'maybe you meant "{guess}"')
```

new syntax:
``` python
msg=[
    f'unknown command "{cmd_name}"',
    f'maybe you meant "{guess}"' if guess,
]
```


## python3.11/site-packages/pip/_internal/locations/_sysconfig.py:112
current syntax:
``` python
_HOME_KEYS = [
    "installed_base",
    "base",
    "installed_platbase",
    "platbase",
    "prefix",
    "exec_prefix",
]
if sysconfig.get_config_var("userbase") is not None:
    _HOME_KEYS.append("userbase")
```

new syntax:
``` python
_HOME_KEYS=[
    'installed_base',
    'base',
    'installed_platbase',
    'platbase',
    'prefix',
    'exec_prefix',
    'userbase' if sysconfig.get_config_var('userbase') is not None,
]
```


## python3.11/site-packages/pip/_internal/utils/setuptools_build.py:64
current syntax:
``` python
args = [sys.executable]
if unbuffered_output:
    args += ["-u"]
args += ["-c", _SETUPTOOLS_SHIM.format(setup_py_path)]
```

new syntax:
``` python
args=[
    sys.executable,
    '-u' if unbuffered_output,
    '-c',
    _SETUPTOOLS_SHIM.format(setup_py_path),
]
```


## python3.11/site-packages/pip/_vendor/six.py:251
current syntax:
``` python
_moved_attributes = [
    MovedAttribute("cStringIO", "cStringIO", "io", "StringIO"),
    MovedAttribute("filter", "itertools", "builtins", "ifilter", "filter"),
    MovedAttribute("filterfalse", "itertools", "itertools", "ifilterfalse", "filterfalse"),
    MovedAttribute("input", "__builtin__", "builtins", "raw_input", "input"),
    MovedAttribute("intern", "__builtin__", "sys"),
    MovedAttribute("map", "itertools", "builtins", "imap", "map"),
    MovedAttribute("getcwd", "os", "os", "getcwdu", "getcwd"),
    MovedAttribute("getcwdb", "os", "os", "getcwd", "getcwdb"),
    MovedAttribute("getoutput", "commands", "subprocess"),
    MovedAttribute("range", "__builtin__", "builtins", "xrange", "range"),
    MovedAttribute("reload_module", "__builtin__", "importlib" if PY34 else "imp", "reload"),
    MovedAttribute("reduce", "__builtin__", "functools"),
    MovedAttribute("shlex_quote", "pipes", "shlex", "quote"),
    MovedAttribute("StringIO", "StringIO", "io"),
    MovedAttribute("UserDict", "UserDict", "collections"),
    MovedAttribute("UserList", "UserList", "collections"),
    MovedAttribute("UserString", "UserString", "collections"),
    MovedAttribute("xrange", "__builtin__", "builtins", "xrange", "range"),
    MovedAttribute("zip", "itertools", "builtins", "izip", "zip"),
    MovedAttribute("zip_longest", "itertools", "itertools", "izip_longest", "zip_longest"),
    MovedModule("builtins", "__builtin__"),
    MovedModule("configparser", "ConfigParser"),
    MovedModule("collections_abc", "collections", "collections.abc" if sys.version_info >= (3, 3) else "collections"),
    MovedModule("copyreg", "copy_reg"),
    MovedModule("dbm_gnu", "gdbm", "dbm.gnu"),
    MovedModule("dbm_ndbm", "dbm", "dbm.ndbm"),
    MovedModule("_dummy_thread", "dummy_thread", "_dummy_thread" if sys.version_info < (3, 9) else "_thread"),
    MovedModule("http_cookiejar", "cookielib", "http.cookiejar"),
    MovedModule("http_cookies", "Cookie", "http.cookies"),
    MovedModule("html_entities", "htmlentitydefs", "html.entities"),
    MovedModule("html_parser", "HTMLParser", "html.parser"),
    MovedModule("http_client", "httplib", "http.client"),
    MovedModule("email_mime_base", "email.MIMEBase", "email.mime.base"),
    MovedModule("email_mime_image", "email.MIMEImage", "email.mime.image"),
    MovedModule("email_mime_multipart", "email.MIMEMultipart", "email.mime.multipart"),
    MovedModule("email_mime_nonmultipart", "email.MIMENonMultipart", "email.mime.nonmultipart"),
    MovedModule("email_mime_text", "email.MIMEText", "email.mime.text"),
    MovedModule("BaseHTTPServer", "BaseHTTPServer", "http.server"),
    MovedModule("CGIHTTPServer", "CGIHTTPServer", "http.server"),
    MovedModule("SimpleHTTPServer", "SimpleHTTPServer", "http.server"),
    MovedModule("cPickle", "cPickle", "pickle"),
    MovedModule("queue", "Queue"),
    MovedModule("reprlib", "repr"),
    MovedModule("socketserver", "SocketServer"),
    MovedModule("_thread", "thread", "_thread"),
    MovedModule("tkinter", "Tkinter"),
    MovedModule("tkinter_dialog", "Dialog", "tkinter.dialog"),
    MovedModule("tkinter_filedialog", "FileDialog", "tkinter.filedialog"),
    MovedModule("tkinter_scrolledtext", "ScrolledText", "tkinter.scrolledtext"),
    MovedModule("tkinter_simpledialog", "SimpleDialog", "tkinter.simpledialog"),
    MovedModule("tkinter_tix", "Tix", "tkinter.tix"),
    MovedModule("tkinter_ttk", "ttk", "tkinter.ttk"),
    MovedModule("tkinter_constants", "Tkconstants", "tkinter.constants"),
    MovedModule("tkinter_dnd", "Tkdnd", "tkinter.dnd"),
    MovedModule("tkinter_colorchooser", "tkColorChooser",
                "tkinter.colorchooser"),
    MovedModule("tkinter_commondialog", "tkCommonDialog",
                "tkinter.commondialog"),
    MovedModule("tkinter_tkfiledialog", "tkFileDialog", "tkinter.filedialog"),
    MovedModule("tkinter_font", "tkFont", "tkinter.font"),
    MovedModule("tkinter_messagebox", "tkMessageBox", "tkinter.messagebox"),
    MovedModule("tkinter_tksimpledialog", "tkSimpleDialog",
                "tkinter.simpledialog"),
    MovedModule("urllib_parse", __name__ + ".moves.urllib_parse", "urllib.parse"),
    MovedModule("urllib_error", __name__ + ".moves.urllib_error", "urllib.error"),
    MovedModule("urllib", __name__ + ".moves.urllib", __name__ + ".moves.urllib"),
    MovedModule("urllib_robotparser", "robotparser", "urllib.robotparser"),
    MovedModule("xmlrpc_client", "xmlrpclib", "xmlrpc.client"),
    MovedModule("xmlrpc_server", "SimpleXMLRPCServer", "xmlrpc.server"),
]
# Add windows specific modules.
if sys.platform == "win32":
    _moved_attributes += [
        MovedModule("winreg", "_winreg"),
```

new syntax:
``` python
_moved_attributes=[
    MovedAttribute('cStringIO', 'cStringIO', 'io', 'StringIO'),
    MovedAttribute('filter', 'itertools', 'builtins', 'ifilter', 'filter'),
    MovedAttribute('filterfalse', 'itertools', 'itertools', 'ifilterfalse', 'filterfalse'),
    MovedAttribute('input', '__builtin__', 'builtins', 'raw_input', 'input'),
    MovedAttribute('intern', '__builtin__', 'sys'),
    MovedAttribute('map', 'itertools', 'builtins', 'imap', 'map'),
    MovedAttribute('getcwd', 'os', 'os', 'getcwdu', 'getcwd'),
    MovedAttribute('getcwdb', 'os', 'os', 'getcwd', 'getcwdb'),
    MovedAttribute('getoutput', 'commands', 'subprocess'),
    MovedAttribute('range', '__builtin__', 'builtins', 'xrange', 'range'),
    MovedAttribute('reload_module', '__builtin__', 'importlib' if PY34 else 'imp', 'reload'),
    MovedAttribute('reduce', '__builtin__', 'functools'),
    MovedAttribute('shlex_quote', 'pipes', 'shlex', 'quote'),
    MovedAttribute('StringIO', 'StringIO', 'io'),
    MovedAttribute('UserDict', 'UserDict', 'collections'),
    MovedAttribute('UserList', 'UserList', 'collections'),
    MovedAttribute('UserString', 'UserString', 'collections'),
    MovedAttribute('xrange', '__builtin__', 'builtins', 'xrange', 'range'),
    MovedAttribute('zip', 'itertools', 'builtins', 'izip', 'zip'),
    MovedAttribute('zip_longest', 'itertools', 'itertools', 'izip_longest', 'zip_longest'),
    MovedModule('builtins', '__builtin__'),
    MovedModule('configparser', 'ConfigParser'),
    MovedModule('collections_abc', 'collections', 'collections.abc' if sys.version_info >= (3, 3) else 'collections'),
    MovedModule('copyreg', 'copy_reg'),
    MovedModule('dbm_gnu', 'gdbm', 'dbm.gnu'),
    MovedModule('dbm_ndbm', 'dbm', 'dbm.ndbm'),
    MovedModule('_dummy_thread', 'dummy_thread', '_dummy_thread' if sys.version_info < (3, 9) else '_thread'),
    MovedModule('http_cookiejar', 'cookielib', 'http.cookiejar'),
    MovedModule('http_cookies', 'Cookie', 'http.cookies'),
    MovedModule('html_entities', 'htmlentitydefs', 'html.entities'),
    MovedModule('html_parser', 'HTMLParser', 'html.parser'),
    MovedModule('http_client', 'httplib', 'http.client'),
    MovedModule('email_mime_base', 'email.MIMEBase', 'email.mime.base'),
    MovedModule('email_mime_image', 'email.MIMEImage', 'email.mime.image'),
    MovedModule('email_mime_multipart', 'email.MIMEMultipart', 'email.mime.multipart'),
    MovedModule('email_mime_nonmultipart', 'email.MIMENonMultipart', 'email.mime.nonmultipart'),
    MovedModule('email_mime_text', 'email.MIMEText', 'email.mime.text'),
    MovedModule('BaseHTTPServer', 'BaseHTTPServer', 'http.server'),
    MovedModule('CGIHTTPServer', 'CGIHTTPServer', 'http.server'),
    MovedModule('SimpleHTTPServer', 'SimpleHTTPServer', 'http.server'),
    MovedModule('cPickle', 'cPickle', 'pickle'),
    MovedModule('queue', 'Queue'),
    MovedModule('reprlib', 'repr'),
    MovedModule('socketserver', 'SocketServer'),
    MovedModule('_thread', 'thread', '_thread'),
    MovedModule('tkinter', 'Tkinter'),
    MovedModule('tkinter_dialog', 'Dialog', 'tkinter.dialog'),
    MovedModule('tkinter_filedialog', 'FileDialog', 'tkinter.filedialog'),
    MovedModule('tkinter_scrolledtext', 'ScrolledText', 'tkinter.scrolledtext'),
    MovedModule('tkinter_simpledialog', 'SimpleDialog', 'tkinter.simpledialog'),
    MovedModule('tkinter_tix', 'Tix', 'tkinter.tix'),
    MovedModule('tkinter_ttk', 'ttk', 'tkinter.ttk'),
    MovedModule('tkinter_constants', 'Tkconstants', 'tkinter.constants'),
    MovedModule('tkinter_dnd', 'Tkdnd', 'tkinter.dnd'),
    MovedModule('tkinter_colorchooser', 'tkColorChooser', 'tkinter.colorchooser'),
    MovedModule('tkinter_commondialog', 'tkCommonDialog', 'tkinter.commondialog'),
    MovedModule('tkinter_tkfiledialog', 'tkFileDialog', 'tkinter.filedialog'),
    MovedModule('tkinter_font', 'tkFont', 'tkinter.font'),
    MovedModule('tkinter_messagebox', 'tkMessageBox', 'tkinter.messagebox'),
    MovedModule('tkinter_tksimpledialog', 'tkSimpleDialog', 'tkinter.simpledialog'),
    MovedModule('urllib_parse', __name__ + '.moves.urllib_parse', 'urllib.parse'),
    MovedModule('urllib_error', __name__ + '.moves.urllib_error', 'urllib.error'),
    MovedModule('urllib', __name__ + '.moves.urllib', __name__ + '.moves.urllib'),
    MovedModule('urllib_robotparser', 'robotparser', 'urllib.robotparser'),
    MovedModule('xmlrpc_client', 'xmlrpclib', 'xmlrpc.client'),
    MovedModule('xmlrpc_server', 'SimpleXMLRPCServer', 'xmlrpc.server'),
    MovedModule('winreg', '_winreg') if sys.platform == 'win32',
]
```


## python3.11/site-packages/pip/_vendor/distlib/wheel.py:60
current syntax:
``` python
parts = ['cp', VER_SUFFIX]
if sysconfig.get_config_var('Py_DEBUG'):
    parts.append('d')
```

new syntax:
``` python
parts=[
    'cp',
    VER_SUFFIX,
    'd' if sysconfig.get_config_var('Py_DEBUG'),
]
```


## python3.11/site-packages/pip/_vendor/packaging/version.py:357
current syntax:
``` python
parts = []

# Epoch
if self.epoch != 0:
    parts.append(f"{self.epoch}!")

# Release segment
parts.append(".".join(str(x) for x in self.release))
```

new syntax:
``` python
parts=[
    f'{self.epoch}!' if self.epoch != 0,
    '.'.join((str(x) for x in self.release)),
]
```


## python3.11/site-packages/pip/_vendor/pep517/in_process/_in_process.py:101
current syntax:
``` python
features = []
if hasattr(backend, "build_editable"):
    features.append("build_editable")
```

new syntax:
``` python
features=[
    'build_editable' if hasattr(backend, 'build_editable'),
]
```


## python3.11/site-packages/pip/_vendor/pyparsing/exceptions.py:63
current syntax:
``` python
ret = []
if isinstance(exc, ParseBaseException):
    ret.append(exc.line)
    ret.append(" " * (exc.column - 1) + "^")
ret.append("{}: {}".format(type(exc).__name__, exc))
```

new syntax:
``` python
ret=[
    *[exc.line, ' ' * (exc.column - 1) + '^'] if isinstance(exc, ParseBaseException),
    '{}: {}'.format(type(exc).__name__, exc),
]
```


## python3.11/site-packages/pip/_vendor/urllib3/response.py:189
current syntax:
``` python
CONTENT_DECODERS = ["gzip", "deflate"]
if brotli is not None:
    CONTENT_DECODERS += ["br"]
```

new syntax:
``` python
CONTENT_DECODERS=[
    'gzip',
    'deflate',
    'br' if brotli is not None,
]
```


## python3.11/site-packages/pip/_vendor/urllib3/packages/six.py:250
current syntax:
``` python
_moved_attributes = [
    MovedAttribute("cStringIO", "cStringIO", "io", "StringIO"),
    MovedAttribute("filter", "itertools", "builtins", "ifilter", "filter"),
    MovedAttribute(
        "filterfalse", "itertools", "itertools", "ifilterfalse", "filterfalse"
    ),
    MovedAttribute("input", "__builtin__", "builtins", "raw_input", "input"),
    MovedAttribute("intern", "__builtin__", "sys"),
    MovedAttribute("map", "itertools", "builtins", "imap", "map"),
    MovedAttribute("getcwd", "os", "os", "getcwdu", "getcwd"),
    MovedAttribute("getcwdb", "os", "os", "getcwd", "getcwdb"),
    MovedAttribute("getoutput", "commands", "subprocess"),
    MovedAttribute("range", "__builtin__", "builtins", "xrange", "range"),
    MovedAttribute(
        "reload_module", "__builtin__", "importlib" if PY34 else "imp", "reload"
    ),
    MovedAttribute("reduce", "__builtin__", "functools"),
    MovedAttribute("shlex_quote", "pipes", "shlex", "quote"),
    MovedAttribute("StringIO", "StringIO", "io"),
    MovedAttribute("UserDict", "UserDict", "collections"),
    MovedAttribute("UserList", "UserList", "collections"),
    MovedAttribute("UserString", "UserString", "collections"),
    MovedAttribute("xrange", "__builtin__", "builtins", "xrange", "range"),
    MovedAttribute("zip", "itertools", "builtins", "izip", "zip"),
    MovedAttribute(
        "zip_longest", "itertools", "itertools", "izip_longest", "zip_longest"
    ),
    MovedModule("builtins", "__builtin__"),
    MovedModule("configparser", "ConfigParser"),
    MovedModule(
        "collections_abc",
        "collections",
        "collections.abc" if sys.version_info >= (3, 3) else "collections",
    ),
    MovedModule("copyreg", "copy_reg"),
    MovedModule("dbm_gnu", "gdbm", "dbm.gnu"),
    MovedModule("dbm_ndbm", "dbm", "dbm.ndbm"),
    MovedModule(
        "_dummy_thread",
        "dummy_thread",
        "_dummy_thread" if sys.version_info < (3, 9) else "_thread",
    ),
    MovedModule("http_cookiejar", "cookielib", "http.cookiejar"),
    MovedModule("http_cookies", "Cookie", "http.cookies"),
    MovedModule("html_entities", "htmlentitydefs", "html.entities"),
    MovedModule("html_parser", "HTMLParser", "html.parser"),
    MovedModule("http_client", "httplib", "http.client"),
    MovedModule("email_mime_base", "email.MIMEBase", "email.mime.base"),
    MovedModule("email_mime_image", "email.MIMEImage", "email.mime.image"),
    MovedModule("email_mime_multipart", "email.MIMEMultipart", "email.mime.multipart"),
    MovedModule(
        "email_mime_nonmultipart", "email.MIMENonMultipart", "email.mime.nonmultipart"
    ),
    MovedModule("email_mime_text", "email.MIMEText", "email.mime.text"),
    MovedModule("BaseHTTPServer", "BaseHTTPServer", "http.server"),
    MovedModule("CGIHTTPServer", "CGIHTTPServer", "http.server"),
    MovedModule("SimpleHTTPServer", "SimpleHTTPServer", "http.server"),
    MovedModule("cPickle", "cPickle", "pickle"),
    MovedModule("queue", "Queue"),
    MovedModule("reprlib", "repr"),
    MovedModule("socketserver", "SocketServer"),
    MovedModule("_thread", "thread", "_thread"),
    MovedModule("tkinter", "Tkinter"),
    MovedModule("tkinter_dialog", "Dialog", "tkinter.dialog"),
    MovedModule("tkinter_filedialog", "FileDialog", "tkinter.filedialog"),
    MovedModule("tkinter_scrolledtext", "ScrolledText", "tkinter.scrolledtext"),
    MovedModule("tkinter_simpledialog", "SimpleDialog", "tkinter.simpledialog"),
    MovedModule("tkinter_tix", "Tix", "tkinter.tix"),
    MovedModule("tkinter_ttk", "ttk", "tkinter.ttk"),
    MovedModule("tkinter_constants", "Tkconstants", "tkinter.constants"),
    MovedModule("tkinter_dnd", "Tkdnd", "tkinter.dnd"),
    MovedModule("tkinter_colorchooser", "tkColorChooser", "tkinter.colorchooser"),
    MovedModule("tkinter_commondialog", "tkCommonDialog", "tkinter.commondialog"),
    MovedModule("tkinter_tkfiledialog", "tkFileDialog", "tkinter.filedialog"),
    MovedModule("tkinter_font", "tkFont", "tkinter.font"),
    MovedModule("tkinter_messagebox", "tkMessageBox", "tkinter.messagebox"),
    MovedModule("tkinter_tksimpledialog", "tkSimpleDialog", "tkinter.simpledialog"),
    MovedModule("urllib_parse", __name__ + ".moves.urllib_parse", "urllib.parse"),
    MovedModule("urllib_error", __name__ + ".moves.urllib_error", "urllib.error"),
    MovedModule("urllib", __name__ + ".moves.urllib", __name__ + ".moves.urllib"),
    MovedModule("urllib_robotparser", "robotparser", "urllib.robotparser"),
    MovedModule("xmlrpc_client", "xmlrpclib", "xmlrpc.client"),
    MovedModule("xmlrpc_server", "SimpleXMLRPCServer", "xmlrpc.server"),
]
# Add windows specific modules.
if sys.platform == "win32":
    _moved_attributes += [
        MovedModule("winreg", "_winreg"),
```

new syntax:
``` python
_moved_attributes=[
    MovedAttribute('cStringIO', 'cStringIO', 'io', 'StringIO'),
    MovedAttribute('filter', 'itertools', 'builtins', 'ifilter', 'filter'),
    MovedAttribute('filterfalse', 'itertools', 'itertools', 'ifilterfalse', 'filterfalse'),
    MovedAttribute('input', '__builtin__', 'builtins', 'raw_input', 'input'),
    MovedAttribute('intern', '__builtin__', 'sys'),
    MovedAttribute('map', 'itertools', 'builtins', 'imap', 'map'),
    MovedAttribute('getcwd', 'os', 'os', 'getcwdu', 'getcwd'),
    MovedAttribute('getcwdb', 'os', 'os', 'getcwd', 'getcwdb'),
    MovedAttribute('getoutput', 'commands', 'subprocess'),
    MovedAttribute('range', '__builtin__', 'builtins', 'xrange', 'range'),
    MovedAttribute('reload_module', '__builtin__', 'importlib' if PY34 else 'imp', 'reload'),
    MovedAttribute('reduce', '__builtin__', 'functools'),
    MovedAttribute('shlex_quote', 'pipes', 'shlex', 'quote'),
    MovedAttribute('StringIO', 'StringIO', 'io'),
    MovedAttribute('UserDict', 'UserDict', 'collections'),
    MovedAttribute('UserList', 'UserList', 'collections'),
    MovedAttribute('UserString', 'UserString', 'collections'),
    MovedAttribute('xrange', '__builtin__', 'builtins', 'xrange', 'range'),
    MovedAttribute('zip', 'itertools', 'builtins', 'izip', 'zip'),
    MovedAttribute('zip_longest', 'itertools', 'itertools', 'izip_longest', 'zip_longest'),
    MovedModule('builtins', '__builtin__'),
    MovedModule('configparser', 'ConfigParser'),
    MovedModule('collections_abc', 'collections', 'collections.abc' if sys.version_info >= (3, 3) else 'collections'),
    MovedModule('copyreg', 'copy_reg'),
    MovedModule('dbm_gnu', 'gdbm', 'dbm.gnu'),
    MovedModule('dbm_ndbm', 'dbm', 'dbm.ndbm'),
    MovedModule('_dummy_thread', 'dummy_thread', '_dummy_thread' if sys.version_info < (3, 9) else '_thread'),
    MovedModule('http_cookiejar', 'cookielib', 'http.cookiejar'),
    MovedModule('http_cookies', 'Cookie', 'http.cookies'),
    MovedModule('html_entities', 'htmlentitydefs', 'html.entities'),
    MovedModule('html_parser', 'HTMLParser', 'html.parser'),
    MovedModule('http_client', 'httplib', 'http.client'),
    MovedModule('email_mime_base', 'email.MIMEBase', 'email.mime.base'),
    MovedModule('email_mime_image', 'email.MIMEImage', 'email.mime.image'),
    MovedModule('email_mime_multipart', 'email.MIMEMultipart', 'email.mime.multipart'),
    MovedModule('email_mime_nonmultipart', 'email.MIMENonMultipart', 'email.mime.nonmultipart'),
    MovedModule('email_mime_text', 'email.MIMEText', 'email.mime.text'),
    MovedModule('BaseHTTPServer', 'BaseHTTPServer', 'http.server'),
    MovedModule('CGIHTTPServer', 'CGIHTTPServer', 'http.server'),
    MovedModule('SimpleHTTPServer', 'SimpleHTTPServer', 'http.server'),
    MovedModule('cPickle', 'cPickle', 'pickle'),
    MovedModule('queue', 'Queue'),
    MovedModule('reprlib', 'repr'),
    MovedModule('socketserver', 'SocketServer'),
    MovedModule('_thread', 'thread', '_thread'),
    MovedModule('tkinter', 'Tkinter'),
    MovedModule('tkinter_dialog', 'Dialog', 'tkinter.dialog'),
    MovedModule('tkinter_filedialog', 'FileDialog', 'tkinter.filedialog'),
    MovedModule('tkinter_scrolledtext', 'ScrolledText', 'tkinter.scrolledtext'),
    MovedModule('tkinter_simpledialog', 'SimpleDialog', 'tkinter.simpledialog'),
    MovedModule('tkinter_tix', 'Tix', 'tkinter.tix'),
    MovedModule('tkinter_ttk', 'ttk', 'tkinter.ttk'),
    MovedModule('tkinter_constants', 'Tkconstants', 'tkinter.constants'),
    MovedModule('tkinter_dnd', 'Tkdnd', 'tkinter.dnd'),
    MovedModule('tkinter_colorchooser', 'tkColorChooser', 'tkinter.colorchooser'),
    MovedModule('tkinter_commondialog', 'tkCommonDialog', 'tkinter.commondialog'),
    MovedModule('tkinter_tkfiledialog', 'tkFileDialog', 'tkinter.filedialog'),
    MovedModule('tkinter_font', 'tkFont', 'tkinter.font'),
    MovedModule('tkinter_messagebox', 'tkMessageBox', 'tkinter.messagebox'),
    MovedModule('tkinter_tksimpledialog', 'tkSimpleDialog', 'tkinter.simpledialog'),
    MovedModule('urllib_parse', __name__ + '.moves.urllib_parse', 'urllib.parse'),
    MovedModule('urllib_error', __name__ + '.moves.urllib_error', 'urllib.error'),
    MovedModule('urllib', __name__ + '.moves.urllib', __name__ + '.moves.urllib'),
    MovedModule('urllib_robotparser', 'robotparser', 'urllib.robotparser'),
    MovedModule('xmlrpc_client', 'xmlrpclib', 'xmlrpc.client'),
    MovedModule('xmlrpc_server', 'SimpleXMLRPCServer', 'xmlrpc.server'),
    MovedModule('winreg', '_winreg') if sys.platform == 'win32',
]
```


## python3.11/unittest/case.py:1459
current syntax:
``` python
parts = []
if self._message is not _subtest_msg_sentinel:
    parts.append("[{}]".format(self._message))
```

new syntax:
``` python
parts=[
    '[{}]'.format(self._message) if self._message is not _subtest_msg_sentinel,
]
```


## python3.11/unittest/test/test_result.py:17
current syntax:
``` python
result = ['A traceback']
if self.capture_locals:
    result.append('locals')
```

new syntax:
``` python
result=[
    'A traceback',
    'locals' if self.capture_locals,
]
```


## python3.11/urllib/request.py:579
current syntax:
``` python
default_classes = [ProxyHandler, UnknownHandler, HTTPHandler,
                   HTTPDefaultErrorHandler, HTTPRedirectHandler,
                   FTPHandler, FileHandler, HTTPErrorProcessor,
                   DataHandler]
if hasattr(http.client, "HTTPSConnection"):
    default_classes.append(HTTPSHandler)
```

new syntax:
``` python
default_classes=[
    ProxyHandler,
    UnknownHandler,
    HTTPHandler,
    HTTPDefaultErrorHandler,
    HTTPRedirectHandler,
    FTPHandler,
    FileHandler,
    HTTPErrorProcessor,
    DataHandler,
    HTTPSHandler if hasattr(http.client, 'HTTPSConnection'),
]
```


## python3.11/test/_test_embed_set_config.py:55
current syntax:
``` python
options = [
    '_config_init',
    'isolated',
    'use_environment',
    'dev_mode',
    'install_signal_handlers',
    'use_hash_seed',
    'faulthandler',
    'tracemalloc',
    'import_time',
    'code_debug_ranges',
    'show_ref_count',
    'dump_refs',
    'malloc_stats',
    'parse_argv',
    'site_import',
    'bytes_warning',
    'inspect',
    'interactive',
    'optimization_level',
    'parser_debug',
    'write_bytecode',
    'verbose',
    'quiet',
    'user_site_directory',
    'configure_c_stdio',
    'buffered_stdio',
    'pathconfig_warnings',
    'module_search_paths_set',
    'skip_source_first_line',
    '_install_importlib',
    '_init_main',
    '_isolated_interpreter',
]
if MS_WINDOWS:
    options.append('legacy_windows_stdio')
```

new syntax:
``` python
options=[
    '_config_init',
    'isolated',
    'use_environment',
    'dev_mode',
    'install_signal_handlers',
    'use_hash_seed',
    'faulthandler',
    'tracemalloc',
    'import_time',
    'code_debug_ranges',
    'show_ref_count',
    'dump_refs',
    'malloc_stats',
    'parse_argv',
    'site_import',
    'bytes_warning',
    'inspect',
    'interactive',
    'optimization_level',
    'parser_debug',
    'write_bytecode',
    'verbose',
    'quiet',
    'user_site_directory',
    'configure_c_stdio',
    'buffered_stdio',
    'pathconfig_warnings',
    'module_search_paths_set',
    'skip_source_first_line',
    '_install_importlib',
    '_init_main',
    '_isolated_interpreter',
    'legacy_windows_stdio' if MS_WINDOWS,
]
```


## python3.11/test/_test_embed_structseq.py:40
current syntax:
``` python
func_names = ['get_asyncgen_hooks']  # AsyncGenHooksType
if hasattr(sys, 'getwindowsversion'):
    func_names.append('getwindowsversion')  # WindowsVersionType
```

new syntax:
``` python
func_names=[
    'get_asyncgen_hooks',
    'getwindowsversion' if hasattr(sys, 'getwindowsversion'),
]
```


## python3.11/test/_test_multiprocessing.py:648
current syntax:
``` python
exitcodes = [-signal.SIGTERM]
if sys.platform == 'darwin':
    # bpo-31510: On macOS, killing a freshly started process with
    # SIGTERM sometimes kills the process with SIGKILL.
    exitcodes.append(-signal.SIGKILL)
```

new syntax:
``` python
exitcodes=[
    -signal.SIGTERM,
    -signal.SIGKILL if sys.platform == 'darwin',
]
```


## python3.11/test/test_codecs.py:2335
current syntax:
``` python
decoders = [
    codecs.utf_7_decode,
    codecs.utf_8_decode,
    codecs.utf_16_le_decode,
    codecs.utf_16_be_decode,
    codecs.utf_16_ex_decode,
    codecs.utf_32_decode,
    codecs.utf_32_le_decode,
    codecs.utf_32_be_decode,
    codecs.utf_32_ex_decode,
    codecs.latin_1_decode,
    codecs.ascii_decode,
    codecs.charmap_decode,
]
if hasattr(codecs, "mbcs_decode"):
    decoders.append(codecs.mbcs_decode)
```

new syntax:
``` python
decoders=[
    codecs.utf_7_decode,
    codecs.utf_8_decode,
    codecs.utf_16_le_decode,
    codecs.utf_16_be_decode,
    codecs.utf_16_ex_decode,
    codecs.utf_32_decode,
    codecs.utf_32_le_decode,
    codecs.utf_32_be_decode,
    codecs.utf_32_ex_decode,
    codecs.latin_1_decode,
    codecs.ascii_decode,
    codecs.charmap_decode,
    codecs.mbcs_decode if hasattr(codecs, 'mbcs_decode'),
]
```


## python3.11/test/test_compileall.py:924
current syntax:
``` python
args = ["-q", "-o 0", "-o 1", "-o 2"]
if dedup:
    args.append("--hardlink-dupes")
```

new syntax:
``` python
args=[
    '-q',
    '-o 0',
    '-o 1',
    '-o 2',
    '--hardlink-dupes' if dedup,
]
```


## python3.11/test/test_configparser.py:73
current syntax:
``` python
E = ['Commented Bar',
     'Foo Bar',
     'Internationalized Stuff',
     'Long Line',
     'Section\\with$weird%characters[\t',
     'Spaces',
     'Spacey Bar',
     'Spacey Bar From The Beginning',
     'Types',
     'This One Has A ] In It',
     ]

if self.allow_no_value:
    E.append('NoValue')
```

new syntax:
``` python
E=[
    'Commented Bar',
    'Foo Bar',
    'Internationalized Stuff',
    'Long Line',
    'Section\\with$weird%characters[\t',
    'Spaces',
    'Spacey Bar',
    'Spacey Bar From The Beginning',
    'Types',
    'This One Has A ] In It',
    'NoValue' if self.allow_no_value,
]
```


## python3.11/test/test_cppext.py:76
current syntax:
``` python
cmd = [python, '-X', 'dev',
       SETUP_TESTCPPEXT, 'build_ext', '--verbose']
if std_cpp03:
    cmd.append('-std=c++03')
```

new syntax:
``` python
cmd=[
    python,
    '-X',
    'dev',
    SETUP_TESTCPPEXT,
    'build_ext',
    '--verbose',
    '-std=c++03' if std_cpp03,
]
```


## python3.11/test/test_faulthandler.py:64
current syntax:
``` python
pass_fds = []
if fd is not None:
    pass_fds.append(fd)
```

new syntax:
``` python
pass_fds=[
    fd if fd is not None,
]
```


## python3.11/test/test_gdb.py:176
current syntax:
``` python
commands = ['set breakpoint pending yes',
            'break %s' % breakpoint,

            # The tests assume that the first frame of printed
            #  backtrace will not contain program counter,
            #  that is however not guaranteed by gdb
            #  therefore we need to use 'set print address off' to
            #  make sure the counter is not there. For example:
            # #0 in PyObject_Print ...
            #  is assumed, but sometimes this can be e.g.
            # #0 0x00003fffb7dd1798 in PyObject_Print ...
            'set print address off',

            'run']

# GDB as of 7.4 onwards can distinguish between the
# value of a variable at entry vs current value:
#   http://sourceware.org/gdb/onlinedocs/gdb/Variables.html
# which leads to the selftests failing with errors like this:
#   AssertionError: 'v@entry=()' != '()'
# Disable this:
if (gdb_major_version, gdb_minor_version) >= (7, 4):
    commands += ['set print entry-values no']
```

new syntax:
``` python
commands=[
    'set breakpoint pending yes',
    'break %s' % breakpoint,
    'set print address off',
    'run',
    'set print entry-values no' if (gdb_major_version, gdb_minor_version) >= (7, 4),
]
```


## python3.11/test/test_gdb.py:970
current syntax:
``` python
cmds_after_breakpoint = ['break wrapper_call', 'continue']
if CET_PROTECTION:
    # bpo-32962: same case as in get_stack_trace():
    # we need an additional 'next' command in order to read
    # arguments of the innermost function of the call stack.
    cmds_after_breakpoint.append('next')
cmds_after_breakpoint.append('py-bt')
```

new syntax:
``` python
cmds_after_breakpoint=[
    'break wrapper_call',
    'continue',
    'next' if CET_PROTECTION,
    'py-bt',
]
```


## python3.11/test/test_glob.py:268
current syntax:
``` python
full = [('EF',), ('ZZZ',),
        ('a',), ('a', 'D'),
        ('a', 'bcd'),
        ('a', 'bcd', 'EF'),
        ('a', 'bcd', 'efg'),
        ('a', 'bcd', 'efg', 'ha'),
        ('aaa',), ('aaa', 'zzzF'),
        ('aab',), ('aab', 'F'),
       ]
if can_symlink():
    full += [('sym1',), ('sym2',),
             ('sym3',),
             ('sym3', 'EF'),
             ('sym3', 'efg'),
             ('sym3', 'efg', 'ha'),
```

new syntax:
``` python
full=[
    ('EF',),
    ('ZZZ',),
    ('a',),
    ('a', 'D'),
    ('a', 'bcd'),
    ('a', 'bcd', 'EF'),
    ('a', 'bcd', 'efg'),
    ('a', 'bcd', 'efg', 'ha'),
    ('aaa',),
    ('aaa', 'zzzF'),
    ('aab',),
    ('aab', 'F'),
    *[('sym1',), ('sym2',), ('sym3',), ('sym3', 'EF'), ('sym3', 'efg'), ('sym3', 'efg', 'ha')] if can_symlink(),
]
```


## python3.11/test/test_glob.py:287
current syntax:
``` python
dirs = [('a', ''), ('a', 'bcd', ''), ('a', 'bcd', 'efg', ''),
        ('aaa', ''), ('aab', '')]
if can_symlink():
    dirs += [('sym3', ''), ('sym3', 'efg', '')]
```

new syntax:
``` python
dirs=[
    ('a', ''),
    ('a', 'bcd', ''),
    ('a', 'bcd', 'efg', ''),
    ('aaa', ''),
    ('aab', ''),
    *[('sym3', ''), ('sym3', 'efg', '')] if can_symlink(),
]
```


## python3.11/test/test_glob.py:297
current syntax:
``` python
expect = [('a', 'bcd', 'EF'), ('EF',)]
if can_symlink():
    expect += [('sym3', 'EF')]
```

new syntax:
``` python
expect=[
    ('a', 'bcd', 'EF'),
    ('EF',),
    ('sym3', 'EF') if can_symlink(),
]
```


## python3.11/test/test_glob.py:301
current syntax:
``` python
expect = [('a', 'bcd', 'EF'), ('aaa', 'zzzF'), ('aab', 'F'), ('EF',)]
if can_symlink():
    expect += [('sym3', 'EF')]
```

new syntax:
``` python
expect=[
    ('a', 'bcd', 'EF'),
    ('aaa', 'zzzF'),
    ('aab', 'F'),
    ('EF',),
    ('sym3', 'EF') if can_symlink(),
]
```


## python3.11/test/test_glob.py:326
current syntax:
``` python
expect = [join('a', 'bcd', 'EF'), 'EF']
if can_symlink():
    expect += [join('sym3', 'EF')]
```

new syntax:
``` python
expect=[
    join('a', 'bcd', 'EF'),
    'EF',
    join('sym3', 'EF') if can_symlink(),
]
```


## python3.11/test/test_nntplib.py:1489
current syntax:
``` python
target_api = ['NNTP', 'NNTPError', 'NNTPReplyError',
              'NNTPTemporaryError', 'NNTPPermanentError',
              'NNTPProtocolError', 'NNTPDataError', 'decode_header']
if ssl is not None:
    target_api.append('NNTP_SSL')
```

new syntax:
``` python
target_api=[
    'NNTP',
    'NNTPError',
    'NNTPReplyError',
    'NNTPTemporaryError',
    'NNTPPermanentError',
    'NNTPProtocolError',
    'NNTPDataError',
    'decode_header',
    'NNTP_SSL' if ssl is not None,
]
```


## python3.11/test/test_os.py:4194
current syntax:
``` python
names = ['dir', 'file.txt']
if link:
    names.append('link_file.txt')
```

new syntax:
``` python
names=[
    'dir',
    'file.txt',
    'link_file.txt' if link,
]
```


## python3.11/test/test_pathlib.py:1623
current syntax:
``` python
expected = ['dirA', 'dirB', 'dirC', 'dirE', 'fileA']
if os_helper.can_symlink():
    expected += ['linkA', 'linkB', 'brokenLink', 'brokenLinkLoop']
```

new syntax:
``` python
expected=[
    'dirA',
    'dirB',
    'dirC',
    'dirE',
    'fileA',
    *['linkA', 'linkB', 'brokenLink', 'brokenLinkLoop'] if os_helper.can_symlink(),
]
```


## python3.11/test/test_shutil.py:2701
current syntax:
``` python
target_api = ['copyfileobj', 'copyfile', 'copymode', 'copystat',
              'copy', 'copy2', 'copytree', 'move', 'rmtree', 'Error',
              'SpecialFileError', 'ExecError', 'make_archive',
              'get_archive_formats', 'register_archive_format',
              'unregister_archive_format', 'get_unpack_formats',
              'register_unpack_format', 'unregister_unpack_format',
              'unpack_archive', 'ignore_patterns', 'chown', 'which',
              'get_terminal_size', 'SameFileError']
if hasattr(os, 'statvfs') or os.name == 'nt':
    target_api.append('disk_usage')
```

new syntax:
``` python
target_api=[
    'copyfileobj',
    'copyfile',
    'copymode',
    'copystat',
    'copy',
    'copy2',
    'copytree',
    'move',
    'rmtree',
    'Error',
    'SpecialFileError',
    'ExecError',
    'make_archive',
    'get_archive_formats',
    'register_archive_format',
    'unregister_archive_format',
    'get_unpack_formats',
    'register_unpack_format',
    'unregister_unpack_format',
    'unpack_archive',
    'ignore_patterns',
    'chown',
    'which',
    'get_terminal_size',
    'SameFileError',
    'disk_usage' if hasattr(os, 'statvfs') or os.name == 'nt',
]
```


## python3.11/test/test_statistics.py:657
current syntax:
``` python
substrings = [
        'tol=%r' % tol,
        'rel=%r' % rel,
        'absolute error = %r' % abs_err,
        'relative error = %r' % rel_err,
        ]
if idx is not None:
    substrings.append('differ at index %d' % idx)
```

new syntax:
``` python
substrings=[
    'tol=%r' % tol,
    'rel=%r' % rel,
    'absolute error = %r' % abs_err,
    'relative error = %r' % rel_err,
    'differ at index %d' % idx if idx is not None,
]
```


## python3.11/test/test_sys.py:831
current syntax:
``` python
args = [sys.executable, "-X", "utf8=0", "-c", code]
if isolated:
    args.append("-I")
```

new syntax:
``` python
args=[
    sys.executable,
    '-X',
    'utf8=0',
    '-c',
    code,
    '-I' if isolated,
]
```


## python3.11/test/test_time.py:565
current syntax:
``` python
clocks = [
    'monotonic',
    'perf_counter',
    'process_time',
    'time',
]
if hasattr(time, 'thread_time'):
    clocks.append('thread_time')
```

new syntax:
``` python
clocks=[
    'monotonic',
    'perf_counter',
    'process_time',
    'time',
    'thread_time' if hasattr(time, 'thread_time'),
]
```


## python3.11/test/test_time.py:783
current syntax:
``` python
units = [1, US_TO_NS, MS_TO_NS, SEC_TO_NS]
if use_float:
    # picoseconds are only tested to pytime_converter accepting floats
    units.append(1e-3)
```

new syntax:
``` python
units=[
    1,
    US_TO_NS,
    MS_TO_NS,
    SEC_TO_NS,
    0.001 if use_float,
]
```


## python3.11/test/support/script_helper.py:187
current syntax:
``` python
cmd_line = [sys.executable]
if not interpreter_requires_environment():
    cmd_line.append('-E')
```

new syntax:
``` python
cmd_line=[
    sys.executable,
    '-E' if not interpreter_requires_environment(),
]
```


## python3.11/test/test_warnings/__init__.py:492
current syntax:
``` python
filenames = ["nonascii\xe9\u20ac"]
if not support.is_emscripten:
    # JavaScript does not like surrogates.
    # Invalid UTF-8 leading byte 0x80 encountered when
    # deserializing a UTF-8 string in wasm memory to a JS
    # string!
    filenames.append("surrogate\udc80")
```

new syntax:
``` python
filenames=[
    'nonasciié€',
    'surrogate\udc80' if not support.is_emscripten,
]
```
