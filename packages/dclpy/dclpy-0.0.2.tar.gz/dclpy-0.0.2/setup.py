import subprocess
from distutils.core import setup, Extension

packagename = "dclpy"

result = subprocess.call("dclconfig --ldlibs", shell=True)

setup(
    name='dclpy',
    version='0.0.2',
    ext_modules = [
        Extension(
            'dclpy',
            ['dclpy/dclpy_wrapper.c'],
    libraries=['f77dcl751','gtk-3','gdk-3','pangocairo-1.0',
               'pango-1.0','harfbuzz','atk-1.0','cairo-gobject','cairo',
               'gdk_pixbuf-2.0','gio-2.0','gobject-2.0','glib-2.0','m','gfortran'],
        ),
    ],
)
