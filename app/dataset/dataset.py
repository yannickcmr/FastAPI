from typing import Protocol, Optional
import pandas as pd


""" Response Class """

class Response(Protocol):
    """ Default Response Class """
    msg: str
    code: int
    data: Optional[dict] = None
    ...


""" CSV Reader Class """

class DatasetReader:
    """ Test Dataset Reader for .csv Files. """

    def __init__(self, filename: str, delimiter: str = ";", chunk_size: int = 10_000):
        self.filename = filename
        self._chunk_size = chunk_size
        self._delimiter = delimiter

        # testing dataset.
        self.get_columns()

    def log_settings(self) -> None:
        """ Method to log current settings. """
        print(f"{self.filename=} - {self._chunk_size=}")
        print(f"columns: {self.get_columns()['data']['columns']}")

    def get_columns(self) -> Response:
        """ Method for getting all the .csv file's columns. """
        try:
            columns = pd.read_csv(self.filename, nrows=1, delimiter=self._delimiter)
            columns = columns.columns.tolist()

        except Exception as e:
            raise MemoryError(f"Could not get columns: {e}")

        return {
            'msg': ".get_columns success.",
            'code': 200,
            'data': {
                'columns': list(columns)
            }
        }

    def find(self, query = "index==index") -> Response:
        """ Method for filtering the .csv file with a query. """
        try:
            columns = self.get_columns()
            dataframe = pd.DataFrame(columns=columns['data']['columns'])

            for chunk in pd.read_csv(self.filename, chunksize=self._chunk_size, delimiter=self._delimiter):
                try:
                    data = chunk.query(query)
                    dataframe = pd.concat([dataframe, data], ignore_index=True)

                except Exception as e:
                    print(f"Could not parse chunks: {e}")

            if len(dataframe) == 0:
                raise ValueError(f"Could not find any results for query: {query}")

        except Exception as e:
           print(f"Could not find query in dataset: {e}")

        return {
            'msg': ".findall success.",
            'code': 200,
            'data': {
                'query': query,
                'result': dataframe.to_json()
            }
        }


""" Testing """

if __name__ == "__main__":
    def log_info(msg: str, bar_size: int = 10) -> None:
        bar = "=" * bar_size
        print(f"{bar} - {msg} - {bar}")

    log_info("Test running!")

    FILENAME = """business_sales.csv"""

    dataset = DatasetReader(FILENAME, chunk_size=10000)
    dataset.log_settings()

    result = dataset.find("price < 100")
    dataframe = pd.read_json(result['data']['result'])
    print(dataframe)

    log_info("Test success!")
