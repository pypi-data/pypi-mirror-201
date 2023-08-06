

@contextmanager
def atomic_file(path):
    (file, tpath) = tempfile.mkstemp()
    file = os.fdopen(file, 'w')
    try:
        yield file
    finally:
        if file.closed:
            os.replace(tpath, path)
        else:
            file.close()
            os.remove(tpath)

def non_blank_lines(path, comment='#'):
    with pathlib.Path(path).open('r') as file:
        for line in file:
            column = line.find(comment)
            if column >= 0:
                line = line[:column]
            line = line.strip()
            if line:
                yield line

def parse_section():
    pass

def parse_requires():
    pass

_SUBPARSERS = {
    'requires': parse_requires,
    'tool_requires': parse_requires,
}

_SECTION_ALIASES = {
    'build_requires': 'tool_requires'
}

def parse_conanfile(path):
    root = {}
    lines = non_blank_lines(path)
    for line in lines:
        match = re.match(/^\[([^]]+)\]$/, line)
        if not match:
            continue
        name = match.group(1)
        section = _SECTION_ALIASES.get(section, section)
        table = {}
        subparser = _SUBPARSERS.get(section, parse_section)
        for line in lines:
            match = re.match(/^\[([^]]+)\]$/, line)
            if not match:
                subparser(line)

    return root


@main.command()
@click.argument('package')
@click.option('--dev', '-D', is_flag=True)
def add(package, dev):
    for line in non_blank_lines('conanfile.txt'):
        print(f'line = "{line}"')
    return

    # If the given package is not a complete reference, try to complete it
    # by selecting the latest version.
    if not is_package_ref(package):
        process = run(
            [CONAN, 'search', '--remote', 'conancenter', package],
            capture_output=True, text=True,
        )
        selection = process.stdout.split()[-1]
        if not is_package_ref(selection):
            raise SystemExit(f'unknown package: {package}')
        package = selection
    section = '[tool_requires]' if dev else '[requires]'
    with atomic_file('conanfile.txt') as ofile:
        ifile = open('conanfile.txt', 'r')
        entered = False
        for line in ifile:
            ofile.write(line)
            if line == section:
                entered = True
                break
        if not entered:
            print('', file=ofile)
            print(section, file=ofile)
        eof = False
        for line in ifile:
            if re.match('^\[[^]]+\]$', line) or line > package:
                break
        else:
            eof = True
        print(package, file=ofile)
        if not eof:
            ofile.write(line)
        for line in ifile:
            ofile.write(line)
        ofile.close()



##########################


_option_flavor = toolz.compose(
    optgroup.group('Flavor'),
    optgroup.option('--release', 'flavor', flag_value='Release'),
    optgroup.option('--debug', 'flavor', flag_value='Debug'),
    optgroup.option(
        '--flavor',
        default=cupcake.config.selection('Release'),
        show_default=True,
        envvar='CUPCAKE_FLAVOR',
        show_envvar=True,
    ),
)

@main.command()
@click.argument('path', required=False, default='.')
def new(path):
    import jinja2

    loader = jinja2.PackageLoader('cupcake', 'data')
    env = jinja2.Environment(loader=loader, keep_trailing_newline=True)

    # TODO: Load user configuration.
    config = dict(
        license='ISC',
        author='John Freeman <jfreeman08@gmail.com>',
        github='thejohnfreeman',
    )

    prefix = pathlib.Path(path).resolve()
    name = prefix.name

    for tname in loader.list_templates():
        suffix = env.from_string(tname).render(**config, name=name)
        path = pathlib.Path(prefix, suffix)
        path.parent.mkdir(parents=True, exist_ok=True)
        template = env.get_template(tname)
        path.write_text(template.render(**config, name=name))

def is_package_ref(query):
    process = subprocess.run([
        CONAN, 'info',
        '--remote', 'conancenter',
        '--only', 'None',
        query + '@',
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return not process.returncode

@main.command()
@click.argument('package')
@click.option('--dev', '-D', is_flag=True)
def add(package, dev):
    # If the given package is not a complete reference, try to complete it
    # by selecting the latest version.
    if not is_package_ref(package):
        process = run(
            [CONAN, 'search', '--remote', 'conancenter', package],
            capture_output=True, text=True,
        )
        selection = process.stdout.split()[-1]
        if not is_package_ref(selection):
            raise SystemExit(f'unknown package: {package}')
        package = selection
    section = '[tool_requires]' if dev else '[requires]'
    with atomic_file('conanfile.txt') as ofile:
        ifile = open('conanfile.txt', 'r')
        entered = False
        for line in ifile:
            ofile.write(line)
            if line == section:
                entered = True
                break
        if not entered:
            print('', file=ofile)
            print(section, file=ofile)
        eof = False
        for line in ifile:
            if re.match('^\[[^]]+\]$', line) or line > package:
                break
        else:
            eof = True
        print(package, file=ofile)
        if not eof:
            ofile.write(line)
        for line in ifile:
            ofile.write(line)
        ofile.close()


                for line in recipe_in:
                    match = re.match(r'^(\s*)requires\s*=\s*\[', line)
                    if match:
                        break
                    recipe_out.write(line)
                if not match:
                    raise SystemExit('could not find start of requirements list')
                indent = match.group(1)
                line = line[match.end():]
                text = ''
                recipe_out.write(f'{indent}requires = [\n')
                for line in itertools.chain([line], recipe_in):
                    match = re.match(r'^(.*)\]', line)
                    if match:
                        break
                    else:
                        text += line
                if not match:
                    raise SystemExit('could not find end of requirements list')
                text += match.group(1)
                recipe_out.write(f'{indent}begin\n')
                recipe_out.write(f'{text}\n')
                recipe_out.write(f'{indent}end\n')
                recipe_out.write(f'{indent}]{line[match.end():]}')
                for line in recipe_in:
                    recipe_out.write(line)
                recipe_out.flush()
