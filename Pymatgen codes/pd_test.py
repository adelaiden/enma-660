from pymatgen import MPRester
from pymatgen import Element, Composition
from pymatgen.phasediagram.maker import PhaseDiagram
from pymatgen.phasediagram.entries import PDEntry
from pymatgen.phasediagram.plotter import PDPlotter
from pymatgen.phasediagram.analyzer import PDAnalyzer
from pymatgen.analysis.reaction_calculator import Reaction, ComputedReaction
import matplotlib.pyplot as plt 
import sys

with MPRester() as m:
	entries = m.get_entries_in_chemsys(['Li', 'Ni','Mn','Co','O'])
	decomps = m.get_entries('LiCoO2')

for entry in decomps:
	print entry.name

decomps_sort = sorted(decomps, key=lambda e: e.energy_per_atom)

for entry in decomps_sort:
	print entry.name

sys.exit()
pd = PhaseDiagram(entries) # constructs the ConvexHull

pda = PDAnalyzer(pd) # function for analyzing the phase diagram lol

comp  = Composition('LiNiMnCoO2')
decomp, ehull = pda.get_decomp_and_e_above_hull(PDEntry(comp, 0)) 

print ehull/comp.num_atoms



sys.exit()
# print ent.energy
# print ent.uncorrected_energy
# print ent.correction

# print len(evolution_profile)
# print evolution_profile[5]['evolution']

# for x in range((len(evolution_profile))):
# 	print x
# 	if abs(evolution_profile[x]['evolution']) < 0.0001:
# 		cat = evolution_profile[x]['chempot'] - evolution_profile[x]['element_reference'].energy
# 		ano = evolution_profile[x+1]['chempot'] - evolution_profile[x+1]['element_reference'].energy
# 		print 'Stability window for ' +'Li3PS4'+ ' is: '+ str(cat) + ' to ' + str(ano)


def get_stability_window(chsys, formula_id, elem):
	'''chsys is the a list of strings of the elements in the chemical system, 
	mpid is a string of the materials project ID for the formula of interest, elem is the open element'''
	cat = 0
	ano = 0


	chempots = []
	phases = []
	with MPRester() as m:
		entries = m.get_entries_in_chemsys(chsys)
		compound = m.get_entry_by_material_id(formula_id)

	pd = PhaseDiagram(entries)
	pda = PDAnalyzer(pd)

	evolution_profile = pda.get_element_profile(Element(elem), Composition(compound.name))
	ref = evolution_profile[0]['element_reference'].energy_per_atom
	reac = [compound]
	reac.append(evolution_profile[0]['element_reference'])

	# print [entry.name for entry in evolution_profile[0]['entries']]

	# base_enthalpy = ComputedReaction(reac, evolution_profile[0]['entries']).calculated_reaction_energy
	# print base_enthalpy
	
	enthalpies = []
	evolutions = []
	
	for stage in evolution_profile:
		rxn = ComputedReaction(reac, stage['entries'])
		rxn.normalize_to(Composition(compound.name))
		enthalpies.append(rxn.calculated_reaction_energy)
		evolutions.append(stage['evolution'])

	for stage in evolution_profile:
		chempots.append(-(stage['chempot'] - ref))
		namelist = []
		for entry in stage['entries']:
			namelist.append(entry.name)
		phases.append(namelist)
	
	for x in range((len(evolution_profile))):
		if abs(evolution_profile[x]['evolution']) < 0.0001:
			cat = evolution_profile[x]['chempot'] - ref
			ano = evolution_profile[x+1]['chempot'] - ref
			proc = evolution_profile[x+1]['entries']
			#proc.append(evolution_profile[0]['element_reference'])
			#print evolution_profile[x+1]['reaction']
			#print ComputedReaction([reac], proc).calculated_reaction_energy
			# print 'Stability window for ' +formula+ ' is: '+ str(cat) + ' to ' + str(ano)
	print chempots
	print phases 
	print enthalpies
	print evolutions
	
	yvec = []
	for i in range(len(chempots)):
		ynew = evolutions[i]*chempots[i] + enthalpies[i]
		yvec.append(ynew)
	
	return [chempots, yvec]


# LPS = get_stability_window(['Li','P','S'], 'Li3PS4', 'Li')
# LLZO = get_stability_window(['Li','La','Zr','O'], 'Li7La3Zr2O12', 'Li')
# LATP = get_stability_window(['Li','Al','Ti','P','O'],'Li13Al3Ti17P30O120', 'Li')

# print 'LPS: ', LPS
# print 'LLZO: ', LLZO
# print 'LATP: ', LATP

LCO = get_stability_window(['Li','Fe','P','O'], 'mp-19017', 'O')
print 'LCO: ', LCO

plt.plot(LCO[0], LCO[1], 'k')

plt.ylabel('Reaction Enthalpy per Formula Unit of Cathode Material (eV)')
plt.xlabel('Chemical Potential of O2 (eV)')
plt.show()

sys.exit()
LMO = get_stability_window(['Li','Mn','O'], 'LiMn2O4', 'O')
print 'LiMn2O4: ', LMO
LFPO = get_stability_window(['Li','Fe','P','O'], 'LiFePO4', 'O')
print 'LFPO: ', LFPO
LLZO = get_stability_window(['Li','La','Zr','O'], 'Li7La3Zr2O12', 'O')
print 'LLZO: ', LLZO

LATP = get_stability_window(['Li','Al','Ti','P','O'],'Li13Al3Ti17P30O120', 'O')
print 'LATP: ', LATP




