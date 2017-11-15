from pymatgen import MPRester, Element, Composition
from pymatgen.phasediagram.maker import PhaseDiagram
from pymatgen.phasediagram.entries import PDEntry
from pymatgen.phasediagram.analyzer import PDAnalyzer
import matplotlib.pyplot as plt
import sys

def get_interface_energies(m_id1, m_id2, chemsys):
	'''m_id1 and m_id2 are Materials Project material identifier strings, chemsys is a list of strings of all the 
	elements in the system. This function returns the negative of the energy above hull for the interface compounds 
	as a list of float. '''
	with MPRester() as m:
		entries = m.get_entries_in_chemsys(chemsys)
		m1 = m.get_entry_by_material_id(m_id1)
		m2 = m.get_entry_by_material_id(m_id2)

	m1C = Composition(m1.name)
	m2C = Composition(m2.name)

	pd = PhaseDiagram(entries)
	pda = PDAnalyzer(pd)

	x = []
	ehull = []
	for i in range(11):
		x.append(i/float(10))

	# print 1/m1C.num_atoms, 1/m2C.num_atoms
	# print m1C

	for i in x:
		E0 = m1.energy_per_atom * i + m2.energy_per_atom * (1 - i)
		comp = (1/m1C.num_atoms) * i * m1C + (1/m2C.num_atoms) * (1 - i) * m2C
		ehull.append((-1) * pda.get_e_above_hull(PDEntry(comp, E0)))

	# ehull[-1] = 0.0
	return ehull


lps_lco = get_interface_energies('mp-985583', 'mp-24850', ['Li','P','S','Co','O'])
llzo_lco = get_interface_energies('mp-942733', 'mp-24850', ['Li','La','Zr','Co','O'])
#latp_lco = get_interface_energies('', 'mp-24850', ['Li','Al','Ti','P','O','Co'])

vec = []
for i in range(len(lps_lco)):
	vec.append(i/float(len(lps_lco)-1))

fig, ax = plt.subplots()
ax.plot(vec, lps_lco, 'k', label='LPS-LCO')
ax.plot(vec, llzo_lco, 'b', label='LLZO-LCO')
ax.legend(loc='lower right')

plt.ylabel('-E Above Hull (eV)')
plt.xlabel('Mol frac SE')
plt.show()



