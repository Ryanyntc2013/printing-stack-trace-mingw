import doozer

project('stack_trace')

# Variables
flags = needvar('stack_trace.flags', 'flags', description='list of abstract build flags (see doozer docs)')
platform = needvar('stack_trace.platform', description='"windows" or "osx"')


# Builds a static library for stack_trace.
@target
def staticlib(kit):
    opt = kit.cpp.opt(*flags)
    opt.sources += here/'src/*.cpp'
    opt.includes += [here/'include']

    syslibs = []

    if platform == 'windows':
        if 'msvc' in kit.installed():
            opt.cppflags -= ['/Za']

        syslibs = ['imagehlp']

        if 'gpp' in kit.installed():
            syslibs += ['bfd', 'iberty', 'intl', 'iconv']

    return properties(
        libs = [kit.cpp.lib('stack_trace', opt)],
        includes = [here/'include'],
        syslibs = syslibs
    )

@target
def example(kit):
    stack_trace = staticlib(kit)

    opt = kit.cpp.opt(*flags)

    opt.sources += here/'example/*.cpp'
    opt.includes += stack_trace.includes
    opt.libs += stack_trace.libs
    opt.syslibs += stack_trace.syslibs

    return kit.cpp.exe('example', opt)
