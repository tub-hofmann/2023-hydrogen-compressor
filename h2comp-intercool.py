from tespy.components import (Source, Sink, Compressor, HeatExchanger)
from tespy.connections import Connection, Bus
from tespy.networks import Network

# fluids
h = 'H2'
a = 'air'
hh = {h: 1, a: 0}
aa = {a: 1, h: 0}

# network
nw = Network(fluids=[h, a], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s')

# define components
soh = Source('SourceHydrogen')
sih = Sink('SinkHydrogen')
soa = Source('SourceAir')
sia = Sink('SinkAir')
cp1 = Compressor('Compressor1')
chx = HeatExchanger('Intercooler')
cp2 = Compressor('Compressor2')

# set connections
c1 = Connection(soh, 'out1', cp1, 'in1')
c2 = Connection(cp1, 'out1', chx, 'in1')
c3 = Connection(chx, 'out1', cp2, 'in1')
c4 = Connection(cp2, 'out1', sih, 'in1')
c11 = Connection(soa, 'out1', chx, 'in2')
c12 = Connection(chx, 'out2', sia, 'in1')

nw.add_conns(c1, c2, c3, c4, c11, c12)

# connection parameters
c1.set_attr(m=1, p=30, T=25, fluid=hh)
c2.set_attr(p=95)  # optimize this parameter !
c4.set_attr(p=300)
c11.set_attr(m=500, p=1.013, T=25, fluid=aa)

# component parameters
cp1.set_attr(eta_s=0.85)
cp2.set_attr(eta_s=0.85)
chx.set_attr(pr1=1,pr2=1,Q=-2e6)

# power and product (hydrogen) bus
motor1 = Bus('motor1')
motor1.add_comps({'comp': cp1, 'char': 1.0, 'base': 'bus'})  # motor1 mech./el. eff. 1.0
motor2 = Bus('motor2')
motor2.add_comps({'comp': cp2, 'char': 1.0, 'base': 'bus'})  # motor2 mech./el. eff. 1.0

hydrogen = Bus('hydrogen')
hydrogen.add_comps({'comp': soh, 'base': 'bus'}, {'comp': sih})

# solve network
nw.solve(mode='design')
nw.print_results()
