from tespy.components import (Source, Sink, Compressor)
from tespy.connections import Connection, Bus
from tespy.tools import ExergyAnalysis
from tespy.networks import Network

# fluids
f = 'Hydrogen'
ff = {f: 1}

# network
nw = Network(fluids=[f], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s')

# define components
so = Source('Source')
si = Sink('Sink')
cp = Compressor('Compressor')

# set connections
c1 = Connection(so, 'out1', cp, 'in1')
c2 = Connection(cp, 'out1', si, 'in1')

nw.add_conns(c1, c2)

# connection parameters
c1.set_attr(m=1, p=30, T=25, fluid=ff)
c2.set_attr(p=300)

# component parameters
cp.set_attr(eta_s=0.85)

# power and product (hydrogen) bus
motor = Bus('motor')
motor.add_comps({'comp': cp, 'char': 1.0, 'base': 'bus'})  # motor mech./el. eff. 1.0

hydrogen = Bus('hydrogen')
hydrogen.add_comps({'comp': so, 'base': 'bus'}, {'comp': si})

# solve network
nw.solve(mode='design')
nw.print_results()

# exergy analysis
ean = ExergyAnalysis(network=nw, E_F=[motor], E_P=[hydrogen])
ean.analyse(1.013, 25)
ean.print_results()
