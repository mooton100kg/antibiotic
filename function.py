import pandas as pd
import random

def modify_drugs(col_drugs, col_bacs, drugs, bacs): 
	# Apply the transformation
	for column in col_drugs:
		drugs[column] = drugs[column].apply(
			lambda x: [line.strip() for line in str(x).split("\n")] if pd.notnull(x) else []
		)
	for column in col_bacs:
		bacs[column] = bacs[column].apply(
			lambda x: x.strip()
		)
	
	drugs_bacs = {'drug':[], 'bac':[]}

	for d in drugs.index.tolist():
		# get data of each drug
		bac_set = set()

		# find what bac is in type col
		for t in drugs.loc[d, 'type']:
			bac_set.update(bacs[bacs['type shape'] == t].index)
		
		# find what bac is in group col
		for g in drugs.loc[d, 'group']:
			bac_set.update(bacs[bacs['group'] == g].index)

		# add bac in other bac col
		bac_set.update(drugs.loc[d, 'other bac'])

		# remove any bac that in no col
		bac_set = bac_set - set(drugs.loc[d, 'no'])
		
		# add drug and bac_set to dict
		drugs_bacs['drug'].append(d)
		drugs_bacs['bac'].append(list(bac_set))

	drugs = pd.DataFrame.from_dict(drugs_bacs)
	return drugs, bacs

def get_drug_from_bac(bac, bacs, drugs):
	# get usable drug from bacteria name
	# check if bac is in database
	if bac in bacs.index:
		drug_list = [d 
			for d in drugs['drug'] 
			if bac in drugs[drugs['drug'] == d]['bac'].iloc[0]
		]
		return drug_list
	else:
		return []

def get_bac_from_drug(drug, bacs, drugs):
	# get all bac that susceptible to drug
	# check if drug is in database
	if drug in drugs['drug'].tolist():
		return drugs[drugs['drug'] == drug]['bac'].iloc[0]
	else:
		return []

def create_question(bacs, drugs):
	while True:
		bac = random.choice(bacs.index)

		drug_list = get_drug_from_bac(bac, bacs, drugs)
		drug = random.choice(drug_list)

		drug_no_list = list(set(drugs['drug']) - set(drug_list))

		drug_choice = [drug] + random.sample(drug_no_list, 3)
		random.shuffle(drug_choice)



		print(f'Bacteria : {bac}\n')
		for index, d in enumerate(drug_choice):
			print(f'{index+1} : {d}')
			if drug == d:
				correct_choice = index+1

		
		ans = input('\nANS : ')
		try:
			if int(ans) == correct_choice:
				print('Correct\n')
			elif int(ans) == 0:
				break
			else:
				print(f'Incorrect : {drug}\n')
		except:
			print('Error\n')
