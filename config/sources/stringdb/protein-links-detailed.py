from foo import Gene, PairwiseGeneToGeneInteraction
from bar import inject_files, inject_translation_table, next_row

_ingest_code = 'protein-links-detailed'

file, entrez_2_string = inject_files(_ingest_code)
translation_table = inject_translation_table(_ingest_code)

gene_a = Gene
gene_b = Gene

pairwise_gene_to_gene_interaction = PairwiseGeneToGeneInteraction

if file['combined_score'] >= 700:
    next_row()

#################################
# Above could be autogenerated using yaml + codegen
#
# Below contains ingest logic
#################################

gene_a.id = 'NCBIGene:' + entrez_2_string[file['protein1']]['entrez']
gene_b.id = 'NCBIGene:' + entrez_2_string[file['protein2']]['entrez']

pairwise_gene_to_gene_interaction.subject = gene_a
pairwise_gene_to_gene_interaction.object = gene_b
pairwise_gene_to_gene_interaction.relation = translation_table.global['interacts with']
