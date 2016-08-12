# coding=utf-8
import os
import tempfile

from destral.testing import get_spec_suite, run_spec_suite
from destral.patch import RestorePatchedRegisterAll
from expects import *
from doublex_expects import *
from doublex import Spy, method_returning
from mamba.runners import BaseRunner
from mamba.reporter import Reporter

with description('Fixture#Mamba support'):
    with it('has to create a runner if spec directory is present'):
        module = tempfile.mkdtemp()

        suite = get_spec_suite(module)
        expect(suite).to(be(None))

        spec_dir = os.path.join(module, 'spec')
        os.mkdir(spec_dir)
        suite = get_spec_suite(module)
        expect(suite).to(be_a(BaseRunner))

    with it('has to run the tests found in spec directory'):
        module = tempfile.mkdtemp()
        spec_dir = os.path.join(module, 'spec')
        os.mkdir(spec_dir)
        suite = get_spec_suite(module)
        suite = Spy(suite)
        suite.run = method_returning(True)
        result = run_spec_suite(suite)
        expect(result).to(be_a(Reporter))
        expect(suite.run).to(have_been_called)


with description('When running tests'):
    with it('must be reload report.interface'):
        import report

        orig = id(report.interface.register_all)

        def new_register_all(db):
            pass

        with RestorePatchedRegisterAll():

            report.interface.register_all = new_register_all
            expect(id(report.interface.register_all)).to(
                equal(id(new_register_all))
            )

        expect(id(report.interface.register_all)).to(equal(orig))

