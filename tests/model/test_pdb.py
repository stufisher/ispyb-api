from __future__ import absolute_import, division, print_function

import ispyb.model.pdb
import mock
import pytest

def test_pdb_values_are_immutable():
  P = ispyb.model.pdb.PDB()
  with pytest.raises(AttributeError):
    P.name = 'test'
  with pytest.raises(AttributeError):
    P.rawfile = 'test'
  with pytest.raises(AttributeError):
    P.code = 'test'

def test_pdb_values_can_be_read_back():
  P = ispyb.model.pdb.PDB(name=mock.sentinel.name, rawfile=mock.sentinel.rawfile, code=mock.sentinel.code)
  assert P.name == mock.sentinel.name
  assert P.rawfile == mock.sentinel.rawfile
  assert P.code == mock.sentinel.code

def test_pdb_object_representation():
  P = ispyb.model.pdb.PDB(name='somename', rawfile='x'*100, code='somecode')
  assert repr(P) == '<PDB somename>'
  assert 'somename' in str(P)
  assert '100 bytes' in str(P)
  assert 'xxxxxxxxx' not in str(P)
  assert 'somecode' in str(P)
