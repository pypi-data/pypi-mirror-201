from typing import Union

from diengine_connect.datatypes import registry
from diengine_connect.driver.common import write_leb128
from diengine_connect.driver.exceptions import StreamCompleteException, StreamFailureError
from diengine_connect.driver.insert import InsertContext
from diengine_connect.driver.npquery import NumpyResult
from diengine_connect.driver.query import QueryResult, QueryContext
from diengine_connect.driver.types import ByteSource
from diengine_connect.driver.compression import get_compressor
from diengine_connect.driver.models import ColumnDef

_EMPTY_CTX = QueryContext()


class NativeTransform:

    @staticmethod
    def diengine_pares_response(respons, context: QueryContext = _EMPTY_CTX):
        names = []
        col_types = []
        data_list = []
        colums = respons['colum']
        for colum in colums:
            names.append(colum['name'])
            col_types.append(colum['type'])
        data = respons['data']
        for data_var in data:
            var_list = data_var.split(",")
            data_list.append(var_list)
        
        return QueryResult(data_list, None, tuple(names), tuple(col_types), context.column_oriented)
    
    # pylint: disable=too-many-locals
    @staticmethod
    def parse_response(source: ByteSource, context: QueryContext = _EMPTY_CTX) -> Union[NumpyResult, QueryResult]:
        names = []
        col_types = []
        block_num = 0

        def get_block():
            nonlocal block_num
            result_block = []
            try:
                try:
                    if context.block_info:
                        source.read_bytes(8)
                    num_cols = source.read_leb128()
                except StreamCompleteException:
                    return None
                num_rows = source.read_leb128()
                for col_num in range(num_cols):
                    name = source.read_leb128_str()
                    type_name = source.read_leb128_str()
                    if block_num == 0:
                        names.append(name)
                        col_type = registry.get_from_name(type_name)
                        col_types.append(col_type)
                    else:
                        col_type = col_types[col_num]
                    context.start_column(name)
                    column = col_type.read_column(source, num_rows, context)
                    result_block.append(column)
            except Exception as ex:
                source.close()
                if isinstance(ex, StreamCompleteException):
                    # We ran out of data before it was expected, this could be ClickHouse reporting an error
                    # in the response
                    message = source.last_message
                    if len(message) > 1024:
                        message = message[-1024:]
                    error_start = message.find('Code: ')
                    if error_start != -1:
                        message = message[error_start:]
                    raise StreamFailureError(message) from None
                raise
            block_num += 1
            return result_block

        first_block = get_block()
        if first_block is None:
            return NumpyResult() if context.use_numpy else QueryResult([])

        def gen():
            yield first_block
            while True:
                next_block = get_block()
                if next_block is None:
                    return
                yield next_block

        if context.use_numpy:
            d_types = [col.dtype if hasattr(col, 'dtype') else 'O' for col in first_block]
            return NumpyResult(gen(), tuple(names), tuple(col_types), d_types, source)
        return QueryResult(None, gen(), tuple(names), tuple(col_types), context.column_oriented, source)

    @staticmethod
    def build_insert(context: InsertContext):
        compressor = get_compressor(context.compression)

        def chunk_gen():
            for x in context.next_block():
                output = bytearray()
                write_leb128(x.column_count, output)
                write_leb128(x.row_count, output)
                for col_name, col_type, data in zip(x.column_names, x.column_types, x.column_data):
                    write_leb128(len(col_name), output)
                    output += col_name.encode()
                    write_leb128(len(col_type.name), output)
                    output += col_type.name.encode()
                    context.start_column(col_name)
                    try:
                        col_type.write_column(data, output, context)
                    except Exception as ex:  # pylint: disable=broad-except
                        # This is hideous, but some low level serializations can fail while streaming
                        # the insert if the user has included bad data in the column.  We need to ensure that the
                        # insert fails (using garbage data) to avoid a partial insert, and use the context to
                        # propagate the correct exception to the user
                        context.insert_exception = ex
                        yield 'INTERNAL EXCEPTION WHILE SERIALIZING'.encode()
                        return
                yield compressor.compress_block(output)
            footer = compressor.flush()
            if footer:
                yield footer

        return chunk_gen()
