# Importing mamba is not needed!
# import mamba
from expects import *

with description('mamba'):
    with it('true is true'):
        expect(True).to(be_false)