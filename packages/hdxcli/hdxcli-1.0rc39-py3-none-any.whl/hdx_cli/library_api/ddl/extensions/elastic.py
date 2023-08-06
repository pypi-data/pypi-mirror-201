from enum import Enum
from typing import Iterator, List, Union, Tuple

import json

from ..common_intermediate_representation import ColumnDefinition, DdlCreateTableInfo
from ..interfaces import SourceToTableInfoProcessor, ComposedTypeParser
from ...common.exceptions import NotSupportedException

__all__ = ['ElasticSourceToTableInfoProcessor',
           'ElasticComposedTypeParser']


# pylint: disable=R0903
class ElasticComposedTypeParser(ComposedTypeParser):
    def parse(self, ddl_datatype,
              simple_datatypes_mapping,
              compound_datatypes_mapping) -> List[str]:
        pass


class ConstraintKind(Enum):
    NULLABLE = 0
    PRIMARY_KEY = 1
    # pass


class ParseContext(Enum):
    UNKNOWN = 0
    TABLE = 1
    COLUMN = 2
    COLUMNCONSTRAINT = 3


# pylint: disable=R0903
class ElasticSourceToTableInfoProcessor(SourceToTableInfoProcessor):
    def yield_table_info_tokens(self, source_mapping: str,
                                mapper) -> Iterator[Union[ColumnDefinition, Tuple[str, str]]]:
        elastic_json = json.loads(source_mapping)
        top_level_key = list(elastic_json.keys())[0]
        elastic_mappings = elastic_json[top_level_key]['mappings']
        if elastic_mappings['dynamic'].lower() in ('true'):
            raise NotSupportedException('Elastic dynamic mappings are not supported')
        prj_name, tbl_name = top_level_key, top_level_key
        yield (prj_name, tbl_name)
        for prop_name, prop_value in elastic_mappings["properties"].items():
            if prop_type := prop_value.get('type'):
                if prop_type == 'alias':
                    yield ColumnDefinition(datatype=prop_type,
                                           identifier=prop_name,
                                           ignored_field=True)
                else:
                    yield ColumnDefinition(datatype=prop_type,
                                           hdx_datatype=mapper(prop_type),
                                           identifier=prop_name,
                                           nullable=True)
