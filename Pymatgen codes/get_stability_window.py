from pymatgen import MPRester
from pymatgen import Element, Composition
from pymatgen.phasediagram.maker import PhaseDiagram
from pymatgen.phasediagram.plotter import PDPlotter
from pymatgen.phasediagram.analyzer import PDAnalyzer


def get_stability_window(chsys, formula):
	'''chsys is the a list of strings of the elements in the chemical system, 
	formula is a string of chemical formula'''
	with MPRester() as m:
		entries = m.get_entries_in_chemsys(chsys)
	pd = PhaseDiagram(entries)
	pda = PDAnalyzer(pd)
	evolution_profile = pda.get_element_profile(Element('Li'), Composition(formula))
	ref = evolution_profile[0]['element_reference'].energy
	
	for x in range((len(evolution_profile))):
		if abs(evolution_profile[x]['evolution']) < 0.0001:
			cat = evolution_profile[x]['chempot'] - ref
			ano = evolution_profile[x+1]['chempot'] - ref
			# print 'Stability window for ' +formula+ ' is: '+ str(cat) + ' to ' + str(ano)
	return [cat, ano]


LPS = get_stability_window(['Li','P','S'], 'Li3PS4')
LLZO = get_stability_window(['Li','La','Zr','O'], 'Li7La3Zr2O12')
LATP = get_stability_window(['Li','Al','Ti','P','O'],'Li13Al3Ti17P30O120')

print 'LPS: ', LPS
print 'LLZO: ', LLZO
print 'LATP: ', LATP