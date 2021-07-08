import types
from typing import Iterable

import pytest
from biolink_model_pydantic.model import (
    Gene,
    GeneToPhenotypicFeatureAssociation,
    NamedThingToInformationContentEntityAssociation,
    PhenotypicFeature,
    Publication,
)

from koza.app import KozaApp
from koza.koza_runner import get_translation_table, set_koza
from koza.model.config.source_config import PrimaryFileConfig
from koza.model.source import Source, SourceFile


@pytest.fixture
def mock_koza():

    # This should be extracted out but for quick prototyping
    def _mock_write(self, source_name, *entities):
        self._entities = list(*entities)

    def _make_mock_koza_app(
        name: str,
        data: Iterable,
        transform_code: str,
        map_cache=None,
        filters=None,
        translation_table=None,
    ):
        mock_source_file_config = PrimaryFileConfig(
            name=name,
            files=[],
            transform_code=transform_code,
        )
        mock_source_file = SourceFile(mock_source_file_config)
        mock_source_file._reader = data

        mock_source = Source(source_files=[mock_source_file])

        koza = KozaApp(mock_source)
        # TODO filter mocks
        koza.source.translation_table = translation_table
        koza.map_cache = map_cache
        koza.write = types.MethodType(_mock_write, koza)

        return koza

    def _transform(
        name: str,
        data: Iterable,
        transform_code: str,
        map_cache=None,
        filters=None,
        translation_table=None,
    ):
        koza_app = _make_mock_koza_app(
            name,
            data,
            transform_code,
            map_cache=map_cache,
            filters=filters,
            translation_table=translation_table,
        )
        set_koza(koza_app)
        koza_app.process_sources()
        return koza_app._entities

    return _transform


@pytest.fixture
def gene_information_entities(mock_koza):
    row = iter(
        [
            {
                'DB': 'Xenbase',
                'DB_Object_ID': 'XB-GENE-478054',
                'DB_Object_Symbol': 'trnt1',
                'DB_Object_Name': 'tRNA nucleotidyl transferase, CCA-adding, 1',
                'DB_Object_Synonym(s)': 'cca1|mtcca|tRNA nucleotidyl transferase|xcca',
                'DB_Object_Type': 'gene',
                'Taxon': 'taxon:8364',
                'Parent_Object_ID': '',
                'DB_Xref(s)': 'NCBI_Gene:394602|UniProtKB:F6V8Z1|UniProtKB:F7DM70|UniProtKB:Q6P873',
                'Properties': '',
            }
        ]
    )

    return mock_koza('gene-information', row, './examples/xenbase/gene-information.py')


def test_gene_information_gene(gene_information_entities):
    assert len(gene_information_entities) == 1
    gene = gene_information_entities[0]
    assert gene


def test_gene_information_synonym(gene_information_entities):
    gene = gene_information_entities[0]
    assert gene.synonym
    assert 'xcca' in gene.synonym


def test_gene_information_id(gene_information_entities):
    gene = gene_information_entities[0]
    assert gene.id == 'Xenbase:XB-GENE-478054'


@pytest.fixture
def gene2phenotype_entities(mock_koza):
    row = iter(
        [
            {
                'SUBJECT': 'XB-GENE-1000632',
                'SUBJECT_LABEL': 'dctn2',
                'SUBJECT_TAXON': 'NCBITaxon:8364',
                'SUBJECT_TAXON_LABEL': 'Xla',
                'OBJECT': 'XPO:0102358',
                'OBJECT_LABEL': 'abnormal tail morphology',
                'RELATION': 'RO_0002200',
                'RELATION_LABEL': 'has_phenotype',
                'EVIDENCE': '',
                'EVIDENCE_LABEL': '',
                'SOURCE': 'PMID:17112317',
                'IS_DEFINED_BY': '',
                'QUALIFIER': '',
            }
        ]
    )
    return mock_koza('gene-to-phenotype', row, './examples/xenbase/gene-to-phenotype.py')


def test_gene2_phenotype_transform(gene2phenotype_entities):
    assert gene2phenotype_entities
    assert len(gene2phenotype_entities) == 3
    genes = [entity for entity in gene2phenotype_entities if isinstance(entity, Gene)]
    phenotypes = [
        entity for entity in gene2phenotype_entities if isinstance(entity, PhenotypicFeature)
    ]
    associations = [
        entity
        for entity in gene2phenotype_entities
        if isinstance(entity, GeneToPhenotypicFeatureAssociation)
    ]
    assert len(genes) == 1
    assert len(phenotypes) == 1
    assert len(associations) == 1


def test_gene2_phenotype_transform_publications(gene2phenotype_entities):
    associations = [
        entity
        for entity in gene2phenotype_entities
        if isinstance(entity, GeneToPhenotypicFeatureAssociation)
    ]
    assert 'PMID:17112317' in associations[0].publications


@pytest.fixture
def gene_literature_entities(mock_koza):
    row = iter(
        [
            {
                'xb_article': 'XB-ART-1',
                'pmid': '16938438',
                'gene_pages': 'XB-GENEPAGE-487723 nog,XB-GENEPAGE-490377 msx1,XB-GENEPAGE-481828 bmp2,XB-GENEPAGE-483057 bmp4,XB-GENEPAGE-480982 fgf8,XB-GENEPAGE-6045068 hspa1l,XB-GENEPAGE-485625 hsp70',
            }
        ]
    )
    map_cache = {
        'genepage-2-gene': {
            'XB-GENEPAGE-487723': {
                'tropicalis_id': 'XB-GENE-487724',
                'laevis_l_id': 'XB-GENE-864891',
                'laevis_s_id': 'XB-GENE-17332089',
            },
            'XB-GENEPAGE-490377': {
                'tropicalis_id': 'XB-GENE-490378',
                'laevis_l_id': 'XB-GENE-490382',
                'laevis_s_id': 'XB-GENE-6253888',
            },
            'XB-GENEPAGE-481828': {
                'tropicalis_id': 'XB-GENE-481829',
                'laevis_l_id': 'XB-GENE-6252323',
                'laevis_s_id': 'XB-GENE-481833',
            },
            'XB-GENEPAGE-483057': {
                'tropicalis_id': 'XB-GENE-483058',
                'laevis_l_id': 'XB-GENE-483062',
                'laevis_s_id': 'XB-GENE-6254046',
            },
            'XB-GENEPAGE-480982': {
                'tropicalis_id': 'XB-GENE-480983',
                'laevis_l_id': 'XB-GENE-865429',
                'laevis_s_id': 'XB-GENE-17330198',
            },
            'XB-GENEPAGE-6045068': {
                'tropicalis_id': 'XB-GENE-6045069',
                'laevis_l_id': 'XB-GENE-17342842',
                'laevis_s_id': 'XB-GENE-6254949',
            },
            'XB-GENEPAGE-485625': {
                'tropicalis_id': 'XB-GENE-485626',
                'laevis_l_id': 'XB-GENE-485630',
                'laevis_s_id': 'XB-GENE-17340402',
            },
        }
    }
    tt = get_translation_table("examples/translation_table.yaml", None)

    return mock_koza(
        'gene-literature',
        row,
        './examples/xenbase/gene-literature.py',
        map_cache=map_cache,
        translation_table=tt,
    )


def test_gene_literature_entities(gene_literature_entities):
    assert gene_literature_entities


def test_gene_literature_entity_types(gene_literature_entities):
    publications = [
        entity for entity in gene_literature_entities if isinstance(entity, Publication)
    ]
    genes = [entity for entity in gene_literature_entities if isinstance(entity, Gene)]
    associations = [
        entity
        for entity in gene_literature_entities
        if isinstance(entity, NamedThingToInformationContentEntityAssociation)
    ]

    # a roundabout way of confirming that everything generated is one of these three and there's nothing else
    assert len(gene_literature_entities) == len(publications) + len(genes) + len(associations)
    assert len(publications) == 1


def test_gene_literature_entity(gene_literature_entities):
    genes = [entity for entity in gene_literature_entities if isinstance(entity, Gene)]

    # confirm one gene id from each species
    assert 'Xenbase:XB-GENE-480983' in [gene.id for gene in genes]
    assert 'Xenbase:XB-GENE-6253888' in [gene.id for gene in genes]
    assert 'Xenbase:XB-GENE-485630' in [gene.id for gene in genes]
