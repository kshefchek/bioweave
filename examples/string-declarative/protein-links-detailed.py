import re

from koza.model.biolink import Protein, PairwiseGeneToGeneInteraction, predicate
from koza.manager.data_provider import inject_row, inject_translation_table
from koza.manager.data_collector import collect

row = inject_row('protein-links-detailed')
translation_table = inject_translation_table()

protein_a = Protein()
protein_b = Protein()

pairwise_gene_to_gene_interaction = PairwiseGeneToGeneInteraction()

protein_a.id = 'ENSEMBL:' + re.sub(r'\d+\.', '', row['protein1'])
protein_b.id = 'ENSEMBL:' + re.sub(r'\d+\.', '', row['protein2'])

pairwise_gene_to_gene_interaction.subject = protein_a
pairwise_gene_to_gene_interaction.object = protein_b
pairwise_gene_to_gene_interaction.predicate = predicate.interacts_with
#pairwise_gene_to_gene_interaction.relation = translation_table.global_table['interacts with']
pairwise_gene_to_gene_interaction.relation = 'RO:0002436'

collect(protein_a, protein_b, pairwise_gene_to_gene_interaction)