import pandas as pd

class GetData:
    def __init__(self, file_path):
        """
        Initialize the GetData class with the file path of the Excel file.

        :param file_path: Path to the Excel file containing the data
        """
        self.file_path = file_path

    def get_data(self, cif):
        """
        Retrieve unique SUBHEADER values based on the given CIF and specific TRX_TYPE conditions.

        :param cif: The CIF value to filter the data
        :return: A list of unique SUBHEADER values that match the criteria
        """
        try:
            # Load the data from the Excel file
            data = pd.read_excel(self.file_path)

            # Filter the data based on CIF and TRX_TYPE conditions
            filtered_data = data[
                (data['CIF'] == cif) &
                ((data['TRX_TYPE'] == 'Pembayaran') | (data['TRX_TYPE'] == 'Pembayaran Qris'))
            ]

            # Return unique SUBHEADER values
            return filtered_data['SUBHEADER'].unique().tolist()
        except Exception as e:
            print(f"An error occurred: {e}")
            return []