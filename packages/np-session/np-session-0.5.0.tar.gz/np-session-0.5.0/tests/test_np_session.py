import doctest

import np_session
from np_session import *

doctest.testmod(np_session.session, verbose=True)

Session('1233182025_649324_20221215').data_dict['EcephysRigSync']
Session('1233182025_649324_20221215').mtrain
Session('1233182025_649324_20221215').project.lims


session = Session('1200879339_634837_20220825')

# doctest.testfile("README.md", module_relative=False, verbose=True)