from setuptools import setup, Extension
import os
#from VerifyOwner.version import __version__

Vf_c=Extension(
    name='VerifyOwner.VerifyOwnerF',
    sources=['VerifyOwnerF.m'],
    extra_compile_args=['-ObjC++'],
    extra_link_args=['-framework','Cocoa','-framework','LocalAuthentication'],
    libraries=[]
)

rd=open(os.path.join(os.path.dirname(__file__),'README.md')).read()

setup(
    name='VerifyOwner',
    version='1.0.1',
    author='AliebcX',
    author_email='aliebcx@outlook.com',
    url='https://github.com/Aliebc/VerifyOwner',
    ext_modules=[Vf_c],
    description='A package to verify owner by Touch ID',
    license='MIT LICENSE',
    long_description=rd,
    packages=['VerifyOwner'],
    platforms=['Darwin'],
)