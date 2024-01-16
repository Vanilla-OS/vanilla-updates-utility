pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'updates_utility')
gnome = import('gnome')

gnome.compile_resources('updates_utility',
  'updates-utility.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'vanilla-updates-utility.in',
  output: 'vanilla-updates-utility',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

subdir('windows')
subdir('utils')

updates_utility_sources = [
  '__init__.py',
  'main.py',
]

install_data(updates_utility_sources, install_dir: moduledir)
